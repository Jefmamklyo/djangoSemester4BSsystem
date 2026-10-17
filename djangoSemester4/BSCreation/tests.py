

import unittest

import django
from django.test import TestCase, TransactionTestCase
from .models import User

from .rateLimiting import SlidingWindowRateLimiter
from merkleTree.models import RateLimiterModel


from datetime import timedelta  
from django.utils import timezone
from unittest.mock import patch

from functools import wraps
def testLogger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f" Finished executing {func.__name__}")
        print(result)
        return result
    return wrapper



class RateLimiterBehaviorTest(TestCase):
   #Setup
   def setUp(self):
       self.user = User.objects.create_user(username="testuser", password="testpassword")
       self.limiter = SlidingWindowRateLimiter(limit=5, windowSeconds=60)
       self.start = timezone.now()  

   #TimeHelper
   def timeHelper(self, seconds):
       patcher = patch('django.utils.timezone.now', return_value=self.start + timedelta(seconds=seconds))
       return patcher

   #request helper
   def requestHelper(self, seconds):
       with self.timeHelper(seconds):
           return self.limiter.allowRequest(self.user)

   @testLogger
   #Window burst
   def testWindowBurst(self):
       for i in range(5):
           self.requestHelper(59) #5 requeststins withing a second window
       hits = []
       expectedCases = [False, False, False, False, False]
       for i in range(5):
           hits.append(self.requestHelper(61)) #5 requests after window has expired
       self.assertEqual(hits, expectedCases)
    
   @testLogger
   #Windwo edge case
   def testWindowEdgeCase(self):
       for i in range(5):
           self.requestHelper(0)
       expectedCases = [(1,False), (59,False), (60,True), (61,True)] #test all cases (lower, edge, upper, beyond)
       for time, expected in expectedCases:
           with self.subTest(seconds=time):
                self.assertEqual(self.requestHelper(time), expected)
        

   #Blocked attaemts aren't commited to database
   @testLogger
   def testCheckBlockedDatabaseCommits(self):
       for i in range(10):
           self.requestHelper(1)
        #check only 5 enter database from ratelimitermodel specfiically
       self.assertEqual(RateLimiterModel.objects.filter(user=self.user).count(),5)

   #retryAfter functionality
   @testLogger
   def testRetryAfterWorksSuccesfully(self):
       for i in range(5):
           self.requestHelper(0)
       with self.timeHelper(1):
           retryAfter = self.limiter.retryAfter(self.user)

       self.assertFalse(self.requestHelper(retryAfter)) #Falase after the time frame
       self.assertTrue(self.requestHelper(1+ retryAfter)) #False before the time frame

   #Pruning removes only expireed rows
   @testLogger
   def testCheckPruningDeletsOnlyExpiredRows(self):
       self.requestHelper(0)
       self.requestHelper(30)
       self.requestHelper(70)

       #sort the requests by time crated -> asseretEqual time only 50 and 70 are kept
       createdTime = []
       for request in RateLimiterModel.objects.filter(user=self.user).order_by('createdAt'):
            createdTime.append( (request.createdAt -self.start).total_seconds())
       self.assertEqual(createdTime, [30,70])

   #blockedRequestsDeletion???





import threading
from concurrent.futures import ThreadPoolExecutor, thread
from django.db import connection

class SlidingWindowConcurrencyTest(TransactionTestCase):
    TestInstances = 10
    
    def deterministicThreadCreation(self, user):
        limiter = SlidingWindowRateLimiter(limit=5, windowSeconds=60)
        barrier = threading.Barrier(self.TestInstances)



        #closure
        def threadFunction(threadIndex):
            try:
                barrier.wait()
                return limiter.allowRequest(user)
            finally:
                connection.close() 

        with ThreadPoolExecutor(max_workers=self.TestInstances) as TPE:
            return sum(TPE.map(threadFunction, range(self.TestInstances)))


    def testConcurrency(self):
        for  i in range(10):
            user = User.objects.create_user(username=f"testuser{i}", password="testpassword")
            self.assertEqual(self.deterministicThreadCreation(user),5) #only 5 requests should be allowed
