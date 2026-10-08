

#---------------------------------#
########RATE LIMITING LOGIC########
#---------------------------------#

from datetime import timedelta
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
