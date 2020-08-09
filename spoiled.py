# spoiled.py
# Spoiled Python Module
#

# printer.py
# Simple printer classes
#

import sys

class Printer:
	def __init__(self, prefix="", suffix="", file=sys.stdout):
		self.m_count = 0
		self.m_group = None
		self.m_prefix = str(prefix)
		self.m_suffix = str(suffix)
		self.m_file = file

	def print(self, *value, sep=" ", end="\n", flush=False):
		if self.m_group is not None:
			self.m_group.print()
		print(self.m_prefix, *value, self.m_suffix, sep=sep, end=end, file=self.m_file, flush=flush)
		self.m_count += 1

	def clear(self):
		self.leaveGroup()
		self.__init__(file=self.m_file)

	def dirty(self):
		return self.m_count != 0

	def makeGroup(self, name, prefix="", suffix=""):
		self.joinGroup(PrintGroup(name, prefix, suffix, self.m_file))

	def joinGroup(self, group):
		self.leaveGroup()
		self.m_group = group
		self.m_group.join()
	
	def leaveGroup(self):
		if self.m_group is not None:
			self.m_group.leave()

class MutePrinter(Printer):
	def print(self, *value, sep=" ", end="\n", flush=False):
		self.m_count += 1
		pass

class PrintGroup(Printer):
	def __init__(self, name, prefix="", suffix="", file=sys.stdout):
		Printer.__init__(self, prefix, suffix, file)
		self.m_name = str(name)
		self.m_ref = 0

	def print(self):
		if self.m_count == 0:
			if self.m_prefix != "":
				print(self.m_prefix, end="", file=self.m_file)
			print(self.m_name, file=self.m_file)
		self.m_count += 1

	def setName(self, name):
		self.m_name = name

	def join(self):
		self.m_ref += 1

	def leave(self):
		self.m_ref -= 1
		if self.m_ref == 0 and self.m_count != 0:
			if self.m_suffix != "":
				print(self.m_suffix, end="", file=self.m_file)
		elif self.m_ref < 0:
			self.m_ref = 0

# debug.py
# Simple debug tool functions
#

# from .printer import *

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

# string.py
# Simple string tool functions
#

# from .debug import *

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

# access.py
# Simple file tool functions
#

# from ..base import *
import copy

dictOpenMode =\
{
	"r": "Read",
	"rb": "Read Binary",
	"w": "Write",
	"wb": "Write Binary",
}

tupleBinaryMode = ("rb", "wb")

def fileAccess(fileName, mode, accessFunc, data=None, level=error, debug=False, openFunc=None, openArgs=[]):
	success = True
	file_ = None
	if debug:
		mean = getAlt(dictOpenMode.get(mode), "Open")
		print("Debug", mean, fileName)
		if openFunc is not None:
			file_ = openFunc(fileName, *openArgs)
		elif mode in tupleBinaryMode:
			file_ = open(fileName, mode)
		else:
			file_ = open(fileName, mode, encoding="utf-16")
		accessFunc(file_, data, level)
		file_.close()
	else:
		try:
			mean = getAlt(dictOpenMode.get(mode), "Open")
			print(mean, fileName)
			if openFunc is not None:
				file_ = openFunc(fileName, *openArgs)
			elif mode in tupleBinaryMode:
				file_ = open(fileName, mode)
			else:
				file_ = open(fileName, mode, encoding="utf-16")
			try:
				accessFunc(file_, data, level)
			except:
				level.print("Data Access Failed (%s)" % fileName)
		except:
			level.print("%s Failed (%s)" % (mean, fileName))
			success = False
		finally:
			if file_ is not None:
				file_.close()
	return success

def inRaw(file_, data, level=error, ):
	data.clear()
	reader = file_.readlines()
	for row in reader:
		data.append(row)
	return

def outRaw(file_, data, level=error):
	file_.write(data)
	return

# ext_csv.py
# Simple tool functions for csv files
#

# from ..base import *

import csv

