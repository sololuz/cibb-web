#!/bin/bash

APP_NAME="{{ project_name }}"                                         # Application Name

PROJECT_PATH=/home/victor/Proyectos/python/{{ project_name }}         # Project path
PROJECT_DJANGO=$PROJECT_PATH/app
PYTHON_ENV=$PROJECT_PATH/env                           # Virtual environment path

SOCKET_PATH=/tmp                                       # Root socket path
SOCKET_FILE=$SOCKET_PATH/{{ project_name }}.socket                    # Socket file path


USER=victor                                            # Application user
GROUP=victor
NUM_WORKERS=3                                          # workers CPUs*2+1

DJANGO_SETTINGS_MODULE=settings.production             # Settings to production mode
DJANGO_WSGI_MODULE=wsgi                                # WSGI Module
BIND=unix:$SOCKET_FILE                                 # Socket to binding

echo "Starting $NAME as `whoami`"


cd $PROJECT_PATH
source env/bin/activate
cd $PROJECT_DJANGO

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$PROJECT_DJANGO:$PYTHONPATH

# Crea el directorio para el socket si no existe
test -d $SOCKET_PATH || mkdir -p $SOCKET_PATH

# Ejecuta la aplicación Django
# Los programas que se ejecutaran bajo **supervisor** no deben demonizarse a si mismas (no usar --daemon)
exec $PYTHON_ENV/bin/gunicorn wsgi:application \
  --name=$APP_NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=$BIND \
  --log-file=-
  # --log-level=debug \
