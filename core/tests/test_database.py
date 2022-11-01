import pytest
from fastapi.testclient import TestClient

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base

from core.main import app, get_db

# Documentatino https://stackoverflow.com/questions/67255653/how-to-set-up-and-tear-down-a-database-between-tests-in-fastapi

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/test-fastapi"

DATABASE_URL = SQLALCHEMY_DATABASE_URL
engine = create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


def test_post_entry(client):
    response = client.get("/")
    client.post('api/v1/daily-return/new/00dc9d7c-fcef-4653-a3e8-2931ba5665b4/4500')
    assert response.status_code == 200

    item = client.get('api/v1/daily-return/00dc9d7c-fcef-4653-a3e8-2931ba5665b4')
    item_json = item.json()
    assert item.status_code == 200
    assert type(item_json['requested_id']) == str
    assert item_json['data']['last_price'] == 4500
    assert "data" in item_json


def test_update_entry(client):
    response = client.get('/')
    assert response.status_code == 200

    item = client.post('api/v1/daily-return/new/00dc9d7c-fcef-4653-a3e8-2931ba5665b4/4500')
    item_json = item.json()
    assert item.status_code == 200
    assert type(item_json['requested_id']) == str
    assert item_json['data']['last_price'] == 4500
    assert "data" in item_json

    entry_id = item_json['data']['id']
    updated_item = client.patch(f"/api/v1/daily-return/update/{entry_id}/5000")
    updated_item_json = updated_item.json()
    assert type(updated_item_json['requested_id']) == str
    assert "data" in updated_item_json
    assert updated_item.status_code == 200
    assert updated_item_json['data']['last_price'] == 5000


def test_delete_entry(client):
    response = client.get('/')
    assert response.status_code == 200

    item = client.post('api/v1/daily-return/new/00dc9d7c-fcef-4653-a3e8-2931ba5665b4/4500')
    item_json = item.json()
    assert item.status_code == 200
    assert "data" in item_json
    assert type(item_json['requested_id']) == str
    assert item_json['data']['last_price'] == 4500

    entry_id = item_json['data']['id']
    response = client.delete(f"/api/v1/daily-return/delete/{entry_id}")
    assert response.status_code == 200

    response_json = response.json()
    assert "data" in response_json
    assert type(response_json['data']['delete_id']) == str
    assert response_json['data']['detail'] == 'Entry deleted'
