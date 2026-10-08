

#---------------------------------#
########RATE LIMITING LOGIC########
#---------------------------------#

from datetime import timedelta
import time
from django.utils import timezone
from dataclasses import dataclass
from merkleTree.models import RateLimiterModel


@dataclass(slots = True)
class SlidingWindowRateLimiter:
    limit: int
    windowSeconds: int
    
    #sliding windwo logic for request
    def allowRequest(self, user):
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

    def retryAfter(self, user):
        now = timezone.now()
        cutoff = now - timedelta(seconds=self.windowSeconds)

        #get and process oldest request to wait for it to expire
        oldestRequest = RateLimiterModel.objects.filter(user=user, createdAt__gte=cutoff).order_by('createdAt').first()
        if oldestRequest == None:
            return 0
        expireTime = oldestRequest.createdAt + timedelta(seconds = self.windowSeconds)
        return max(0,(expireTime-now).total_seconds())