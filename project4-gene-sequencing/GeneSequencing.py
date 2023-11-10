#!/usr/bin/python3

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
		self.INDEL = 5
		self.SUB = 1
		self.MATCH = -3
		pass

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def align( self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		# seq1 is on "top", thus aligning with the columns
		# seq2 is on "left", thus aligning with the rows
		# Creating a list of lists to hold the edit distance dictionaries

		self.edit_distance = [[] for i in range(len(seq2))]
		self.edit_distance[0].append(0)

		# Tie breakers are always gonna be left, top, then diagonal
		# Incrementation Values
		# Insertions/Deletions: 5
		# Substitutions: 1
		# Match: -3

		prev_ed = 0
		sub_seq1 = ''
		sub_seq2 = ''

		prev_info = {
			'prev_i': 0,
			'prev_j': 0,
			'ed': prev_ed,
			'sub_seq1': sub_seq1,
			'sub_seq2': sub_seq2
		}
		self.edit_distance[0][0] = (prev_info)

		if not banded:
			# Initializing top row
			for j in range(1,len(seq1) + 1):
				prev_ed += 5
				sub_seq1 += seq1[j-1]
				sub_seq2 += '_'
				prev_info = {
					'prev_i': 0,
					'prev_j': j-1,
					'ed': prev_ed,
					'sub_seq1': sub_seq1,
					'sub_seq2': sub_seq2
				}
				self.edit_distance[0].append(prev_info)

			prev_ed = 0
			sub_seq1 = ''
			sub_seq2 = ''

			# Initializing left most column
			for i in range(1, len(seq2) + 1):
				prev_ed += 5
				sub_seq1 += '_'
				sub_seq2 += seq2[i - 1]
				prev_info = {
					'prev_i': i - 1,
					'prev_j': 0,
					'ed': prev_ed,
					'sub_seq1': sub_seq1,
					'sub_seq2': sub_seq2
				}
				self.edit_distance[i].append(prev_info)
		else:
			# Initializing top row
			for j in range(1, len(seq1)):
				prev_ed += 5
				if prev_ed > 7:
					continue
				sub_seq1 += seq1[j - 1]
				sub_seq2 += '_'
				prev_info = {
					'prev_i': 0,
					'prev_j': j -1,
					'ed': prev_ed,
					'sub_seq1': sub_seq1,
					'sub_seq2': sub_seq2
				}
				self.edit_distance[0].append(prev_info)

			prev_ed = 0
			sub_seq1 = ''
			sub_seq2 = ''
			# Initializing left most column
			for i in range(1, len(seq2)):
				prev_ed += 5
				if prev_ed > 7:
					continue
				sub_seq1 += '_'
				sub_seq2 += seq2[i - 1]
				prev_info = {
					'prev_i': i - 1,
					'prev_j': 0,
					'ed': prev_ed,
					'sub_seq1': sub_seq1,
					'sub_seq2': sub_seq2
				}
				self.edit_distance[i].append(prev_info)

		print(self.edit_distance)



###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
		score = random.random()*100
		alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
			len(seq1), align_length, ',BANDED' if banded else '')
		alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
			len(seq2), align_length, ',BANDED' if banded else '')
###################################################################################################

		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}

	def get_edit_distance(self, i, j):
		pass

	def get_left(self, i, j):
		pass

	def get_top(self, i, j):
		pass

	def get_diagonal(self, i, j):
		pass