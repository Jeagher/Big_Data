import csv 
from dbfpy import dbf
import os
import sys

DATADIR = "./"

for filename in os.listdir(DATADIR):
	print(filename)
	if filename.endswith(".dbf"):
		print("-->", filename)
		csv_fn = DATADIR+filename[:-4]+".csv"
		with open(csv_fn, "wb") as csvfile:
			in_db = dbf.Dbf(DATADIR+filename)
			out_csv = csv.writer(csvfile)
			names=[]
			for field in in_db.header.fields:
				names.append(field.name)
			out_csv.writerow(names)
			for rec in in_db:
				out_csv.writerow(rec.fieldData)
			in_db.close()