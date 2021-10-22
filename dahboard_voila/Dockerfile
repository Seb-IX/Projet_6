# lightweight python
FROM python:3.7-slim

RUN apt-get update

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN ls -la $APP_HOME/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install dependencies
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm