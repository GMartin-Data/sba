FROM python:3.11-slim

WORKDIR /web

COPY requirements.txt .

RUN python -m venv venv

# Append Left python from the venv
ENV PATH="opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Enable getting logs from Django within the terminal
ENV PYTHONUNBUFFERED 1

COPY . /web/

EXPOSE 8000

# Enable launching entrypoint script
RUN chmod +x /web/entrypoint.sh

CMD ["/web/entrypoint.sh"]