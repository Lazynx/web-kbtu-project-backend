from django.db import models

class Tour(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stars = models.IntegerField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='tours/', blank=True, null=True) 

    def __str__(self):
        return self.name