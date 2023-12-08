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


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		adjacency_matrix = np.array(self._scenario._edge_exists.copy())

		adjacency_cost_matrix = self.generate_adjacency_matrix(adjacency_matrix, cities)

		lower_bound, reduced_cost_matrix = self.compute_lower_bound(adjacency_cost_matrix)

		print(lower_bound, reduced_cost_matrix)

		start_time = time.time()
		while not foundTour and time.time() - start_time < time_allowance:
			# create a random permutation
			for i in range(ncities):
				route = []
				# Get a function to find the shortest path based on the adjacency matrix
				bssf = TSPSolution(route)
				count += 1
				if bssf.cost < np.inf:
					# Found a valid route
					foundTour = True

		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results




	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound( self, time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass

	def generate_adjacency_matrix(self, adjacency_matrix, cities):
		cost_matrix = []
		for i in range(len(adjacency_matrix)):
			src = cities[i]
			cost_matrix.append([])
			for j in range(len(adjacency_matrix)):
				target = cities[j]
				if adjacency_matrix[i,j]:
					cost_matrix[i].append(src.costTo(target))
				else:
					cost_matrix[i].append(math.inf)

		return np.array(cost_matrix)

	def compute_lower_bound(self, adjacency_cost_matrix):
		reduced_outbound_matrix = []
		lower_bound = 0

		# Get the least cost for each outbound path
		for row in adjacency_cost_matrix:
			least_cost = min(row)
			lower_bound += least_cost

			# print(f'Before reduction: {row}')
			row -= least_cost
			# print(f'After reduction: {row}')
			reduced_outbound_matrix.append(row)

		reduced_outbound_matrix = np.array(reduced_outbound_matrix)

		reduced_cost_matrix = reduced_outbound_matrix.copy()

		# print(f'Reduced outbound matrix: {reduced_cost_matrix}')
		for i in range(len(reduced_cost_matrix)):
			least_cost = min(reduced_cost_matrix[:,i])
			if least_cost == 0:
				continue
			lower_bound += least_cost

			# print(f'Before reduction: {reduced_cost_matrix[:,i]}')
			reduced_cost_matrix[:,i] -= least_cost
			# print(f'After reduction: {reduced_cost_matrix[:,i]}')

		return (lower_bound, reduced_cost_matrix)

