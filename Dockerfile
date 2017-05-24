FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /example_app
WORKDIR /example_app
ADD . /example_app/
RUN pip install -r requirements.txt
