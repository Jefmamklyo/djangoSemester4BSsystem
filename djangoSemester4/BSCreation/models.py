from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import constraints


#base user manager modelobject
class UserManagerModel(BaseUserManager):
    def create_user(self, username, password = None):
        #never save a user without a valid username  ||||| Please accesses later to display using django.messages
        if not username:
            raise ValueError("User must have a valid username")

        user= self.model(username=username)
        user.set_password(password)
        user.save()
        return user


#custom perpmision user obejct
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManagerModel() #Linking usermanagermodel

    #human readable name in sql queries
    def __str__(self):
        return self.email


#user account manager
class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class meta:
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte=0), name="balance_gte_0")
        ]





#Create your models here.