def inCsv(file_, data, level=error, debug=False):
	data.clear()
	reader = csv.reader(file_, delimiter="\t")
	for row in reader:
		data.append(row)
	return

# ext_xlsx.py
# Simple tool functions for xlsx files
#

# from ..base import *

import openpyxl

def inXlsx(file_, data, level=error, debug=False):
	wb = file_
	for key in data.keys():
		print("Read worksheet %s" % key)
		ws = wb.get_sheet_by_name(key)
		data[key] = ReadOnlySheet(ws)
	return
#---------------------------------------------------------------------- Simplified Excel classes
class ReadOnlyCell:
	# openpyxl.cell.Cell 간략화
	def __init__(self, openpyxl_cell):
		self.coordinate = openpyxl_cell.coordinate
		self.value = safeCellValue(openpyxl_cell, level=mute)
		return

class ReadOnlySheet:
	# openpyxl.worksheet.Worksheet 간편화
	lastFounds = []
	def __init__(self, openpyxl_worksheet):
		def convertRows(rows, cols, cells):
			sameColList = {}
			for row in range(len(rows)):
				for col in range(len(rows[row])):
					col_idx = rows[row][col].col_idx
					# 변환
					rows[row][col] = ReadOnlyCell(rows[row][col])
					# cols 생성
					if sameColList.get(col_idx) is None:
						sameColList[col_idx] = [rows[row][col], ]
					else:
						sameColList[col_idx].append(rows[row][col])
					# cells 생성
					coord = rows[row][col].coordinate
					value = rows[row][col].value
					cells[coord] = value
			for mergedCol in sameColList.values():
				cols.append(mergedCol.copy())
			return
		self.mergedRows = []
		self.mergedCols = []
		self.mergedCells = {}
		self._regMergedRows(openpyxl_worksheet)
		convertRows(self.mergedRows, self.mergedCols, self.mergedCells)
		self.commonRows = []
		self.commonCols = []
		self.commonCells = {}
		self._regCommonRows(openpyxl_worksheet)
		convertRows(self.commonRows, self.commonCols, self.commonCells)
		return
	def _regMergedRows(self, openpyxl_worksheet):
		"""
			병합 셀을 보다 쉽게 다루기 위해 정렬하는 함수
			- 모든 병합 셀 시작 점을 잡아, 행 기준으로 정렬\n
			- e.g. [[A1, A3], [B4], [C2], [D1, D4]]\n
		"""
		ws = openpyxl_worksheet
		self.mergedRows.clear()

		# 워크시트에서 병합 셀 위치 추출
		# (e.g. J3, C1, A3, ...)
		unorderedList = []
		for cellRange in ws.merged_cell_ranges:
			# 시작점의 위치 만을 추출
			coord = list(openpyxl.utils.range_boundaries(cellRange)[0:2])
			# 내부는 col, row 로 되어있기에 리스트 반전
			# (e.g. 3J, 1C, 3A, ...)
			coord.reverse()
			unorderedList.append(coord)
		# 병합 셀 위치를 순차적으로 정렬
		# (e.g. 1A, 3C, 3J, ...)
		unorderedList.sort()

		# 같은 행 끼리 묶어줌
		previousRow = unorderedList[0][0]
		sameRowList = []
		orderedList = []
		for coord in unorderedList:
			# 행 번호가 이전과 다르면(=새로운 행이면),
			if coord[0] != previousRow:
				orderedList.append(sameRowList.copy())
				sameRowList.clear()
				previousRow = coord[0]
			sameRowList.append(coord.copy())
		orderedList.append(sameRowList.copy())

		# 위치로부터 셀 객체를 얻음
		# (e.g. cell[1C], cell[3A], cell[3J], ...)
		sameRowList.clear()
		for row in orderedList:
			for coord in row:
				sameRowList.append(ws[coord[0]][coord[1]-1])
			self.mergedRows.append(sameRowList.copy())
			sameRowList.clear()
		return
	def _regCommonRows(self, openpyxl_worksheet):
		"""
			일반 셀을 보다 쉽게 다루기 위해 정리하는 함수
			- 내용이 있는 셀만 포함되며, 병합 셀은 제외된다\n
		"""
		ws = openpyxl_worksheet
		self.commonRows.clear()
		
		# 정렬은 이미 되어있으므로, 값과 병합 셀의 유무 만을 확인
		orderedList = []
		for row in ws.iter_rows():
			for cell in row:
				if cell.value is not None:
					if cell.coordinate not in self.mergedCells.keys():
						orderedList.append(cell)
			if len(orderedList) != 0:
				self.commonRows.append(orderedList.copy())
			orderedList.clear()
		return
	def findInCommonRows(self, *args):
		return self._findIn(self.commonRows, *args)
	def findInCommonCols(self, *args):
		return self._findIn(self.commonCols, *args)
	def findInMergedRows(self, *args):
		return self._findIn(self.mergedRows, *args)
	def findInMergedCols(self, *args):
		return self._findIn(self.mergedCols, *args)
	def _findIn(self, cellLists, *args):
		"""
			정렬된 셀 리스트에서 특정 이름을 검색
			- 행/열 기준 검색
			- 행/열의 첫 번째 셀(태그)의 값 만을 검색
			- 같은 조건의 태그를 지닌 모든 행/열을 리스트로 반환
			- 매개변수 *args 를 통해, 1차 검색에 실패한 경우 n차 검색 시도 가능
		"""
		founds = []
		string = str(args[0])
		# 여러 속성의 일괄적 처리를 위해 리스트로 가져옴
		# [속성 명 #1] [ ... ]
		# [속성 명 #2] [ ... ]
		# [속성 명 #3] [ ... ]
		for cells in cellLists:
			if cells[0].value.find(string) != -1:
				founds.append(cells)
		ReadOnlySheet.lastFounds = founds

		if len(founds) == 0:
			if len(args) > 1:
				return self._findIn(cellLists, *(args[1:]))
		return founds
