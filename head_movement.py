# get the head movement information
# 
import numpy as np

class move_prediction:

	def __init__(self):
		self.estimate_track_index = []
		self.actual_track_index = []


	# ask about need what to do the estimate
	# return estimate of the viewport as an array of tiles
	def get_head_movement_prediction(self):
		self.estimate_track_index = [2, 3, 4, 5, 6, 7, 8, 9, 10]

		return self.estimate_track_index

	# get the actual viewport as an array of tiles
	def get_head_movement_current(self):

		return self.actual_track_index


