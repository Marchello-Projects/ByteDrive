import os
from dotenv import load_dotenv
from django.apps import AppConfig
from django.db.models.signals import post_migrate

load_dotenv()

class DriveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drive'

    def ready(self):
        import drive.signals
        post_migrate.connect(create_default_superuser, sender=self)

def create_default_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    ADMIN_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
    ADMIN_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
    ADMIN_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        print(f"Creating superuser: {ADMIN_USERNAME}...")
        try:
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            print("Superuser created successfully!")
        except Exception as e:
            print(f"Error creating superuser: {e}")
    else:
        print("Superuser already exists. Skipping creation")