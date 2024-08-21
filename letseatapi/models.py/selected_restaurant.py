from django.db import models
from .restaurant import Restaurant
from .spinner import Spinner

class SelectedRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    spinner = models.ForeignKey(Spinner, on_delete=models.CASCADE)
