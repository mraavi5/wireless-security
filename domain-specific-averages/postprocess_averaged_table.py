import os
import re
import csv
import sys


# Given a regular expression, list the files that match it, and ask for user input
def selectFile(regex, subdirs = False, walkDir = '.'):
	files = []
	if subdirs:
		for (dirpath, dirnames, filenames) in os.walk(walkDir):
			for file in filenames:
				path = os.path.join(dirpath, file)
				if path[:2] == '.\\': path = path[2:]
				if bool(re.match(regex, path)):
					files.append(path)
	else:
		for file in os.listdir(os.curdir):
			if os.path.isfile(file) and bool(re.match(regex, file)):
				files.append(file)
	
	print()
	if len(files) == 0:
		print(f'No files were found that match "{regex}"')
		print()
		return ''

	print('List of files:')
	for i, file in enumerate(files):
		print(f'  File {i + 1}  -  {file}')
	print()

	selection = None
	while selection is None:
		try:
			i = int(input(f'Please select a file (1 to {len(files)}): '))
		except KeyboardInterrupt:
			sys.exit()
		except:
			pass
		if i > 0 and i <= len(files):
			selection = files[i - 1]
	print()
	return selection


fileName = selectFile('.*.csv', True, '..')
if fileName == '': sys.exit()

# Extract the file path from the file name, since the walkDir is '..', not the current directory
i = fileName.rfind('/') # Linux
if i != -1:
	fileNamePath = fileName[:i+1]
	fileName = fileName[i+1:]
i = fileName.rfind('\\') # Windows
if i != -1:
	fileNamePath = fileName[:i+1]
	fileName = fileName[i+1:]


readerFile = open(fileName, 'r')
reader = csv.reader(x.replace('\0', '') for x in readerFile)

header = next(reader)
print(f'Columns: {len(header)}')
if len(header) != 64:
	print('ERROR: Invalid number of columns, should be 64')
	sys.exit()


outputFile = open(f'postprocessed_averaged_{fileName}', 'w')

# Dictionary where each url has an array, the array values are as follows:
# 0: Count for number of samples
# 1: Sum of time_taken
# 3: Sum of num_hops
sumData = {}

for row in reader:
	destination_url = row[0]
	time_taken = float(row[1])
	num_hops = float(row[2])

	if destination_url not in sumData:
		sumData[destination_url] = [1, time_taken, num_hops]
	else:
		sumData[destination_url][0] += 1
		sumData[destination_url][1] += time_taken
		sumData[destination_url][2] += num_hops

line = ''
line += 'URL,'
line += 'Num Samples,'
line += 'Avg Time Taken,'
line += 'Avg Num Hops,'
outputFile.write(line + '\n')

for destination_url in sumData:
	print(f'Writing url "{destination_url}"')
	line = ''
	line += destination_url + ','
	line += str(sumData[destination_url][0]) + ','
	line += str(sumData[destination_url][1] / sumData[destination_url][0]) + ','
	line += str(sumData[destination_url][2] / sumData[destination_url][0]) + ','
	outputFile.write(line + '\n')

print('DONE.')