# Sanuli-Konuli API
Expose the Sanuli-Konuli solver machinery via REST API.

# Tricks

## Adding new API-keys

### Add user
Run Django-shell `DJANGO_SETTINGS_MODULE=sanuli_konuli_api.settings python -m django shell
`.

In shell:
```python
import django.contrib.auth
User = django.contrib.auth.get_user_model()
user = User.objects.create_user('sanuli', password='')
user.is_superuser = False
user.is_staff = False
user.save()
exit()
```

### Add API-key to newly created user

Assign an API-key by running `./manage.py drf_create_token sanuli`,
results:
```bash
Reading config from sanuli-konuli/django-api/config_dev.env
Generated token -yes-a-very-secret-key-will-be-here- for user sanuli
```

## Container operations
Somebody would call this Docker, but this implementation is not bound to
Docker, Inc. nor any of their technologies. Any container mechanism should
do the trick.

See: https://hub.docker.com/repository/docker/kingjatu/sanuli-konuli for ready-baked image.

### Create your own container with SQlite
(this will be done automatically)
```bash
podman pull docker.io/kingjatu/sanuli-konuli:latest
```

With your SQlite and dictionaries, run:
```bash
podman build -f django-api/local-Dockerfile .
```


### Run your image
Run the Django REST API Sanuli-Konuli.

#### Example 1:
Publish container Django internal port TCP/8000 into the machine doing the running.
```bash
podman run -p 8000:8000 <your-own-image-ID-here>
```

#### Example 2:
Publish container Django internal port TCP/8000 into the machine doing the running
as port TCP/8080.
```bash
podman run -p 8080:8000 <your-own-image-ID-here>
```

### Build the base image
Note: This image is missing dictionaries and SQlite-database with user and API-key,
thus making it unusable as-is.
```bash
podman build -f django-api/Dockerfile . -t docker.io/kingjatu/sanuli-konuli:latest
podman push docker.io/kingjatu/sanuli-konuli:latest
```

Django database SQlite file: `/sanuli-konuli/django-api/db.sqlite3`
Django configuration file: `/sanuli-konuli/django-api/config.env`
Sanuli-Konuli dictionaries directory: `/sanuli-konuli/django-api/words/`

Those slots need to be filled in your own container.