#------------------------------------------------------------------------ Tag finding tool class
class TagFinder:
	createdList = []
	targetSheet = None
	def __init__(self, *keywords):
		if TagFinder.targetSheet is not None:
			if keywords is not None:
				self.isDerived = False
				self.keywords = keywords
				self.cellList = TagFinder.targetSheet.findInMergedRows(*keywords)
				TagFinder.createdList.append(self)
		return
	def __eq__(self, other):
		return self.keywords == other.keywords
	def __ne__(self, other):
		return self.keywords != other.keywords
	def fillBlanks(level=warning):
		group = PrintGroup("-- 찾지 못한 행이 있어, 다른 행으로부터 재검색 합니다", file=sys.stderr)
		level.joinGroup(group)
		for finder in TagFinder.createdList:
			if len(finder.cellList) == 0:
				empty = finder
				# 자기 자신을 검색 대상에서 제외하기 위해 isDerived 사용
				empty.isDerived = True
				for other in TagFinder.createdList:
					empty._fillIn(other)
					if len(empty.cellList) != 0:
						level.print("'%s' 옆에서 '%s'을 찾았습니다" % (other.keywords, empty.keywords))
						break # 하나라도 있으면 break (전부 다시 찾으려면 비활성화)
				# end for
		# end for
		level.leaveGroup()
		return
	def _fillIn(self, other):
		if not other.isDerived and len(other.cellList) > 0 and other != self:
			for otherRow in other.cellList:
				if len(otherRow) > 2:
					# 키워드로 검색
					for keyword in self.keywords:
						if str(otherRow[2].value).find(keyword) != -1:
							v = otherRow.pop()
							k = otherRow.pop()
							self.cellList.append([k, v])
							break
				# end if
		# end if
		return
