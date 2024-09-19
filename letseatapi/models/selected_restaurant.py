from django.db import models
from .restaurant import Restaurant
from .spinner import Spinner
from .user import User

class SelectedRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
