from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

import uuid

def generate_uid():
    return uuid.uuid4().hex[:16]

class User(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=255, default=generate_uid)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.name
