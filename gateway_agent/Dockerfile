FROM python:3.11-slim
WORKDIR /app
RUN pip install requests
COPY proxy_logic.py .
CMD ["python", "proxy_logic.py"]
