FROM python:3-alpine

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt


COPY . /code
WORKDIR /code
CMD ["python", "app.py"]

EXPOSE 5000