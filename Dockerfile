FROM python:3.11-alpine

RUN apk update && apk add --no-cache \
    chromium \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    && rm -rf /var/cache/apk/*

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV HEADLESS=1

ENV CHROME_BINARY_PATH=/usr/bin/chromium-browser

COPY . .

RUN pip install --no-cache-dir /app/

ENTRYPOINT ["robotcasino"]
CMD ["run"]