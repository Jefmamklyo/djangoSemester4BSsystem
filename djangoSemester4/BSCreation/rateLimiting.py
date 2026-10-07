##-------------------------------#
#######RATE LIMITING Models#######
#--------------------------------#


from django.db import models
from django.contrib.auth import get_user_model

#user refernece
User = get_user_model()
class RateLimiterModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'createdAt'])
        ]

#---------------------------------#
########RATE LIMITING LOGIC########
#---------------------------------#

from datetime import timedelta
from django.utils import timezone
from dataclasses import dataclass



@dataclass(slots = True)
class SlidingWindowRateLimiter:
    limit: int
    windowSeconds: int
    
    #sliding windwo logic for request
    def allowRequest(self):
        now = timezone.now()

        #define cutoff between secodns
        cutoff = now- timedelta(seconds=self.windowSeconds)

        #get user from request
        count = RateLimiterModel.objects.filter(user=user, createdAt__gte = cutoff).count()

        #filter count based on limit
        if count >= self.limit:
            return False #process return value
        RateLimiterModel.objects.create(user=user)
        return True
