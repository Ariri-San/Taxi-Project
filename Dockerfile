FROM mcr.microsoft.com/devcontainers/base:ubuntu
# Install the xz-utils packa
CMD [ "docker-compose", "--build", "-d", "up" ]