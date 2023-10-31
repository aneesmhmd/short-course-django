from django.db import models

# Create your models here.
class Courses(models.Model):
    title = models.CharField(max_length=50, unique=True)
    subtitle = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='courses')
    description = models.TextField()
    is_available = models.BooleanField(default=False)
    amounts = models.ManyToManyField("Amount")

    def __str__(self):
        return self.title

class Amount(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    text = models.TextField()

    def __str__(self):
        return str(self.value)