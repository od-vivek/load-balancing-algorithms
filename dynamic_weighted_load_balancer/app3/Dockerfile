FROM python:3.8-slim

WORKDIR /app

COPY app.py .

RUN pip install flask
RUN pip install psutil

EXPOSE 5000

CMD ["python", "app.py"]
