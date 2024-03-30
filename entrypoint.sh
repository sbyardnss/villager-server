#!/bin/sh

python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

gunicorn villager_chess.wsgi:application --bind 0.0.0.0:8000 
#CHECK

#if i wanted to add logging:
# YOU WOULD ADD SOMETHING LIKE THIS IN THIS FILE
# # Set the Django settings module
# export DJANGO_SETTINGS_MODULE=villager_chess.settings

# # Collect static files
# python3 manage.py collectstatic --no-input

# # Start Gunicorn
# exec gunicorn villager_chess.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-level=info


# YOU WOULD ADD SOMETHING LIKE THIS IN YOUR settings.py FOR DJANGO LOGGING:
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/path/to/your/django/logfile.log', PATH THAT YOU WANT THE FILES TO GO TO
#         },
#     },
#     'root': {
#         'handlers': ['file'],
#         'level': 'DEBUG',
#     },
# }


# YOU WOULD ADD SOMETHING LIKE THIS TO YOUR gunicorn.conf.py FOR GUNICORN LOGGING
# accesslog = "/var/log/gunicorn/access.log"
# errorlog = "/var/log/gunicorn/error.log"

# YOU WOULD ADD SOMETHING LIKE THIS TO YOUR nginx.conf FOR NGINX LOGGING
# access_log /var/log/nginx/access.log;
# error_log /var/log/nginx/error.log;