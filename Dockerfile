FROM tiangolo/uvicorn-gunicorn:python3.8-slim

WORKDIR /code
COPY .env /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./core /code/core

CMD ["uvicorn",  "core.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port" , "80"]
