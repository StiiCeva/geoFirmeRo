import csv
import sys

if len(sys.argv)==0:
  file_name = sys.argv[0]
file_name = 'nS_1_A.csv'

csv_len=14
row_line=0

with open(file_name, 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
  for row in reader:
    if(len(row)!=csv_len):
      print row_line, " ", len(row)
      print row
    row_line=row_line+1

