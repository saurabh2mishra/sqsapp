FROM python:3.7

WORKDIR /sqs-test

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /src ./src

CMD [ "python -m", "src.process" ]
