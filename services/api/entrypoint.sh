#!/bin/bash

set -e

if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

if [ -f src/celery_app/celery.log ]; then
  > src/celery_app/celery.log
fi

alembic upgrade head

exec "$@"