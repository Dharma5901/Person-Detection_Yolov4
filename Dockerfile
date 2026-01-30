FROM katomaran/python-slim3.6.8:open-cv-4.4.0

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . .