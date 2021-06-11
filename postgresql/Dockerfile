FROM postgres:9.6

LABEL maintainer="Octavian G"
LABEL description="image supporting data layer"
LABEL version="0.1"

# By copying it to below directory, init.sql runs each time the postgres container is started.
COPY init.sql /docker-entrypoint-initdb.d