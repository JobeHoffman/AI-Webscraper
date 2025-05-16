from django.db import models

# Create your models here.
class testMigration(models.Model):
    var1 = models.CharField()
    var2 = models.IntegerField()