# import os
# import pytest
# from fastapi.testclient import TestClient
# from decouple import config
#
# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from core.main import app, get_db
# from core.database import Base
#
#
# from uuid import uuid4
# from datetime import datetime
#
# DATABASE_URL = os.getenv("DATABASE_URL", config("DATABASE_URL"))
# engine = create_engine(
#     DATABASE_URL, pool_size=3, max_overflow=0
# )
#
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
#
#
# @pytest.fixture()
# def session():
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = TestingSessionLocal(bind=connection)
#     nested = connection.begin_nested()
#
#     @sa.event.listens_for(session, "after_transaction_end")
#     def end_savepoint(session, transaction):
#         nonlocal nested
#         if not nested.is_active:
#             nested = connection.begin_nested()
#
#     yield session
#
#     session.close()
#     transaction.rollback()
#     connection.close()
#
#
# @pytest.fixture()
# def client(session):
#     def override_db():
#         yield session
#
#     app.dependency_overrides[get_db] = override_db()
#     yield TestClient(app)
#     del app.dependency_overrides[get_db]
#
#
