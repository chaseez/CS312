#!/usr/bin/python3


from CS312Graph import *
import time
from MinHeap import MinHeap
from math import inf as INF


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex

        src_node = self.network.nodes[self.source]
        # for node in self.shortest_path:
        #     if node.node_id == self.source:
        #         src_node = node
        #         break

        curr_node = self.network.nodes[self.dest]
        # for node in self.shortest_path:
        #     if node.node_id == self.dest:
        #         curr_node = node
        #         break

        found = False
        total_length = 0
        path_edges = []

        while not found:
            prev, length = self.shortest_path[curr_node]
            if total_length == 0:
                total_length = length

            for neighbor in prev.neighbors:
                if neighbor.dest == curr_node:
                    path_edges.append((neighbor.src.loc, neighbor.dest.loc, '{:.0f}'.format(neighbor.length)))
                    break

            if prev == src_node:
                found = True
            else:
                curr_node = prev

        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        starting_node = self.network.nodes[srcIndex]
        self.shortest_path = {}

        # Stores next node and shortest length
        distance = {}
        previous = {}

        if use_heap:
            # Creating a list of undiscovered nodes with infinity as the weights
            items = [(item, INF) for item in self.network.nodes]
            heap = MinHeap(items)
            heap.decrease_key((starting_node, 0))

            while len(heap.items) > 0:
                curr_node_tuple = heap.pop()

                # neighbor has 3 members
                # .src (source node)
                # .dest (destination node)
                # .length (weight)
                for neighbor in curr_node_tuple[0].neighbors:

                    if neighbor.dest not in distance:
                        distance[neighbor.dest] = INF

                    if neighbor.dest not in previous:
                        previous[neighbor.dest] = neighbor.src

                    # Comparing the current weight of the neighboring node to the new weight
                    if distance[neighbor.dest] > curr_node_tuple[1] + neighbor.length:
                        # Updating the total distance to that node
                        distance[neighbor.dest] = curr_node_tuple[1] + neighbor.length

                        # Updating the previous pointing node
                        previous[neighbor.dest] = curr_node_tuple[0]

                        # Update the distance in the heap
                        heap.decrease_key((neighbor.dest, curr_node_tuple[1] + neighbor.length))
        else:  # Put dictionary implementation here
            node_map ={}
            for node in self.network.nodes:
                node_map[node] = INF

            node_map[starting_node] = 0

            while len(node_map) > 0:
                # Update the curr_node by finding the next smallest weight
                curr_node = (min(node_map.items(), key=lambda x: x[1]))[0]
                curr_length = node_map.pop(curr_node)

                for neighbor in curr_node.neighbors:

                    if neighbor.dest not in distance:
                        distance[neighbor.dest] = INF

                    if neighbor.dest not in previous:
                        previous[neighbor.dest] = neighbor.src

                    # Comparing the current weight of the neighboring node to the new weight
                    if distance[neighbor.dest] > curr_length + neighbor.length:
                        # Updating the total distance to that node
                        distance[neighbor.dest] = curr_length + neighbor.length

                        # Updating the previous pointing node
                        previous[neighbor.dest] = curr_node

                        # Update the distance in the map
                        node_map[neighbor.dest] = curr_length + neighbor.length

        # shortest_path = { destination node: (previous node, TOTAL distance to node)}
        for node, prev in previous.items():
            self.shortest_path[node] = (prev, distance[node])

        t2 = time.time()
        return (t2 - t1)
