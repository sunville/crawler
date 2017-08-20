#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

if __name__ == '__main__':
	with open('wangshu.csv','rb') as csvfile:
		rdr = csv.reader(csvfile, delimiter='\t')
		with open('wangshu_simply.csv','wb') as result:
			wtr = csv.writer(result)
			for row in rdr:
				wtr.writerow([row[0],row[1],row[2],row[3]])
		
