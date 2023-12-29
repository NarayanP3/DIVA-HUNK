from django.db import models

class Voter(models.Model):
    name =  models.CharField(max_length = 100, blank = True)
    contact = models.CharField(max_length = 10, blank = True)
    email = models.EmailField(blank=True)
    otp =  models.CharField(max_length = 6, blank = True, null = True)

    def __str__(self):
        return self.name
# Create your models here.
