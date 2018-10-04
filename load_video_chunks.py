# load video chunks as arrays
# including number of bitrate level, video size of each chunk, position information
import numpy as np
import os

TOTAL_VIDEO_CHUNCK = 20
BITRATE_LEVELS = 4
VIDEO_PATH = '/home/xgw/360video/gpac/SRD/srd_hevc/multi_rate_p60/'
VIDEO_TILES = 9


def get_video_size(bitrate_level, track_index, chunk_index):
	qp = ''
	if bitrate_level == 0:
		qp = 'qp37'
	elif bitrate_level == 1:
		qp = 'qp32'
	elif bitrate_level == 2:
		qp = 'qp27'
	elif bitrate_level == 3:
		qp = 'qp22'

	file_path = VIDEO_PATH + 'sequence_' + qp + '_dash_track' \
				+ str(track_index) + '_' + str(chunk_index) + '.m4s'

	chunk_size = os.path.getsize(file_path)
	return chunk_size