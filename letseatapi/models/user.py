from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

def generate_uid():
    return uuid.uuid4().hex[:16]

class User(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=255, primary_key=True, unique=True, default=generate_uid)
    password = models.CharField(max_length=128)
    user_name = models.CharField(max_length=50, unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.CharField(max_length=1000, null=True, blank=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.name
