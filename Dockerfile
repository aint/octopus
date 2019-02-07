FROM python:3-alpine

COPY . /app
WORKDIR /app

RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 5000

CMD ["python", "app.py"]