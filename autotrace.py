import os
import re
import csv
import time

#is_windows = os.name == 'nt'

urls_to_sample = ['facebook.com','YouTube.com','google.com','twitter.com','wordpress.com','gmail.com','tripadvisor.com','yahoo.com','apple.com','glassdoor.com']

def init_test(numSamples, urls):
	#cmd = 'tracert /w 1000 /h 30' if is_windows else 'traceroute -w1 -m30'
	cmd = 'traceroute -w1 -m30'
	for i in range(numSamples):
		for url in urls:
			t1 = time.time()
			os.system(f'{cmd} {url} > temp_traceroute_data.txt')
			t2 = time.time()
			time_taken = t2 - t1
			process_file(url, time_taken)

			print(f'Sample {i + 1} completed, URL = {url}, seconds = {time_taken}')


def process_file(destination_url, time_taken):
	ip_latencies_dictionary = {}
	file = open('temp_traceroute_data.txt', 'r')
	lines = file.readlines()
	file.close()
	num_hops = 0

	avg_latency_list = []
	for line in lines:
		if line.startswith('*'): continue

		match = re.match(r'\s*([0-9]+|\s)\s+([^\s]+)\s+\(([^\s]+)\)(.+)', line)
		if match is None: continue
		
		if match.group(1) == ' ': hop_number = 0
		else: hop_number = int(match.group(1))

		url = match.group(2)
		ip = match.group(3)
		everything_else = match.group(4).strip()
		
		if ip in ip_latencies_dictionary: continue # Only look at the first hop

		latencies = re.match(r'([0-9\.]+) ms(?: +([0-9\.]+) ms)?(?: +([0-9\.]+) ms)?', everything_else)
		if match is None: continue # No latency given
		avg_latency = 0
		if latencies.group(3) is not None:
			avg_latency = (float(latencies.group(1)) + float(latencies.group(2)) + float(latencies.group(3))) / 3
		elif latencies.group(2) is not None:
			avg_latency = (float(latencies.group(1)) + float(latencies.group(2))) / 2
		elif latencies.group(1) is not None:
			avg_latency = float(latencies.group(1))
		else: continue

		ip_latencies_dictionary[ip] = avg_latency

		avg_latency_list.append(f'{ip},{avg_latency}')

		num_hops = max(num_hops, hop_number)

	log_sample(destination_url, num_hops, time_taken, avg_latency_list)

def log_header():
	line = ''
	line += 'Destination URL,'
	line += 'Number of Hops,'
	line += 'Time Taken (s),'
	line += 'Averaged Latency (s),'
	output_file.write(line + '\n')


def log_sample(destination_url, num_hops, time_taken, avg_latency_list):
	avg_latency_str = ','.join(avg_latency_list)

	line = ''
	line += str(destination_url) + ','
	line += str(num_hops) + ','
	line += str(time_taken) + ','
	line += str(avg_latency_str) + ','
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