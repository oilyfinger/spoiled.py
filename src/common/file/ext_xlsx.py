# ext_xlsx.py
# Simple tool functions for xlsx files
#

from ..base import *

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
