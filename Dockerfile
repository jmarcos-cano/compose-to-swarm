FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt


COPY . /code
WORKDIR /code
CMD ["python", "app.py"]

EXPOSE 5000

