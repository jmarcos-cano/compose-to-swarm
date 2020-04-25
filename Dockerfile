FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY app/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt


COPY app/ /code
WORKDIR /code
CMD ["python", "server.py"]

EXPOSE 5000

