# ext_xml.py
# Simple tool functions for xml files
#

from ..base import *

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
