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
from MinHeap import MinHeap

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
		self.cities = self._scenario.getCities()
		self.ncities = len(self.cities)
		foundTour = False
		count = 0
		self.bssf = None

		lower_bound, self.reduced_cost_matrix = self.get_lower_bound_and_reduced_cost_matrix()

		original_reduced_cost_matrix = self.reduced_cost_matrix.copy()

		start_time = time.time()
		while not foundTour and time.time() - start_time < time_allowance:

			for i in range(self.ncities):
				route = []
				self.src = self.cities[i]
				self.src_index = i

				route.append(self.src)
				# Get a function to find the shortest path based on the adjacency matrix
				route = self.find_cheapest_route(i, route)

				self.reduced_cost_matrix = original_reduced_cost_matrix.copy()
				if route is None:
					continue


				solution = TSPSolution(route)
				solution.cost = solution._costOfRoute()

				if self.bssf is None or solution.cost < self.bssf.cost:
					self.bssf = solution
				count += 1
				if self.bssf.cost < np.inf:
					# Found a valid route
					foundTour = True

		end_time = time.time()
		results['cost'] = self.bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = self.bssf
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
		results = {}
		self.cities = self._scenario.getCities()
		self.ncities = len(self.cities)
		foundTour = False
		count = 0
		pruned = 0
		total_states = 0
		max_heap_size = 0
		self.pq = MinHeap([], len(self.cities)//2)

		lower_bound, self.reduced_cost_matrix = self.get_lower_bound_and_reduced_cost_matrix()

		start_time = time.time()
		while not foundTour and time.time() - start_time < time_allowance:
			# Rotate through different starting nodes
			for i in range(self.ncities):
				self.src = self.cities[i]
				self.src_index = i

				unvisited_nodes = [n for n in self.cities if n != self.src]
				self.pq.insert((0,TSPSolution([self.src], lower_bound, unvisited_nodes, self.src_index)))

				# Keep cycling through the lightest items until the queue is empty
				while len(self.pq.items) > 0:
					max_heap_size = len(self.pq.items) if len(self.pq.items) > max_heap_size else max_heap_size
					curr_solution = self.pq.pop()
					curr_lower_bound = curr_solution[1].lower_bound
					# Just in case the bssf updated since the curr_solution was added to the queue
					if curr_lower_bound > self.bssf.cost:
						pruned += 1
						continue

					curr_city_index = curr_solution[1].curr_index

					# Get a list of cities connected to the current city
					outbound_cities = self.reduced_cost_matrix[curr_city_index, :]

					for i in range(len(outbound_cities)):
						# Checkin if the route can be completed
						if len(curr_solution[1].route) == self.ncities:
							# Check if the city connects back to the center
							if outbound_cities[self.src_index] != math.inf:
								# Add cost to total route and compare to bssf
								curr_cost = outbound_cities[self.src_index]
								curr_solution[1].cost = curr_solution[1]._costOfRoute() + curr_cost
								if curr_solution[1].cost < self.bssf.cost:
									self.bssf = curr_solution[1]
								count += 1
								foundTour = True

						if i == curr_city_index: # Don't  check the same
							continue

						# Get the cost from the reduced cost matrix
						curr_cost = outbound_cities[i]

						if curr_cost != math.inf:
							# Get the corresponding city
							dest_city = self.cities[i]

							# Don't include any cities already on along the route
							if dest_city in curr_solution[1].route:
								continue

							updated_lower_bound = curr_cost + curr_lower_bound

							# Branch bounding
							if updated_lower_bound < self.bssf.cost:

								# Get a copy of the current route
								updated_route = curr_solution[1].route.copy()
								# Add the destination to the route
								updated_route.append(dest_city)

								# Get a copy of the unvisited routes
								updated_unvisited_nodes = curr_solution[1].unvisited_nodes.copy()
								# Remove the destination from unvisited routes
								updated_unvisited_nodes.remove(dest_city)

								# Update the score
								score = self.get_pq_score(updated_route, updated_lower_bound)

								# Insert in the priority queue
								self.pq.insert((score, TSPSolution(updated_route, updated_lower_bound, updated_unvisited_nodes, i)))
							else:
								pruned += 1
							total_states += 1

			break





		end_time = time.time()
		results['cost'] = self.bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = self.bssf
		results['max'] = max_heap_size
		results['total'] = total_states
		results['pruned'] = pruned
		return results



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

	def find_cheapest_route(self, curr_index, route):
		cheapest_cost = min(self.reduced_cost_matrix[curr_index, :])
		if cheapest_cost == math.inf:
			if len(route) == self.ncities:
				if self.cities[curr_index].costTo(self.src) != math.inf:
					return route
			else:
				return None

		dest_index = np.where(self.reduced_cost_matrix[curr_index, :] == cheapest_cost)[0][0]

		self.update_visited_routes(curr_index)

		route.append(self.cities[dest_index])

		return self.find_cheapest_route(dest_index, route)

	def update_visited_routes(self, index):
		# Block out all outbound edges
		self.reduced_cost_matrix[index,:] = math.inf

		# Block out all inbound edges
		self.reduced_cost_matrix[:,index] = math.inf

	def get_lower_bound_and_reduced_cost_matrix(self):
		adjacency_matrix = np.array(self._scenario._edge_exists.copy())

		adjacency_cost_matrix = self.generate_adjacency_matrix(adjacency_matrix, self.cities)

		return self.compute_lower_bound(adjacency_cost_matrix)

	def get_pq_score(self, updated_route, updated_lower_bound):
		return updated_lower_bound / len(updated_route)

