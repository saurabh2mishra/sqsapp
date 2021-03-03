FROM python:3.7

WORKDIR /dpg-test

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /dpg ./dpg

CMD [ "python", "./dpg/process.py" ]