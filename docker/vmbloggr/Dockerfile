FROM python:3.11.0-alpine

LABEL org.opencontainers.image.authors="name: Kelvin Johnson-Chu, email: ojkelvinchu@gmail.com"


# Set the desired time zone to Nigerian time (West Africa Time)
RUN ln -sf /usr/share/zoneinfo/Africa/Lagos /etc/localtime

# Get dependencies
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev freetype-dev


WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
# RUN pip install gunicorn
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./src /app/src
ADD ./docker /app/docker

RUN chmod +x /app/docker/vmbloggr/server-entrypoint.sh

# # change owner of all the files to the app user
# RUN chown -R vmblogger_app:vmblogger_app /app

# create the app user
#RUN addgroup -S vmblogger_app && adduser -S vmblogger_app -G vmblogger_app

# # change to the user vmblogger_app
# USER vmblogger_app