FROM python:3.7-slim AS build
#Update first
RUN apt-get update && apt-get upgrade -y
ADD . /build
WORKDIR /build
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

#Multistage build with distroless image
FROM gcr.io/distroless/python3-debian10
COPY --from=build /build /discord_bot
COPY --from=build /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
WORKDIR /discord_bot
ENV PYTHONPATH=/usr/local/lib/python3.7/site-packages

#Don't generate .pyc files and enable tracebacks on segfaults
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

CMD [ "main.py" ]