# config.py
# For configuration management
#

from ..base import *
from ..file import *

import os
import sys

import	xml.etree.ElementTree	as ET
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
