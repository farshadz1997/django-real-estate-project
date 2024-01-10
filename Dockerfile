FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /django_real_estate
COPY requirements.txt ./
RUN pip install -r requirements.txt