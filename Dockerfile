FROM python:3.11-alpine

RUN apk update && apk add --no-cache \
    chromium \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    && rm -rf /var/cache/apk/*

WORKDIR /app/output

ENV PYTHONUNBUFFERED=1
ENV HEADLESS=1

ENV CHROME_BINARY_PATH=/usr/bin/chromium-browser

COPY . /app/

RUN pip install --no-cache-dir /app/

VOLUME /app/output

ENTRYPOINT ["robotcasino"]
CMD ["run"]