#---------------------------------------------------------------- Tool functions for excel cells
def safeCellValue(cell, level=warning):
	"""
		셀 객체로부터 값을 안전하게 얻기 위한 함수
		- 안전하지 않은 경우, 공백 문자열을 반환
	"""
	cellType = type(cell)
	if cellType is openpyxl.cell.Cell or cellType is ReadOnlyCell:
		noneSpaceString = str(cell.value).strip()
		if noneSpaceString not in kIgnoreCharacters:
			return noneSpaceString
		else:
			# level.print("셀 값이 존재하지 않습니다 (%s)" % cell.coordinate)
			pass
	else:
		level.print("셀이 아닌 객체를 호출하고 있습니다 (safeCellValue)")
	return ""

def safeCellValueAlter(cells, org, alt, level=warning):
	"""
		셀 객체로부터 값을 안전하게 얻기 위한 함수
		- 원본 데이터가 없는 경우, 대체 데이터를 사용
		- 둘 다 없는 경우, 공백 문자열을 반환
	"""
	valueOrg = safeCellValue(cells[org], level)
	valueAlt = safeCellValue(cells[alt], level)
	if valueOrg != "":
		return valueOrg
	elif valueAlt == "":
		# level.print("원본 셀과 참조 셀 모두 값이 없습니다 (%s, %s)" % (cells[org].coordinate, cells[alt].coordinate))
		pass
	return valueAlt

# ext_xml.py
# Simple tool functions for xml files
#

# from ..base import *

import	xml.etree.ElementTree	as ET
from	xml.etree.ElementTree	import Element
from	xml.dom					import minidom

def inXml(file_, wrapper, level=error, debug=False):
	wrapper.clear()
	root = ET.fromstring(file_.read().decode("utf-16"))
	wrapper.append(root)
	return
def outXml(file_, xel, level=error, debug=False):
	worst = minidom.parseString(ET.tostring(xel, encoding="utf-16")).toprettyxml(encoding="UTF-16")
	better = worst.decode(encoding="utf-16").replace('"', "'").replace("\n", "\r\n").encode("utf-16")
	file_.write(better)
	return

#------------------------------------------------------------------------------------- XmlObject
class XmlObject:
	def readFrom(self, xel):
		assert(0)
	def writeTo(self, xel):
		assert(0)
#---------------------------------------------------------------------- XmlObject tool functions
def getAttrValue(xel, name, defaultValue, level=warning):
	return _getAttrValue(xel, name, defaultValue, type(defaultValue), level)
def setAttrValue(xel, name, value, level=warning):
	return _setAttrValue(xel, name, value, type(value), level)
def attachChild(parent, child):
	pass
def detachChild(parent, child):
	pass
#------------------------------------------------------------------------- string tool functions
def appendIfExist(attr, value, end="\n"):
	# 여기서 value는 정제된 데이터이기에 strip 등을 사용하지 않는다
	if value not in kIgnoreCharacters:
		return "%s='%s'%s" % (attr, str(value), end)
	return ""
def appendIfEqual(attr, value, equal, end="\n"):
	# 여기서 value는 정제된 데이터이기에 strip 등을 사용하지 않는다
	if value == equal:
		return "%s='%s'%s" % (attr, str(value), end)
	return ""
	
def replaceEscape(string):
	# print("BEFORE %s" % string)
	string = string.replace("&", "&amp;")
	string = string.replace("<", "&lt;")
	string = string.replace(">", "&gt;")
	string = string.replace("'", "&apos;")
	string = string.replace('"', "&quot;")
	# print("AFTER %s" % string)
	return string
#------------------------------------------------------------------------------- local functions
def _getAttrValue(xel, name, defaultValue, valueType, level):
	if type(xel) is Element:
		value = xel.get(name)
		if value is None:
			# 값을 찾지 못한 경우
			return defaultValue
		else:
			# 값을 찾은 경우 변환
			if valueType is str:
				return value
			elif valueType is int:
				return strToInt(value, defaultValue, level)
			elif valueType is float:
				return strToFloat(value, defaultValue, level)
			elif valueType is bool:
				return strToBool(value, defaultValue, level)
		# 값 변환이 불가능한 경우
		level.print("허용되지 않은 타입 - getAttrValue%s" % str(valueType))
	else:
		level.print("잘못된 호출 - getAttrValue")
	return
