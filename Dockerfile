FROM python:3.14-alpine

RUN addgroup -S jhongroup && adduser -S jhon -G jhongroup
RUN mkdir -p /home/jhon/Downloads/ /home/jhon/Downloads/robotcasino/ /home/jhon/.cache/robotcasino/logs/ /tmp/robotcasino/ 

RUN apk update && apk add --no-cache \
    chromium \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY ./src/ .

RUN pip install --no-cache-dir /app

RUN chown -R jhon:jhongroup /app && \
    chown -R jhon:jhongroup /home/jhon/Downloads/robotcasino/ && \
    chown -R jhon:jhongroup /home/jhon/.cache/robotcasino/logs/ && \
    chown -R jhon:jhongroup /tmp/robotcasino/

ENV PYTHONUNBUFFERED=1

USER jhon

ENTRYPOINT ["robotcasino"]
CMD ["run"]