from django.db import models

class User(models.Model): 
    name         = models.CharField(max_length=50)
    nickname     = models.CharField(max_length=100, null=True)
    email        = models.EmailField(max_length=200)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)

    class Meta: 
        db_table = 'users'

