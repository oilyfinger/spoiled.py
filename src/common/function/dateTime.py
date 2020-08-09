# dateTime.py
# Simple tool functions for datetime converting
#

from ..base.string import *

import datetime

def afterDays(dateBegin, nDays):
	return dateBegin + datetime.timedelta(days=nDays)

def untilDaysEnd(dateBegin, nDays):
	return dateBegin + datetime.timedelta(days=nDays, hours=23, minutes=59, seconds=59)

def	untilDaysToStr(dateBegin, nDays):
	return periodToStr(dateBegin, untilDaysEnd(dateBegin, nDays))

def minDate():
	return datetime.datetime(1900, 1, 1)

def maxDate():
	return datetime.datetime(2079, 6, 6)

def maxDateTime():
	return datetime.datetime(2079, 6, 6, 23, 59, 59)
