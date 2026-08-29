from pydoc import plain
import secrets

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from .crypt import hashLookups, encrypt, decrypt

#base user manager modelobject
class UserManagerModel(BaseUserManager):
    def create_user(self, username, password = None):
        #never save a user without a valid username  ||||| Please accesses later to display using django.messages
        #Delete once you display with messages
        if not username:
            raise ValueError("User must have a valid username")

        user= self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


#custom perpmision user obejct
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)


    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManagerModel() #Linking usermanagermodel

    #human readable name in sql queries
    def __str__(self):
        return self.username


#user account manager
class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    encryptedBalance = models.CharField(max_length=255)
    encryptedAccountID= models.CharField(max_length=255)
    accountLookup = models.CharField(max_length=64, unique=True)

    
    def save(self, *args, **kwargs):
        #For cryptographycalyl saved account ID's
        plainNumber = secrets.token_hex(8)
        self.encryptedAccountID = encrypt(plainNumber)
        self.accountLookup = hashLookups(plainNumber)

        if not self.encryptedBalance:
            self.encryptedBalance = encrypt("0.00")



        super().save(*args, **kwargs)

    @property #getter
    def balance(self):
        return 

    @balance.setter
    def balance(self):
        pass

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(balance__gte=0), name="balance_gte_0")
        ]



