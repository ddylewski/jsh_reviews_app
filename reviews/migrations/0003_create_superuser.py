from django.db import migrations
import os

def create_or_update_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not (username and email and password):
        return

    try:
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
    except User.DoesNotExist:
        User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_populate_specialties'),
    ]

    operations = [
        migrations.RunPython(create_or_update_superuser),
    ]