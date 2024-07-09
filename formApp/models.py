from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User=get_user_model()

# Create your models here.
class form(models.Model):
    name = models.CharField(max_length=200)
    owner =  models.ForeignKey(User , on_delete=models.CASCADE)

class question(models.Model):
    form = models.ForeignKey(form , on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    type = models.CharField(max_length=20 , choices=(('Text','Text'),('Option','Option')))
    option1 = models.CharField(max_length=200 , blank=True)
    option2 = models.CharField(max_length=200 , blank=True)
    option3 = models.CharField(max_length=200 , blank=True)
    option4 = models.CharField(max_length=200 , blank=True)
    question_number = models.IntegerField()

class Respons(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    question = models.ForeignKey(question , on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

