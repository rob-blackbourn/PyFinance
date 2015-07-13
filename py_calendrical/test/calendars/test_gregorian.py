'''
Created on 13 Jul 2015

@author: blackrob
'''
import unittest
from py_calendrical.calendars.gregorian import GregorianDate


class TestGregorian(unittest.TestCase):


    def testName(self):
        x = GregorianDate(1967, 8, 12)
        print x


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()