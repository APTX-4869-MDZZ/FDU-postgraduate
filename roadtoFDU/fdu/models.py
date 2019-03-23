from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50, null=True)
    openid = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100)

    def __str__(self):
        return self.name