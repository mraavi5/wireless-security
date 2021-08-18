import os
import re
import csv
import sys
from pprint import pprint

# Given a regular expression, list the files that match it, and ask for user input
def selectFile(regex, subdirs = False):
	files = []
	if subdirs:
		for (dirpath, dirnames, filenames) in os.walk('.'):
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


fileName = selectFile('.*.csv')
if fileName == '': sys.exit()

readerFile = open(fileName, 'r')
reader = csv.reader(x.replace('\0', '') for x in readerFile)

header = next(reader)
print(f'Columns: {len(header)}')
if len(header) != 64:
	print('ERROR: Invalid number of columns, should be 64')
	sys.exit()


outputFile = open(f'postprocessed_intersection_{fileName}', 'w')

nodes_per_url = {}

for row in reader:
	destination_url = row[0]
	time_taken = float(row[1])
	num_hops = float(row[2])

	nodes = []

	i = 3
	while i + 1 < len(row):
		# Append the node address
		nodes.append(row[i])
		i += 2

	if destination_url not in nodes_per_url:
		nodes_per_url[destination_url] = [nodes]
	else:
		nodes_per_url[destination_url].append(nodes)

#pprint(nodes_per_url)

def intersection(l1, l2):
	return list(set(l1) & set(l2))

for url in nodes_per_url:
	for i in range(1, len(nodes_per_url[url])):
		nodes_per_url[url][0] = intersection(nodes_per_url[url][0], nodes_per_url[url][i])



line = ''
line += 'URL,'
line += 'Addresses in common,'
for i in range(1, 31):
	line += ','

for url in nodes_per_url:
	nodes = nodes_per_url[url][0]

	print(f'\nURL: {url} - INTERSECTION {nodes}')
	line = ''
	line += url + ','
	line += ','.join(nodes)
	outputFile.write(line + '\n')

print('DONE.')