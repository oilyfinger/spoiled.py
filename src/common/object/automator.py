# automator.py
# For making automation tools
#

from ..base import *
from .config import ConfigManager as cfgmgr

class Automator:
	def __init__(self, inputs={}, outputs={}, debug=False):
		self.arguments	= []
		self.dataRead	= {}
		self.dataWrite	= {}
		self.inputs		= inputs
		self.outputs	= outputs
		self.debug		= debug
		self.config		= cfgmgr()
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
