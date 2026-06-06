FROM python:3.14-alpine

RUN addgroup -S jhongroup && adduser -S jhon -G jhongroup

RUN apk update && apk add --no-cache \
    chromium \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY --chown=jhon:jhongroup ./src/ .

RUN pip install --no-cache-dir /app

RUN mkdir -p /home/jhon/.cache/robotcasino/logs/ /tmp/robotcasino/ /app/screenshots/ && \
    chown -R jhon:jhongroup /app && \
    chown -R jhon:jhongroup /home/jhon/.cache/robotcasino/logs/ && \
    chown -R jhon:jhongroup /tmp/robotcasino/ && \
    chown -R jhon:jhongroup /app/screenshots/

ENV PYTHONUNBUFFERED=1

USER jhon

ENTRYPOINT ["robotcasino"]
CMD ["run"]