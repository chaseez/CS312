from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25

class Node():
	def __init__(self, point):
		self.point = point
		self.clockwise = self
		self.counter_clockwise = self



class Hull():
	def __init__(self, node):
		self.curr_point = node
		self.left_most = node
		self.right_most = node
		self.merged = None  # pointer to the hull that was merged with this one

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

	# Class constructor
	def __init__(self):
		super().__init__()
		self.pause = False

	# Some helper methods that make calls to the GUI, allowing us to send updates
	# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self, line, color):
		self.showTangent(line, color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self, polygon):
		self.view.clearLines(polygon)

	def showText(self, text):
		self.view.displayStatusText(text)

	def step_up(self, left_hull, right_hull):
		"""
		Implement step up function by getting the right most node from the left hull
		and the left most node from the right hull. Then rotate clockwise on the right hull
		one step and compare the slope from the previous point. If it's greater, update the line.
		Then rotate counterclockwise on the left hull and compare the slopes. If it's less than,
		update the line. Repeat until both sides don't change.
		"""
		high_left = left_hull.right_most
		high_right = right_hull.left_most

		dy = high_left.point.y() - high_right.point.y()
		dx = high_left.point.x() - high_right.point.x()
		slope = dy / dx

		changes = True
		while changes:
			# Moving the right node clockwise and comparing the slopes
			clockwise_right = high_right.clockwise


			n_dy = high_left.point.y() - clockwise_right.point.y()
			n_dx = high_left.point.x() - clockwise_right.point.x()
			new_slope = n_dy/n_dx

			if new_slope > slope:
				high_right = clockwise_right
				slope = new_slope
			else: # Unnecessary, but here to keep me happy lol
				changes = False


			# Moving the left node counter_clockwise and comparing the slopes
			counter_clockwise_left = high_left.counter_clockwise

			n_dy = counter_clockwise_left.point.y() - high_right.point.y()
			n_dx = counter_clockwise_left.point.x() - high_right.point.x()
			new_slope = n_dy / n_dx

			if new_slope < slope:
				high_left = counter_clockwise_left
				# Unnecessary, but here to keep me happy lol
				slope = new_slope
				changes = True

		return high_left, high_right


	def step_down(self, left_hull, right_hull):
		"""
		Do the exact opposite of step_up(). Find the left most node of the right hull and the right
		most node of the left hull. Repeat steps from step up, but reverse the direction. Repeat until
		both sides don't change.
		"""
		low_left = left_hull.right_most
		low_right = right_hull.left_most

		dy = low_left.point.y() - low_right.point.y()
		dx = low_left.point.x() - low_right.point.x()
		slope = dy / dx

		changes = True
		while changes:

			# Moving the right node counter_clockwise and comparing the slopes
			counter_clockwise_right = low_right.counter_clockwise

			n_dy = low_left.point.y() - counter_clockwise_right.point.y()
			n_dx = low_left.point.x() - counter_clockwise_right.point.x()
			new_slope = n_dy / n_dx

			if new_slope < slope:
				low_right = counter_clockwise_right
				slope = new_slope
			else:  # Unnecessary, but here to keep me happy lol
				changes = False

			# Moving the left node counter_clockwise and comparing the slopes
			clockwise_left = low_left.clockwise
			n_dy = clockwise_left.point.y() - low_right.point.y()
			n_dx = clockwise_left.point.x() - low_right.point.x()
			new_slope = n_dy / n_dx

			if new_slope > slope:
				low_left = clockwise_left
				# Unnecessary, but here to keep me happy lol
				slope = new_slope
				changes = True


		return low_left, low_right
		pass

	def merge_hull(self, hulls):
		# Sorts through the hulls to find which ones are unmerged
		need_merge = [p for p in hulls if p.merged == None]

		# If there's only 1 hull to merge, then no work needs to be done
		if len(need_merge) == 1:
			return

		# Loop through all the hulls, merging the "left hull" (i) into the "right hull" (i+1)
		# Hence, the range is 1 before the last index, so the last hull isn't merged with nothing.
		for i in range(len(need_merge) - 1):
			high_left, high_right = self.step_up(need_merge[i], need_merge[i + 1])
			low_left, low_right = self.step_down(need_merge[i], need_merge[i + 1])

			# Updating rotations for upper tangents
			high_left.clockwise = high_right
			low_left.counter_clockwise = low_right

			# Updating rotations for lower tangents
			high_right.counter_clockwise = high_left
			low_right.clockwise = low_left

			# Marking the first hull as merged
			need_merge[i].merged = True

			# Reassigning the left most value for the right hull
			need_merge[i+1].left_most = need_merge[i].left_most

	def join_hulls(self, hulls):
		# Finds the middle partition
		n = len(hulls) // 2

		# Recurse if there's more than one hull in the list
		if n > 1:
			# Recurse on the first half of the list
			self.join_hulls(hulls[:n])
			# Recurse on the second half of the list
			self.join_hulls(hulls[n:])

		# Taking the hulls, finding the upper and lower tangents, and merging the results
		self.merge_hull(hulls)

		# For the Show Recurse functionality
		# polygon = self.draw_convex_hull(hulls[-1])
		# self.showHull(polygon, RED)
		return hulls # Only used to return the list of modified hulls

	def draw_convex_hull(self, hull):
		hull_lines = []

		# Connect the first two nodes
		first_node = hull.left_most
		curr_node = first_node.counter_clockwise

		hull_lines.append(QLineF(first_node.point, curr_node.point))

		# Start a counterclockwise rotation
		next_node = curr_node.counter_clockwise

		# Repeat until the curr_node is the first_node to make a full circle
		while curr_node.point.x() != first_node.point.x():
			hull_lines.append(QLineF(curr_node.point, next_node.point))
			curr_node = next_node
			next_node = next_node.counter_clockwise
		return hull_lines

	# This is the method that gets called by the GUI and actually executes
	# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert (type(points) == list and type(points[0]) == QPointF)

		t1 = time.time()
		x = lambda point: point.x()
		# Sorts the points by x values
		points = sorted(points, key=x)

		# Initialize a list of Hull objects that contain a Node object that holds the point information
		hulls = [Hull(Node(p)) for p in points]
		t2 = time.time()

		t3 = time.time()
		hulls = self.join_hulls(hulls)
		t4 = time.time()

		polygon = self.draw_convex_hull(hulls[-1])

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon, RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
