from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=15)
    desc = models.TextField(default='')

    def __str__(self):
        return self.name



