import os
import sys

def autoInstall(packageName):
	notInstalled = False
	try:
		__import__(packageName)
		print("'%s' 패키지는 이미 설치되어 있습니다" % packageName)
	except ModuleNotFoundError:
		notInstalled = True
		print("'%s' 패키지가 설치되어 있지 않습니다\n설치를 시도합니다" % packageName)

	if notInstalled:
		try:
			import pip
			pip.main(["install", packageName])
			print("'%s' 패키지가 정상적으로 설치 되었습니다" % packageName)
		except:
			print("'%s' 패키지 설치에 실패했습니다\n수동 설치 해주세요" % packageName)
	print("")
	return

autoInstall("openpyxl")
print("자동 설치 스크립트를 종료합니다\n")
