from django.db import models

# Create your models here.


class ExpenditureModel(models.Model):

    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    value = models.IntegerField()
    date_added = models.DateField()


class IncomeModel(models.Model):

    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    value = models.IntegerField()
    date_added = models.DateField()
    is_periodical = models.BooleanField()
