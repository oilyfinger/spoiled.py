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
