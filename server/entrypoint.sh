#!/bin/sh

# Below shells script is required because the flask container need to wait for postgres db server to startup before
# accessing it below.

RETRIES=5
USER=postgres
DATABASE=users_dev
HOST=postgres

until psql -h $HOST -U $USER -d $DATABASE -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server to start, $((RETRIES)) remaining attempts..."
  RETRIES=$((RETRIES-=1))
  sleep 1
done

echo "PostgreSQL started!"

if test -f "main/ml/GoogleNews-vectors-negative300.bin"; then
  echo "Word2vec already on machine."
else
  echo "[START] Downloading Google Word2Vec..."
  wget -nv -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz" -P main/ml
  echo "[END] Downloaded Google Word2Vec..."
  gzip -d main/ml/GoogleNews-vectors-negative300.bin.gz
fi

# Run below commands from manage.py to initialize db and have some default data.
python manage.py recreate_db
#python manage.py seed_db
#chmod 666 /root/nltk_data
uwsgi --ini /etc/uwsgi.ini