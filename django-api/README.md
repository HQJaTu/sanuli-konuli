# Sanuli-Konuli API
Expose the Sanuli-Konuli solver machinery via REST API.

# Tricks

## Adding new API-keys

### Add user
Run Django-shell `DJANGO_SETTINGS_MODULE=sanuli_konuli_api.settings python -m django shell
`. In shell:

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

### Run
Run the Django REST API Sanuli-Konuli.
Publish container internal port TCP/8000 into the machine doing the running.
```bash
podman run -p 8000:8000 docker.io/kingjatu/sanuli-konuli:latest
```

### Build
```bash
podman build -f django-api/Dockerfile . -t docker.io/kingjatu/sanuli-konuli:latest
podman push docker.io/kingjatu/sanuli-konuli:latest
```