FROM python:3.8-slim

WORKDIR /app

COPY load_balancer.py .

RUN pip install flask requests

EXPOSE 80

CMD ["python", "load_balancer.py"]