def _setAttrValue(xel, name, value, valueType, level):
	if type(xel) is Element:
		if valueType is str:
			xel.set(name, value)
		elif valueType is int:
			xel.set(name, str(value))
		elif valueType is float:
			xel.set(name, str(value))
		elif valueType is bool:
			xel.set(name, boolToStr(value, defaultValue, level))
		else:
			# 값 변환이 불가능한 경우
			level.print("허용되지 않은 타입 - setAttrValue%s" % str(valueType))
	else:
		level.print("잘못된 호출 - setAttrValue")
	return

# dateTime.py
# Simple tool functions for datetime converting
#

# from ..base.string import *

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

# config.py
# For configuration management
#

# from ..base import *
# from ..file import *

import os
# import sys

# import	xml.etree.ElementTree	as ET
from	xml.etree.ElementTree	import SubElement

kDirName_defaultConfig = "ConfigDir"
kDirPath_defaultConfig = ".\\" + kDirName_defaultConfig + "\\"

kFileName_defaultConfig = "config.xml"
kFilePath_defaultConfig = ".\\" + kFileName_defaultConfig

class TargetDb(XmlObject):
	def __init__(self, dsn=None, catalog=None, user=None, password=None):
		self.dsn		= dsn
		self.catalog	= catalog
		self.user		= user
		self.password	= password
	def readFrom(self, xel):
		self.dsn		= getAttrValue(xel, "dsn", "")
		self.catalog	= getAttrValue(xel, "catalog", "")
		self.user		= getAttrValue(xel, "user", "")
		self.password	= getAttrValue(xel, "password", "")
		return self
	def writeTo(self, xel):
		SubElement(xel, "targetDb",\
		{
			"dsn":		self.dsn,
			"catalog":	self.catalog, 
			"user":		self.user,
			"password":	self.password
		})
	def isAvailable(self):
		if	self.dsn		in kIgnoreCharacters or\
			self.catalog	in kIgnoreCharacters or\
			self.user		in kIgnoreCharacters or\
			self.password	in kIgnoreCharacters:
			return False
		else:
			return True

class TargetDbSet(XmlObject, list):
	def readFrom(self, xel):
		if xel is not None:
			self.clear()
			for targetDbXel in xel.findall("targetDb"):
				targetDb = TargetDb().readFrom(targetDbXel)
				# attribute가 하나라도 없다면 넣지 않음
				if targetDb.isAvailable():
					self.append(targetDb)
		return
	def writeTo(self, xel):
		targetDbXel = SubElement(xel, "targetDbSet")
		for targetDb in self:
			if targetDb.isAvailable():
				targetDb.writeTo(targetDbXel)
		return 

class ConfigManager:
# INITIALIZER
	def __init__(self):
		self.m_targetDbSet = TargetDbSet()
		self.m_dirPath = kDirPath_defaultConfig
		self.m_input = dict()
		self.m_output = dict()
		return
# GETTER & SETTER
	def getDirPath(self):
		return self.m_dirPath
	def getIn(self, key):
		return self.m_input.get(key)
	def getOut(self, key):
		return self.m_output.get(key)
	def setDirPath(self, dirPath):
		self.m_dirPath = dirPath
		return
	def setIn(self, key, value):
		self.m_input[key] = value
		return
	def setOut(self, key, value):
		self.m_output[key] = value
		return
