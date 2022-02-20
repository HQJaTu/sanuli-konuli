FROM python:3.9

COPY setup.py sanuli-konuli/
COPY cli-utils sanuli-konuli/cli-utils/
COPY lib_sanulikonuli sanuli-konuli/lib_sanulikonuli/
COPY django-api sanuli-konuli/django-api/
RUN pip install sanuli-konuli/ ; pip install -r sanuli-konuli/django-api/requirements.txt
# Clean-up
RUN cd sanuli-konuli/ ; rm -f setup.py ; cd django-api/ ; rm -f Dockerfile README.md manage.py requirements.txt config*.env ; find . -name .DS_Store -or -name "*.iml" -delete

# Create slots for missing files and directories with permissions for www-data to write into
RUN touch sanuli-konuli/django-api/db.sqlite3 sanuli-konuli/django-api/config.env ; \
    mkdir sanuli-konuli/django-api/words ; \
    chown www-data sanuli-konuli/django-api/db.sqlite3 sanuli-konuli/django-api/config.env sanuli-konuli/django-api/words

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