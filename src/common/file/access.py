# access.py
# Simple file tool functions
#

from ..base import *
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
