FROM alpine:3.14
# Install the xz-utils packa
CMD [ "docker-compose", "--build", "-d", "up" ]