# load traces as arrays
# traces is saved as time[index], throughput[index]

TRACE_FOLDER = '/home/xgw/Work/Code/proj/synthetic_traces_complete/training/'

def load_trace(trace_index):
	time, bandwidth = [], []
	filename = TRACE_FOLDER + 'trace' + str(trace_index) + '.txt'
	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			value = [float(s) for s in line.split()]
			time.append(value[0])
			bandwidth.append(value[1])
	return time, bandwidth