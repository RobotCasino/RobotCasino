FROM python:3.11-alpine

RUN addgroup -S jhongroup && adduser -S jhon -G jhongroup

RUN apk update && apk add --no-cache \
    chromium \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir /app/

RUN chown -R jhon:jhongroup /app

ENV PYTHONUNBUFFERED=1
ENV HEADLESS=1
ENV CHROME_BINARY_PATH=/usr/bin/chromium-browser

USER jhon

ENTRYPOINT ["robotcasino"]
CMD ["run"]