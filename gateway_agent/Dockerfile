FROM python:3.11-slim

# Create a non-privileged user
RUN useradd -m actor-robot

WORKDIR /app
RUN pip install --no-cache-dir requests

COPY proxy_logic.py .
RUN chown -R actor-robot:actor-robot /app

USER actor-robot

# Basic healthcheck to ensure the container is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://host.docker.internal:11434/api/tags', timeout=2)" || exit 1

CMD ["python", "proxy_logic.py"]
