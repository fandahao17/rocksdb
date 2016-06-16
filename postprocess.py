#!/usr/bin/env python
from collections import namedtuple
from itertools import islice
import operator
import sys

total_samples = 0
thread_module_samples = {}
function_module_samples = {}
module_samples = {}
threads = set()

ThreadModule = namedtuple('ThreadModule', ['thread', 'module'])
FunctionModule = namedtuple('FunctionModule', ['function', 'module'])

with open(sys.argv[1] + "/" + sys.argv[2] + ".perf.txt") as f:
	for line in f:
		fields = line.split()
		total_samples += int(fields[1])
		key = ThreadModule(fields[2], fields[3])
		thread_module_samples.setdefault(key, 0)
		thread_module_samples[key] += int(fields[1])
		key = FunctionModule(fields[5], fields[3])
		function_module_samples.setdefault(key, 0)
		function_module_samples[key] += int(fields[1])
		threads.add(fields[2])

		key = fields[3]
		module_samples.setdefault(key, 0)
		module_samples[key] += int(fields[1])

for thread in sorted(threads):
	thread_pct = 0
	print
	print("Thread: {:s}".format(thread))
	print(" Percent      Module")
	print("============================") 
	for key, value in sorted(thread_module_samples.items(), key=operator.itemgetter(1), reverse=True):
		if key.thread == thread:
			print("{:8.4f}      {:20s}".format(float(value) * 100 / total_samples, key.module))
			thread_pct += float(value) * 100 / total_samples
	print("============================")
	print("{:8.4f}       Total".format(thread_pct))

print
print(" Percent      Module               Function")
print("=================================================================") 
for key, value in islice(sorted(function_module_samples.items(), key=operator.itemgetter(1), reverse=True), 100):
	print("{:8.4f}      {:20s} {:s}".format(float(value) * 100 / total_samples, key.module, key.function))

print
print
print(" Percent      Module")
print("=================================") 
for key, value in sorted(module_samples.items(), key=operator.itemgetter(1), reverse=True):
	print("{:8.4f}      {:s}".format(float(value) * 100 / total_samples, key))

print
with open(sys.argv[1] + "/" + sys.argv[2] + "_db_bench.txt") as f:
	for line in f:
		if "maxresident" in line:
			fields = line.split()
			print("Wall time elapsed: {:s}".format(fields[2].split("e")[0]))
			print("CPU utilization: {:s}".format(fields[3].split('C')[0]))
			user = float(fields[0].split('u')[0])
			system = float(fields[1].split('s')[0])
			print("User:   {:8.2f} ({:5.2f}%)".format(user, user * 100 / (user + system)))
			print("System: {:8.2f} ({:5.2f}%)".format(system, system * 100 / (user + system)))

print
stat_lines = []
with open(sys.argv[1] + "/" + sys.argv[2] + "_blockdev_stats.txt") as f:
	for line in f:
		stat_lines.append(line.strip())
start = stat_lines[0].split()
end = stat_lines[1].split()
# Documentation on /sys/block/nvme0n1/stat output taken from:
# https://www.kernel.org/doc/Documentation/block/stat.txt
#
# Note: sysfs data always tracks number of sectors in 512-byte chunks,
#  even if underlying namespace is formatted as 4KB.
read_io = int(end[0]) - int(start[0])
read_bytes = (int(end[2]) - int(start[2])) * 512
write_io = int(end[4]) - int(start[4])
write_bytes = (int(end[6]) - int(start[6])) * 512
read_gb = float(read_bytes) / (1024 * 1024 * 1024)
write_gb = float(write_bytes) / (1024 * 1024 * 1024)
read_avg = float(read_bytes) / read_io / 1024
write_avg = float(write_bytes) / write_io / 1024
print("              I/O     Total   Average")
print("=====================================")
print("Read:  {:10d} {:7.2f}GB {:7.2f}KB".format(read_io, read_gb, read_avg))
print("Write: {:10d} {:7.2f}GB {:7.2f}KB".format(write_io, write_gb, write_avg))
