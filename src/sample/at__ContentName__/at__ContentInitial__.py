# at__ContentInitial__.py
# __ContentName__ Automation Tool
#
#-------------------------------------------------------------------------------- common modules
import os
import sys
if __name__ == "__main__":
	# for parent package
	sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
	from module import *
else:
	from . import module
from common import *
#----------------------------------------------------------------------------------- etc modules
# import openpyxl
# import re
# import datetime
# from enum import IntEnum
#------------------------------------------------------------------------------ global variables
keyInput	= "extKeyInput"
keyOutput	= "extKeyOutput"
#------------------------------------------------------------------------------- automator class
class __ContentName__Helper(Automator):
	def __init__(self):
		inputs =\
		{
			keyInput: "in_keyInput.txt"
		}
		outputs =\
		{
			keyOutput: "out_keyOutput.txt",
		}
		Automator.__init__(self, inputs, outputs)
		self.arguments = ["Hello world!\n"]
		self.debug = True
		self.usage =\
"""
Usage: at__ContentInitial__.py	inputs

Options:
	inputs		Sample inputs for at__ContentInitial__.py
"""
		return
	def read(self):
		fileName = self.inputs[keyInput]
		return
	def process(self):
		self.dataWrite[keyOutput] = _make__Something__(self.dataRead, self.arguments)
		return
	def write(self):
		fileName = self.outputs[keyOutput]
		fileAccess(fileName, "w", outRaw, self.dataWrite[keyOutput], debug=self.debug)
		return
#---------------------------------------------------------------------------- _make__Something__
def _make__Something__(dataRead, arguments):
	return str(arguments)
#------------------------------------------------------------------------ referencing dictionary
#----------------------------------------------------------------------------------- end of file
if __name__ == "__main__":
	helper = __ContentName__Helper()
	helper.main(sys.argv[1:], range_=(1,))