# FILE I/O (LOAD & SAVE)
	def load(self, dictIn=None, dictOut=None, debug=False, fileName=kFileName_defaultConfig):
		success = self._read(fileName, debug)
		def _readFrom(this, other):
			if type(other) is dict:
				for key in other.keys():
					other[key] = getAlt(this[key], other[key])
			return
		def _writeTo(this, other):
			if type(other) is dict:
				for key in other.keys():
					this[key] = other[key]
			return
		if success is True:
			_readFrom(self.m_input, dictIn)
			_readFrom(self.m_output, dictOut)
		else:
			self.m_dirPath = kDirPath_defaultConfig
			_writeTo(self.m_input, dictIn)
			_writeTo(self.m_output, dictOut)
			# self.sample()
			success = self.save(fileName, debug)
		return success
	def save(self, fileName=kFileName_defaultConfig, debug=False):
		success = self._write(fileName, debug)
		return success
# MAKE A SAMPLE
	def sample(self):
		self.m_targetDbSet = TargetDbSet()
		self.m_targetDbSet.append(TargetDb("127.0.0.1", "DbName", "UserName", "Password"))
		self.m_dirPath = kDirPath_defaultConfig
		self.m_input = {"foo":"bar", "hello":"world"}
		self.m_output = {"lorem":"ipsum dolor", "sit":"amet"}
		return
# INNER FUNCTIONS
	def _read(self, fileName, debug):
		# 순수하게 데이터 읽기 기능만을 가짐 (무결성 검사 X)
		self.__init__()
		xelWrapper = []
		success = fileAccess(fileName, "rb", inXml, xelWrapper, level=warning, debug=debug)
		if not success:
			return False

		root = xelWrapper[0]
		if root is None:
			success = False
		else:
			rootTargetDbSet = root.find("targetDbSet")
			self.m_targetDbSet.readFrom(rootTargetDbSet)

			rootDirPath = root.find("dirPath")
			if rootDirPath is not None:
				self.m_dirPath = getAttrValue(rootDirPath, "path", kDirPath_defaultConfig)

			rootInput = root.find("input")
			if rootInput is not None:
				for key in rootInput.keys():
					self.m_input[key] = getAttrValue(rootInput, key, "")

			rootOutput = root.find("output")
			if rootOutput is not None:
				for key in rootOutput.keys():
					self.m_output[key] = getAttrValue(rootOutput, key, "")
		return success
	def _write(self, fileName, debug):
		# 순수하게 데이터 쓰기 기능만을 가짐 (무결성 검사 X)
		result = True
		root = ET.Element("config")
		tree = ET.ElementTree(root)

		self.m_targetDbSet.writeTo(root)
		SubElement(root, "dirPath", {"path":self.m_dirPath})
		SubElement(root, "input", self.m_input)
		SubElement(root, "output", self.m_output)
		
		return fileAccess(fileName, "wb", outXml, root, level=error, debug=debug)

# automator.py
# For making automation tools
#

# from ..base import *
# from .config import ConfigManager as cfgmgr

class Automator:
	def __init__(self, inputs={}, outputs={}, debug=False):
		self.arguments	= []
		self.dataRead	= {}
		self.dataWrite	= {}
		self.inputs		= inputs
		self.outputs	= outputs
		self.debug		= debug
		self.config		= ConfigManager()
		self.usage		=\
"""
Usage:
	test.py		nil.

Options:
	nil.		There is no option. Just example.
"""
	def main(self, *argv, range_=(1,)):
		if len(*argv) not in range_:
			print(self.usage)
		else:
			# GET REQUIREMENTS
			safeCall(self._convert, *argv)
			safeCall(self.config.load, self.inputs, self.outputs, self.debug, expected=True)
			# cfgmgr().load(self.inputs, self.outputs, self.debug)
			# USE REQUIREMENTS
			safeCall(self.read)
			safeCall(self.process)
			safeCall(self.write)
			# RESULT
			safeCall(print, "Done!")
			assertCall(print, "Failed!")
		return
	def _convert(self, argv):
		idx = 0
		for defaultValue in self.arguments:
			if idx < len(argv):
				self.arguments[idx] = strToValue(argv[idx], defaultValue, level=warning)
				idx += 1
				continue
			else:
				break
		assertCall(print, self.usage)
		return
	def read(self):
		assert(0)
	def process(self):
		assert(0)
	def write(self):
		assert(0)
