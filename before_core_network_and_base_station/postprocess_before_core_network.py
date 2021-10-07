import os
import re
import csv
import sys
from pprint import pprint

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
fileNamePath = ''
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
print(f'Selected "{fileName}"')
print()
print('1:\tAT&T (core network: 12.x)')
print('2:\tUCCS (core network: 192/206.X)')
print('3:\tQwest (core network: 4/72/152.X)')
print()
service_provider = int(input('What service provider? (1-3): '))

if service_provider == 1:
	core_address_prefix = ['12']
elif service_provider == 2:
	core_address_prefix = ['192', '206']
elif service_provider == 3:
	core_address_prefix = ['4', '72', '152']
else:
	print('Service provider not found.')
	sys.exit()

core_address_prefix_str = '/'.join(core_address_prefix)

def is_core(ip):
	for prefix in core_address_prefix:
		if ip.startswith(prefix + '.'): return True
	return False

readerFile = open(fileNamePath + fileName, 'r')
reader = csv.reader(x.replace('\0', '') for x in readerFile)

header = next(reader)
print(f'Columns: {len(header)}')
if len(header) != 64:
	print('ERROR: Invalid number of columns, should be 64')
	sys.exit()


outputFile = open(f'postprocessed_before_core_network_{fileName}', 'w')

histogram = {}

for row in reader:
	destination_url = row[0]
	time_taken = float(row[1])
	num_hops = float(row[2])

	i = 3
	while i + 1 < len(row):
		if row[i] not in histogram:
			histogram[row[i]] = 1
		else:
			histogram[row[i]] += 1
		i += 2

# Sort the histogram by most occurances
histogram = dict(sorted(histogram.items(), key = lambda item: item[1], reverse = True))

line = ''
line += 'Destination,'
line += f'First {core_address_prefix_str}.X Address,'
line += f'First {core_address_prefix_str}.X Latency,'
line += f'# Hops Up To {core_address_prefix_str}.X,'
line += f'Latencies Up To {core_address_prefix_str}.X,'
line += ' [ DIVIDER ] ,'
for i in range(1, 31):
	line += f'Hop {i} Address,'
	line += f'Hop {i} Histogram Occurrences,'
	line += f'Hop {i} Latency,'

outputFile.write(line + '\n')

# Restart the reader from the beginning
readerFile.seek(0)
reader = csv.reader(x.replace('\0', '') for x in readerFile)
header = next(reader)

row_count = 1

for row in reader:
	row_count += 1

	destination_url = row[0]
	time_taken = float(row[1])
	num_hops = float(row[2])

	first_12x_address = None
	first_12x_latency = 0
	num_hops_to_first_12x = 0
	latencies_up_to_first_12x = 0
	other_hop_data = ''

	i = 3
	while i + 1 < len(row):
		address = row[i]
		latency = row[i + 1] or '0'

		j = address.rfind('(')
		address_before = address[:j].strip()
		address_after = address[j + 1 : -1].strip()

		num_hops_to_first_12x += 1
		other_hop_data += address + ','
		other_hop_data += str(histogram[address]) + ','
		other_hop_data += latency + ','

		if is_core(address_after):
			first_12x_address = address
			first_12x_latency = latency
			break
		else:
			latencies_up_to_first_12x += float(latency)
		i += 2

	if first_12x_address is None:
		print(f'ERROR: Row {row_count} ({destination_url}): No core network that starts with {core_address_prefix_str}.X')
	line = ''
	line += destination_url + ','
	line += str(first_12x_address) + ','
	line += str(first_12x_latency) + ','
	line += str(num_hops_to_first_12x) + ','
	line += str(latencies_up_to_first_12x) + ','
	line += '|,'
	line += other_hop_data + ','
	outputFile.write(line + '\n')

print('DONE.')