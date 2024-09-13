from django.db import models
from .user import User

class Spinner(models.Model):
    primary_user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid', related_name='primary_spinners')
    secondary_user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid', related_name='secondary_spinners')


    class Meta:
        unique_together = ('primary_user', 'secondary_user')
