# debug.py
# Simple debug tool functions
#

from .printer import *

error = Printer(prefix="Error\t", file=sys.stderr)
warning = Printer(prefix="Warning\t", file=sys.stderr)
mute = MutePrinter()
	
def isSafe():
	return not error.dirty()

def isAssert():
	return error.dirty()

def safeCall(function, *args, expected=None):
	"""
		printer 모듈 응용을 위한 보조 함수
		- 기존 오류가 없는 경우에만 함수를 호출
		- 반환된 값이 무시 값이 아닌 경우 오류로 출력
	"""
	global error
	result = None
	if not error.dirty():
		result = function(*args)
	if result is not expected:
		error.print(result)

def safeReturn(newValue, safeValue):
	"""
		printer 모듈 응용을 위한 보조 함수
		- 기존 오류가 없는 경우에만 새로운 값을 반환
		- 오류가 있다면 안전한 값을 반환
	"""
	if not error.dirty():
		return newValue
	else:
		return safeValue

def assertCall(function, *args):
	"""
		printer 모듈 응용을 위한 보조 함수
		- 기존 오류가 있는 경우에만 함수를 호출
	"""
	global error
	if error.dirty():
		function(*args)

def assertReturn(newValue, assertValue):
	"""
		printer 모듈 응용을 위한 보조 함수
		- 기존 오류가 있는 경우에만 새로운 값을 반환
		- 오류가 없다면 표명 값을 반환
	"""
	if error.dirty():
		return newValue
	else:
		return assertValue
