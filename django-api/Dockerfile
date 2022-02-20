FROM python:3.9

COPY setup.py sanuli-konuli/
COPY cli-utils sanuli-konuli/cli-utils/
COPY lib_sanulikonuli sanuli-konuli/lib_sanulikonuli/
COPY django-api sanuli-konuli/django-api/
RUN pip install sanuli-konuli/ ; pip install -r sanuli-konuli/django-api/requirements.txt
RUN cd sanuli-konuli/ ; rm -f setup.py ; cd django-api/ ; rm -f Dockerfile README.md manage.py requirements.txt ; find . -name .DS_Store -or -name "*.iml" -delete

COPY words/*.dat sanuli-konuli/django-api/words/
COPY django-api/db.sqlite3 sanuli-konuli/django-api/db.sqlite3
RUN echo "DICTIONARIES=fi:5:words/kotus-sanalista-5-words_v1.dat,fi:6:words/kotus-sanalista-6-words_v1.dat,en:5:words/nltk-wordnet2021-5-words_v1.dat" > sanuli-konuli/django-api/config_dev.env

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000

# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Security: Non-root execution of gunicorn
USER www-data

# Run the web service on container startup. Here we use the gunicorn webserver
ENTRYPOINT [ "gunicorn", "--chdir", "sanuli-konuli/django-api/", "--config", \
            "sanuli-konuli/django-api/sanuli_konuli_api/gunicorn_config.py", \
            "sanuli_konuli_api.wsgi:application" \
            ]