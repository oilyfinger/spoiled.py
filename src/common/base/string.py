# string.py
# Simple string tool functions
#

from .debug import *

from datetime import date as SmallDate
from datetime import time as SmallTime
from datetime import datetime as SmallDateTime

kIgnoreCharacters = (None, "None", "none", "null", "nil", "n/a", "-", "")

def getAlt(org, alt):
	if org not in kIgnoreCharacters:
		return org
	return alt

# STR ----> INT	
def strToInt(value, defaultValue=None, level=error):
	result = defaultValue
	try:
		result = int(value)
	except:
		level.print("정수 변환에 실패했습니다")
	return result

# STR ----> FLOAT
def strToFloat(value, defaultValue=None, level=error):
	result = defaultValue
	try:
		result = float(value)
	except:
		level.print("실수 변환에 실패했습니다")
	return result

def isTrue(value):
	if value is True or value == 1:
		return True
	elif type(value) is str:
		return value.lower() == "true"
	return False

def isFalse(value):
	if value is False or value == 0:
		return True
	elif type(value) is str:
		return value.lower() == "false"
	return False

# STR <---> BOOL
def strToBool(value, defaultValue=None, level=error):
	if isTrue(value):
		return True
	elif isFalse(value):
		return False
	else:
		return defaultValue
def boolToStr(value, defaultValue=None, level=error):
	if value is True:
		return "true"
	elif value is False:
		return "false"
	else:
		return defaultValue

# STR <---> DATE
def strToDate(value, defaultValue=None, level=error, strfmt="%Y-%m-%d"):
	result = defaultValue
	try:
		result = SmallDateTime.strptime(value, strfmt)
	except:
		level.print("날짜 변환에 실패했습니다 (형식: %s)" % strfmt)
	return result
def dateToStr(value, defaultValue=None, level=error, strfmt="%Y-%m-%d"):
	result = defaultValue
	try:
		result = SmallDateTime.strftime(value, strfmt)
	except:
		level.print("날짜 변환에 실패했습니다 (형식: %s)" % strfmt)
	return result

# STR <---> TIME
def strToTime(value, defaultValue=None, level=error, strfmt="%H:%M:%S"):
	result = defaultValue
	try:
		result = SmallDateTime.strptime(value, strfmt)
	except:
		level.print("시간 변환에 실패했습니다 (형식: %s)" % strfmt)
	return result
def timeToStr(value, defaultValue=None, level=error, strfmt="%H:%M:%S"):
	result = defaultValue
	try:
		result = SmallDateTime.strftime(value, strfmt)
	except:
		level.print("시간 변환에 실패했습니다 (형식: %s)" % strfmt)
	return result

# STR <---> DATETIME
def strToDateTime(value, defaultValue=None, level=error, strfmt="%Y-%m-%dT%H:%M:%S"):
	result = defaultValue
	try:
		result = SmallDateTime.strptime(value, strfmt)
	except:
		level.print("일시 변환에 실패했습니다 (형식: %s)" % strfmt)
	return result
def dateTimeToStr(value, defaultValue=None, level=error, strfmt="%Y-%m-%dT%H:%M:%S"):
	result = defaultValue
	try:
		result = SmallDateTime.strftime(value, strfmt)
	except:
		level.print("일시 변환에 실패했습니다 (형식: %s)" % strfmt)
	return result

# STR <---> PERIOD
def strToPeriod(value, defaultValue=None, level=error, strfmt="%Y-%m-%dT%H:%M:%S", tilde="~"):
	result = defaultValue
	try:
		period = value.split(tilde)
		dateTimeFrom = SmallDateTime.strptime(period[0].strip(), strfmt)
		dateTimeTo = SmallDateTime.strptime(period[1].strip(), strfmt)
		result = [dateTimeFrom, dateTimeTo]
	except:
		level.print("기간 변환에 실패했습니다 (형식: %s%s%s)" % (strfmt, tilde, strfmt))
	return result
def periodToStr(valueFrom, valueTo, defaultValue=None, level=error, strfmt="%Y-%m-%dT%H:%M:%S", tilde="~"):
	result = defaultValue
	try:
		strFrom = SmallDateTime.strftime(valueFrom, strfmt)
		strTo = SmallDateTime.strftime(valueTo, strfmt)
		result = strFrom + tilde + strTo
	except:
		level.print("기간 변환에 실패했습니다 (형식: %s%s%s)" % (strfmt, tilde, strfmt))
	return result

# STR ----> AVAILABLE VALUE
def strToValue(value, defaultValue, level=error):
	defaultType = type(defaultValue)
	if defaultType is str:
		return value
	elif defaultType is int:
		return strToInt(value, defaultValue, level)
	elif defaultType is float:
		return strToFloat(value, defaultValue, level)
	elif defaultType is bool:
		return strToBool(value, defaultValue, level)
	elif defaultType is SmallDate:
		return strToDate(value, defaultValue, level)
	elif defaultType is SmallTime:
		return strToTime(value, defaultValue, level)
	elif defaultType is SmallDateTime:
		return strToDateTime(value, defaultValue, level)
	elif defaultType is tuple:
		if len(defaultValue) == 2:
			subType =\
			[
				type(defaultValue[0]),
				type(defaultValue[1])
			]
			if subType[0] is SmallDateTime and subType[1] is SmallDateTime:
				return strToPeriod(value, defaultValue, level)
	return defaultValue
