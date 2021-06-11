FROM python:3.8.5

LABEL maintainer="Octavian G"
LABEL description="backend"
LABEL version="0.1"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app

# Update working directory
WORKDIR /usr/src/app

# copy everything from this directory to server/flask docker container
COPY . /usr/src/app/

# Give execute permission to below file, so that the script can be executed by docker.
RUN chmod 777 /usr/src/app/entrypoint.sh

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Install nltk additional files
ENV NLTK_DATA /nltk_data/
ADD . $NLTK_DATA
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# COPY uswgi.ini
COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

# run server
CMD ["./entrypoint.sh"]