import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sgm.settings" )

import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.create_superuser(
    username="admin",
    email="diogotadeub@gmail.com",
    password="Bud@0mestre"
)
