from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):


    ROLE_CHOICES = (
        ('user', 'Utilisateur'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='Rôle')
