FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask python-dateutil pandas gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]