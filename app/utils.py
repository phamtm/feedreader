from random import choice
from string import ascii_letters

from threading import *
import copy
from math import sqrt


class Future:

    def __init__(self,func,*param):
        # Constructor
        self.__done=0
        self.__result=None
        self.__status='working'

        self.__C=Condition()   # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__T=Thread(target=self.Wrapper,args=(func,param))
        self.__T.setName("FutureThread")
        self.__T.start()

    def __repr__(self):
        return '<Future at '+hex(id(self))+':'+self.__status+'>'

    def __call__(self):
        self.__C.acquire()
        while self.__done==0:
            self.__C.wait()
        self.__C.release()
        # We deepcopy __result to prevent accidental tampering with it.
        a=copy.deepcopy(self.__result)
        return a

    def Wrapper(self, func, param):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result=func(*param)
        except:
            self.__result="Exception raised within Future"
        self.__done=1
        self.__status=`self.__result`
        self.__C.notify()
        self.__C.release()


def generate_random_string(length):
	return ''.join([choice(ascii_letters) for i in range(length)])


def wilson_score(pos_ratings, num_ratings):
    """
    Return the lower bound of Wilson score confidence
    interval for a Bernoulli parameter.

    Useful for rating system with only positive and negative votes.
    Not applicable to star-rating system.

    Reference
        http://evanmiller.org/how-not-to-sort-by-average-rating.html
    """
    if num_ratings == 0:
        return 0

    z = 1.96    # confidence level 95%

    p = pos_ratings * 1.0 / num_ratings
    score = (p + z**2 / (2 * num_ratings) - z * sqrt((p * (1 - p) + z**2 / (4 * num_ratings))) / num_ratings) / (1 + z**2 / num_ratings)
    return score

