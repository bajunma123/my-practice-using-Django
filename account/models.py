from django.db import models

# Create your models here.

class Account(models.Model):
    website = models.URLField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return '{} : {} : {}'.format(self.website, self.username, self.email)
