

#---------------------------------#
########RATE LIMITING LOGIC########
#---------------------------------#

from datetime import timedelta
import time
from django.utils import timezone
from dataclasses import dataclass
from merkleTree.models import RateLimiterModel
from django.db import transaction 
import math as maths


from django.contrib.auth import get_user_model

User = get_user_model()



@dataclass(slots = True)
class SlidingWindowRateLimiter:
    limit: int
    windowSeconds: int
    
    #sliding windwo logic for request
    def allowRequest(self, user):
        with transaction.atomic():
            #make atomic to fix concurrency
            User.objects.select_for_update().get(pk=user.pk)

            now = timezone.now()

            #define cutoff between secodns
            cutoff = now- timedelta(seconds=self.windowSeconds)

            #deelte older request (PRUNING)
            RateLimiterModel.objects.filter(user=user, createdAt__lte=cutoff).delete()  

            #count the amount of requests in a window
            #ADDED A FIX FOR ENTRY EXPIRY EDGECASE
            count = RateLimiterModel.objects.filter(user=user, createdAt__gte = cutoff).count()
            if count >= self.limit:
                return False 


            RateLimiterModel.objects.create(user=user)
            return True

    def retryAfter(self, user):
        now = timezone.now()    
        cutoff = now - timedelta(seconds=self.windowSeconds)

        #get and process oldest request to wait for it to expire
        oldestRequest = RateLimiterModel.objects.filter(user=user, createdAt__gte=cutoff).order_by('createdAt').first()
        
        expireTime = oldestRequest.createdAt + timedelta(seconds = self.windowSeconds)  

        seconds = (expireTime-now).total_seconds()

        return max(1,seconds)