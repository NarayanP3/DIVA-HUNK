from django.db import models

# Create your models here.
class Diva(models.Model):
    name = models.CharField(max_length = 100, blank = True)
    image = models.ImageField(upload_to='images/', default='user.png')
    image1 = models.ImageField(upload_to='images/', default='user.png')
    image2 = models.ImageField(upload_to='images/', default='user.png')
    college = models.CharField(max_length=100, default="", blank = True)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class Hunk(models.Model):
    name = models.CharField(max_length = 100, blank = True)
    image = models.ImageField(upload_to='images/', default='user.png')
    image1 = models.ImageField(upload_to='images/', default='user.png')
    image2 = models.ImageField(upload_to='images/', default='user.png')
    college = models.CharField(max_length=100, default="", blank = True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Voter(models.Model):
    name =  models.CharField(max_length = 100, blank = True)
    contact = models.CharField(max_length = 14, blank = True)
    email = models.EmailField(blank=True)
    otp_timestamp = models.DateTimeField(null=True, blank=True)
    otp =  models.CharField(max_length = 6, blank = True, null = True)
    diva = models.ForeignKey(Diva, on_delete = models.CASCADE, blank = True, null=True)
    hunk = models.ForeignKey(Hunk, on_delete = models.CASCADE, blank = True, null=True)

    def __str__(self):
        return self.name

