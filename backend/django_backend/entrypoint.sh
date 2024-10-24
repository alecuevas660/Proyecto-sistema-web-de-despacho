#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Esperando a PostgreSQL..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL iniciado correctamente :D"
fi

echo "Migrando..."
python manage.py migrate

exec "$@"