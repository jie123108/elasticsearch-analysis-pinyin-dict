# -*- coding: UTF-8 -*-
import re
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

pypattern = re.compile(r"\D*")

def pytrim(str):
	matched = pypattern.match(str)
	return matched.group(0)

def load_polyphones(filename):
	file = open(filename)
	lines = []
	for line in file:
		line = line.strip()
		arr = line.split("=")
		if len(arr) == 2:
			pys = arr[1].strip()
			pyarr = pys.split(",")
			if len(pyarr) > 1:
				uni = {}
				for py in pyarr:
					py = pytrim(py)
					# print arr[0], pytrim(py)
					uni.setdefault(py, 0)
					uni[py] += 1
				pys = uni.keys()
				if len(pys) > 1:
					lines.append(arr[0])

	return lines

def create_pattern(pinyin_filename):
	lines = load_polyphones(pinyin_filename)

	ptn =  ur"[" + ur''.join(lines) + ur"]"
	pattern = re.compile(ptn, re.UNICODE)
	return pattern

def include_polyphones(pattern, str):
	matched = pattern.search(str)
	return matched != None


def main(pinyin_filename, souguo_filename, max_len):
	i=1
	pattern = create_pattern(pinyin_filename)
	file = open(souguo_filename)
	for line in file:
		line = line.strip()
		arr = line.split(" ")
		if len(arr) == 2:
			pys = arr[0].strip()
			zhs = arr[1].strip()
			pyarr = pys.split("'")
			zhs_uni = zhs.decode("utf8")
			if len(pyarr) <= max_len and include_polyphones(pattern, zhs_uni):
				print(u"%s=%s" % (zhs, pys.replace("'", " ")))

pinyin_filename="./pinyin.txt"
souguo_filename="./pyDhrase.org"
main(pinyin_filename, souguo_filename, 4)