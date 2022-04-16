FROM python:3.9-slim AS build
#Update first
RUN apt-get update && apt-get upgrade -y && apt-get install git -y
ADD . /build
WORKDIR /build
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

#Multistage build with distroless image
FROM gcr.io/distroless/python3-debian11:nonroot
COPY --from=build --chown=nonroot:nonroot /build /discord_bot
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /discord_bot
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages

#Don't generate .pyc files, enable tracebacks on segfaults and disable STDOUT / STDERR buffering
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED 0

#For https://github.com/users/der-eddy/packages/container/package/shinobu_bot
LABEL org.opencontainers.image.source https://github.com/der-eddy/discord_bot

#add user, don't run as root
#distroless creates automatically a nonroot user with uid 65532:65532
USER nonroot

CMD [ "main.py", "docker"]
