from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from ticket.models import Ticket


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
