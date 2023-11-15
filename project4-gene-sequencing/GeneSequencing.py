#!/usr/bin/python3
import math

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def align( self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		self.seq1 = seq1
		self.seq2 = seq2

		"""
		Initializing edit distance lists
		"""

		# seq1 is on "top", thus aligning with the columns
		# seq2 is on "left", thus aligning with the rows
		# Creating a list of lists to hold the edit distance dictionaries

		self.edit_distance_banded = {}
		self.edit_distance_unbanded = [[] for i in range(len(seq2) + 1)]
		self.edit_distance_unbanded[0].append(0)

		# Tie breakers are always gonna be left, top, then diagonal
		# Incrementation Values
		# Insertions/Deletions: 5
		# Substitutions: 1
		# Match: -3

		prev_ed = 0
		sub_seq1 = ''
		sub_seq2 = ''

		# Dictionary for storing all info
		curr_info = {
			'prev_i': None,
			'prev_j': None,
			'ed': prev_ed,
			'sub_seq1': sub_seq1,
			'sub_seq2': sub_seq2
		}
		if self.banded:
			self.edit_distance_banded[(0,0)] = curr_info
		else:
			self.edit_distance_unbanded[0][0] = curr_info

		# Limiting amount of characters that can be allowed with the algorithm
		if len(seq1) > self.MaxCharactersToAlign:
			seq1_size = self.MaxCharactersToAlign + 1
		else:
			seq1_size = len(seq1) + 1


		# Initializing first row
		for j in range(1,seq1_size):
			prev_ed += 5
			if self.banded and j == 4: # Filling up to j + 3 from 0
				break
			sub_seq1 += seq1[j-1]
			sub_seq2 += '-'
			curr_info = {
				'prev_i': 0,
				'prev_j': j-1,
				'ed': prev_ed,
				'sub_seq1': sub_seq1,
				'sub_seq2': sub_seq2
			}
			if self.banded:
				self.edit_distance_banded[(0,j)] = curr_info
			else:
				self.edit_distance_unbanded[0].append(curr_info)

		# Resetting variables
		prev_ed = 0
		sub_seq1 = ''
		sub_seq2 = ''

		if len(seq2) > self.MaxCharactersToAlign:
			seq2_size = self.MaxCharactersToAlign + 1
		else:
			seq2_size = len(seq2) + 1

		# Initializing left most column
		for i in range(1, seq2_size):
			prev_ed += 5
			if self.banded and i == 4: # Filling up to i + 3 from 0
				break
			sub_seq1 += '-'
			sub_seq2 += seq2[i - 1]
			curr_info = {
				'prev_i': i - 1,
				'prev_j': 0,
				'ed': prev_ed,
				'sub_seq1': sub_seq1,
				'sub_seq2': sub_seq2
			}
			if self.banded:
				self.edit_distance_banded[(i,0)] = curr_info
			else:
				self.edit_distance_unbanded[i].append(curr_info)


		"""
		Fill edit distance lists and find the shortest/least-cost distance
		"""
		if self.banded:
			too_big =False
			# No need to calculate edit distance if the genomes are too far apart
			if abs(seq2_size - seq1_size) > 1000:
				too_big = True
				score = math.inf
				alignment1 = 'No possible path'
				alignment2 = 'No possible path'
			else:
				# Moving along the zipped axis
				# This truncates the longer range to fit the short one
				for i,j in zip(range(1,seq2_size), range(1,seq1_size)):
					for banded_j in range(j - MAXINDELS, j + MAXINDELS + 1): # This is the bandwidth
						if 1 <= banded_j < seq1_size: # Guard to protect against pointer out of range
							# Also don't want to mess with the redo the work for column 0
							self.edit_distance_banded[(i,banded_j)] = self.get_edit_distance(i, banded_j)
						else:
							continue
		else:
			# Sequence 2 is lined up with the rows
			for i in range(1, seq2_size):
				# Sequence 1 is lined up with the columns
				for j in range(1, seq1_size):
					# Find the cheapest edit distance
					# Put info into the edit distance list
					self.edit_distance_unbanded[i].append(self.get_edit_distance(i, j))





###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
		if self.banded:
			# Prevent overmatching
			if not too_big:
				# Find the smaller sequence to get the final edit distance index
				smaller_sequence = min([seq2_size, seq1_size])
				score = self.edit_distance_banded[(smaller_sequence - 1, smaller_sequence - 1)]['ed']
				alignment1 = self.edit_distance_banded[(smaller_sequence - 1, smaller_sequence - 1)]['sub_seq1'][:100]
				alignment2 = self.edit_distance_banded[(smaller_sequence - 1, smaller_sequence - 1)]['sub_seq2'][:100]
		else:
			score = self.edit_distance_unbanded[seq2_size - 1][seq1_size - 1]['ed']
			alignment1 = self.edit_distance_unbanded[seq2_size - 1][seq1_size - 1]['sub_seq1'][:100]
			alignment2 = self.edit_distance_unbanded[seq2_size - 1][seq1_size - 1]['sub_seq2'][:100]
###################################################################################################

		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}

	def get_edit_distance(self, i, j):
		left_info = self.get_left(i,j)
		top_info = self.get_top(i,j)
		diag_info = self.get_diagonal(i,j)

		# Find the smallest edit distance out of all the info
		min_value = min([left_info['ed'], top_info['ed'], diag_info['ed']])

		# Left has main priority
		if min_value == left_info['ed']:
			return left_info
		# Top has second priority
		elif min_value == top_info['ed']:
			return top_info
		# Diagonla has last priority
		else:
			return diag_info

	def get_left(self, i, j):
		# Moving one column to the left
		j -= 1

		if self.banded:
			if (i,j) in self.edit_distance_banded:
				ed = self.edit_distance_banded[(i,j)]['ed'] + INDEL
				# Inserting one letter to sequence 2
				sub_seq1 = self.edit_distance_banded[(i,j)]['sub_seq1'] + self.seq1[j]
				sub_seq2 = self.edit_distance_banded[(i,j)]['sub_seq2'] + "-"
			else: # For indexes out of range from the band
				ed = math.inf
				sub_seq1 = None
				sub_seq2 = None
		else:
			# Inserting one letter to sequence 2
			ed = self.edit_distance_unbanded[i][j]['ed'] + INDEL
			sub_seq1 = self.edit_distance_unbanded[i][j]['sub_seq1'] + self.seq1[j]
			sub_seq2 = self.edit_distance_unbanded[i][j]['sub_seq2'] + "-"

		return {
			'prev_i': i,
			'prev_j': j,
			'ed': ed,
			'sub_seq1': sub_seq1,
			'sub_seq2': sub_seq2
		}

	def get_top(self, i, j):
		# Moving one row up
		i -= 1

		if self.banded:
			if (i, j) in self.edit_distance_banded:
				ed = self.edit_distance_banded[(i, j)]['ed'] + INDEL
				# Inserting one letter to sequence 1
				sub_seq1 = self.edit_distance_banded[(i, j)]['sub_seq1'] + "-"
				sub_seq2 = self.edit_distance_banded[(i, j)]['sub_seq2'] + self.seq2[i]
			else: # For indexes out of range from the band
				ed = math.inf
				sub_seq1 = None
				sub_seq2 = None
		else:
			# Inserting one letter to sequence 1
			ed = self.edit_distance_unbanded[i][j]['ed'] + INDEL
			sub_seq1 = self.edit_distance_unbanded[i][j]['sub_seq1'] + "-"
			sub_seq2 = self.edit_distance_unbanded[i][j]['sub_seq2'] + self.seq2[i]

		return {
			'prev_i': i,
			'prev_j': j,
			'ed': ed,
			'sub_seq1': sub_seq1,
			'sub_seq2': sub_seq2
		}


	def get_diagonal(self, i, j):
		# Moving up one row and over one column
		i -= 1
		j -= 1

		# Comparing characters at each index
		if self.seq1[j] == self.seq2[i]:
			if self.banded: # There will always be a diagonal
				ed = self.edit_distance_banded[(i, j)]['ed'] + MATCH
			else:
				ed = self.edit_distance_unbanded[i][j]['ed'] + MATCH
		else: # If the characters can be substituted
			if self.banded: # There will always be a diagonal
				ed = self.edit_distance_banded[(i, j)]['ed'] + SUB
			else:
				ed = self.edit_distance_unbanded[i][j]['ed'] + SUB

		if self.banded: # There will always be a diagonal
			sub_seq1 = self.edit_distance_banded[(i, j)]['sub_seq1'] + self.seq1[j]
			sub_seq2 = self.edit_distance_banded[(i, j)]['sub_seq2'] + self.seq2[i]
		else:
			sub_seq1 = self.edit_distance_unbanded[i][j]['sub_seq1'] + self.seq1[j]
			sub_seq2 = self.edit_distance_unbanded[i][j]['sub_seq2'] + self.seq2[i]

		return {
			'prev_i': i,
			'prev_j': j,
			'ed': ed,
			'sub_seq1': sub_seq1,
			'sub_seq2': sub_seq2
		}