import csv
import sys

# first argument should be the csv to check
assert len(sys.argv)==2
file_name = sys.argv[1]

# csv column count
csv_len=14
row_line=1

# column 2 and 12 swap count
swaps_2_12=0
lines=[]

with open(file_name, 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for row in reader:
    # check for row len    
    if(len(row)!=csv_len):
      print "correct: ", row_line, " ", len(row), " !!!"
    row_line=row_line+1
    # check for column 2 and column 12 swap
    row[2] = row[2].strip()
    row[12] = row[12].strip()
    if not row[2].isdigit() :
      print row_line, " ", row[2]
      row[2], row[12] = row[12], row[2]
      swaps_2_12 = swaps_2_12 + 1
    lines.append(row)

print "made ", swaps_2_12, " swaps"
writer = csv.writer(open(file_name, 'w'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerows(lines)
