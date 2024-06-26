FROM docker/compose:alpine-1.29.2

WORKDIR /app

COPY bash.sh .
RUN apt-get install docker-compose-plugin
RUN chmod +x bash.sh
RUN ./bash.sh

