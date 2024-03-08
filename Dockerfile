FROM python:3.8

RUN mkdir /test_task

WORKDIR /test_task

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh