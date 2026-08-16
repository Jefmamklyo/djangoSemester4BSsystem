from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import constraints


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = test() #please fix this code 

    #human readable name in sql queries
    def __str__(self):
        return self.email

class userAcount(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class meta:
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte=0), name="balance_gte_0")
        ]



#Create your models here.

