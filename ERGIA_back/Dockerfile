FROM python:3.12-alpine

WORKDIR /code

ENV FLASK_APP=flaskr/main.py


RUN apk add --update --no-cache python3 py3-pip gcc musl-dev python3-dev libffi-dev openssl-dev

COPY . .

RUN pip install -r requirements.txt


EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]