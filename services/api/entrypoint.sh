#!/bin/bash

set -e

alembic upgrade head

exec "$@"