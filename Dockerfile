FROM python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# Run the application:
COPY app.py .
COPY static static/
COPY templates templates/
CMD ["/opt/venv/bin/python", "app.py"]

