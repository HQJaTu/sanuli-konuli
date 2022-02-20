# Sanuli-Konuli API
tbd

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