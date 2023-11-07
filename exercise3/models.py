from django.db import models

class KeyValue(models.Model):
    key = models.CharField(max_length=200, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key
