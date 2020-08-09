# ext_csv.py
# Simple tool functions for csv files
#

from ..base import *

import csv

def inCsv(file_, data, level=error, debug=False):
	data.clear()
	reader = csv.reader(file_, delimiter="\t")
	for row in reader:
		data.append(row)
	return
