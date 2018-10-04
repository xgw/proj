# load network trace, video chunk for agent to use, react to the action
import load_video_chunks
import load_trace
import numpy as np

# each action should be taken at the last chunks have been downloaded
# if stall, check the chunks are downloaded or not every x millseconds
# 

MILLISECONDS_IN_SECOND = 1000.0
B_IN_MB = 1000000.0
BITS_IN_BYTE = 8.0
RANDOM_SEED = 42
VIDEO_CHUNCK_LEN = 2000.0  # millisec, every time add this amount to buffer
PACKET_PAYLOAD_PORTION = 0.95
LINK_RTT = 80
BUFFER_THRESHHOLD = 4000
DRAIN_BUFFER_SLEEP_TIME = 500
NUM_OF_TRACKS = 9
TOTAL_VIDEO_CHUNCK = 20

class Environment:
	def __init__(self, time, bandwidth, random_seed=RANDOM_SEED):
		np.random.seed(random_seed)

		self.video_chunk_current = 1
		self.buffer_current = 0

		## pick a random trace file
		self.trace_index = np.random.randint(1, 65)
		self.time, self.bandwidth = load_trace.load_trace(self.trace_index)

		self.trace_ptr = np.random.randint(1, len(self.bandwidth))
		self.last_time = self.time[self.trace_ptr - 1]
		print(len(self.bandwidth))


	def get_video_chunk(self, bitrate_level, track_index):
	# get the size by bitrate_level, track_index and chunk_index from a funtion in load_video_chunks.py
	# track_index is an array that includes all indexes of tracks to download
		video_chunk_size = 0.0
		for index in range(2, NUM_OF_TRACKS+2):
			if index in track_index:
				video_chunk_size += load_video_chunks.get_video_size(bitrate_level, index, self.video_chunk_current)
			else:
				video_chunk_size += load_video_chunks.get_video_size(0, index, self.video_chunk_current)

		delay = 0.0
		video_chunk_sent = 0.0

		while True:
			throughput = self.bandwidth[self.trace_ptr] * B_IN_MB / BITS_IN_BYTE
			duration = self.time[self.trace_ptr] - self.last_time

			packet_payload = throughput * duration * PACKET_PAYLOAD_PORTION

			if video_chunk_sent + packet_payload >= video_chunk_size:
				fractional_time = (video_chunk_size - video_chunk_sent) / \
                                  throughput / PACKET_PAYLOAD_PORTION
				delay += fractional_time
				self.last_time += fractional_time
				break

			video_chunk_sent += packet_payload
			delay += duration
			self.last_time = self.time[self.trace_ptr]
			self.trace_ptr += 1

			if self.trace_ptr >= len(self.bandwidth):
				self.trace_ptr = 1
				self.last_time = 0

		delay *= MILLISECONDS_IN_SECOND
		delay += LINK_RTT
		rebuf = np.maximum(delay - self.buffer_current, 0.0)

		self.buffer_current = np.maximum(self.buffer_current - delay, 0.0)

		self.buffer_current += VIDEO_CHUNCK_LEN

		sleep_time = 0

		if self.buffer_current > BUFFER_THRESHHOLD:
			drain_buffer_time = self.buffer_current - BUFFER_THRESHHOLD
			sleep_time = np.ceil(drain_buffer_time / DRAIN_BUFFER_SLEEP_TIME) * \
                         DRAIN_BUFFER_SLEEP_TIME
			self.buffer_current -= sleep_time

		while True:
			duration = self.time[self.trace_ptr] - self.last_time
			if duration >= sleep_time / MILLISECONDS_IN_SECOND:
				self.last_time += sleep_time / MILLISECONDS_IN_SECOND
				break
			sleep_time -= duration * MILLISECONDS_IN_SECOND
			self.last_time = self.time[self.trace_ptr]
			self.trace_ptr += 1
			if self.trace_ptr >= len(self.bandwidth):
				self.trace_ptr = 1
				self.last_time = 0

		return_buffer_size = self.buffer_current

		self.video_chunk_current += 1
		end_of_video = False
		if self.video_chunk_current >= TOTAL_VIDEO_CHUNCK:
			end_of_video = True
			self.buffer_current = 0
			self.video_chunk_current = 1
			## pick a random trace file
			#
			#
			self.trace_ptr = np.random.randint(1, len(self.bandwidth))
			self.last_time = self.time[self.trace_ptr - 1]

		return delay, \
			rebuf / MILLISECONDS_IN_SECOND, \
			return_buffer_size, \
			sleep_time, \
			video_chunk_size, \
			end_of_video