from django.db import models
from .user import User

class Spinner(models.Model):
    primary_user = models.ForeignKey(User, on_delete=models.CASCADE)
    secondary_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secondary_user')
