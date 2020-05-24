FROM python:3.6.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /Django3
WORKDIR /Django3
COPY . /Django3/
RUN pip install -r requirements.txt