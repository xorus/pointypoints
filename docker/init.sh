#!/bin/sh

alembic upgrade head
./start.sh prod
