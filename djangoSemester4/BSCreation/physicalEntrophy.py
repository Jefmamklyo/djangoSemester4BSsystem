import base64
import hashlib
import os
from abc import abstractmethod

import cv2 as cv

#Camera Manager (sessions managing include later)
class CamManager():
    def __enter__(self):
        self.cam = cv.VideoCapture(0)
        return self.cam

    def __exit__(self, exc_type, exc, tb):
        self.cam.release()
        return False

#abstract (VIRTUAL) Methods for overiding later
class EnrophySource:
    @abstractmethod
    def gatherSource(self):
        pass

#random source of entrophy one
class OSRandSource(EnrophySource):
    def gatherSource(self):
        return os.urandom(32) 



#Camera Source (ENTRPHY SOURCE 2)
class CamSource(EnrophySource):
    def gatherSource(self):
        with CamManager() as cam:
            #read a set amount of frames
            ret1, frame1 = cam.read()
            ret2, frame2 = cam.read()

            #null chaining
            if ret1 and ret2:
                absDifference = cv.absdiff(frame2, frame1)

            #bufer to byte encoding
            _, buffer = cv.imencode('.jpg', absDifference)
            return buffer.tobytes()
            

            
#Key deriivitive

def deriveKey(sources):
    pool = bytearray() #byte array instantiation for zeriong
    for s in sources:
        pool.extend(s.gatherSource())

    hashedPool = hashlib.sha256(memoryview(pool)).digest() #hash retunr values 

    pool[:] = bytes(len(pool)) #zeriong process
    return base64.urlsafe_b64encode(hashedPool)