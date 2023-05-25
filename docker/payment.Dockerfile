FROM python:3.11.3-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /payment

CMD ["python", "main.py"]
