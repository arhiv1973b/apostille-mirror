FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests schedule
COPY robot.py .
CMD ["python3", "-u", "robot.py"]
