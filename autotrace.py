import os
import re
import csv
import time

urls_to_sample = 
['facebook.com','YouTube.com','google.com','twitter.com','wordpress.com','gmail.com','tripadvisor.com','yahoo.com','apple.com','glassdoor.com']

def init_test(numSamples, urls):
	for i in range(numSamples):
		for url in urls:
			t1 = time.time()
			os.system(f'traceroute -w1 -m30 {url} > temp_traceroute_data.txt')
			t2 = time.time()
			time_taken = t2 - t1
			process_file(url, time_taken)

			print(f'Sample {i + 1} completed, URL = {url}, seconds = {time_taken}')


def process_file(destination_url, time_taken):
	file = open('temp_traceroute_data.txt', 'r')
	lines = file.readlines()
	file.close()
	num_hops = 0
	for line in lines:
		match = re.match(r'\s*([0-9]+|\s)\s+([^\s]+)\s+\(([^\s]+)\)(.+)', line)
		if match is None: continue
		
		if match.group(1) == ' ': hop_number = 0
		else: hop_number = int(match.group(1))

		url = match.group(2)
		ip = match.group(3)
		everything_else = match.group(4).strip()
		
		num_hops = max(num_hops, hop_number)

	log_sample(destination_url, num_hops, time_taken)

def log_header():
	line = ''
	line += 'Destination URL,'
	line += 'Number of Hops,'
	line += 'Time Taken (s),'
	output_file.write(line + '\n')


def log_sample(destination_url, num_hops, time_taken):
	line = ''
	line += str(destination_url) + ','
	line += str(num_hops) + ','
	line += str(time_taken) + ','
	output_file.write(line + '\n')

samples = int(input('Enter the number of samples: '))

print()
print(f'URLs to sample: {urls_to_sample}')
print(f'Number of samples per URL: {samples}')
print()
print('Starting...')
print()

file_exists = os.path.isfile('automate_traceroute_log.csv')
output_file = open('automate_traceroute_log.csv', 'a')

if not file_exists: log_header()
init_test(samples, urls_to_sample)

os.remove('temp_traceroute_data.txt')

print('Successfully automated experiment.')