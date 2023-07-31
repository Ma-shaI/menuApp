FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /app
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]