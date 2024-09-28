#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


class MapFile:
    def __init__(self, map_name):
        self.map = self._read_map(map_name)
        self.initial_node = self._get_position_by_char('S')
        self.final_node = self._get_position_by_char('F')
        self.occupancy_grid = self._convert_to_occupancy()
        
    def _get_position_by_char(self,char):
        return (int(np.where(self.map  == char)[0]), int(np.where(self.map  == char)[1]))
    
    def _read_map(self, map_name):
        map_planning = np.loadtxt('./maps/' + map_name, dtype=str)
        return map_planning
    
    def _convert_to_occupancy(self):
        map_arr = np.copy(self.map)
        map_arr[map_arr == 'O'] = 0
        map_arr[(map_arr == 'E') | (map_arr == 'S') | (map_arr == 'F')] = 1
        return map_arr.astype(int)
    
    def get_map(self):
        return Map(self.occupancy_grid,self.initial_node,self.final_node)


class Map:    
    
    class Nodes:
        def __init__(self, row, col, in_map):
            self.node_pos = (row, col)
            self.edges = self.compute_edges(in_map)

        def compute_edges(self, map_arr):
            imax = map_arr.shape[0]
            jmax = map_arr.shape[1]
            edges = []
            if map_arr[self.node_pos[0]][self.node_pos[1]] == 1:
                for dj in [-1, 0, 1]:
                    for di in [-1, 0, 1]:
                        newi = self.node_pos[0] + di
                        newj = self.node_pos[1] + dj
                        if dj == 0 and di == 0:
                            continue
                        if newj >= 0 and newj < jmax and newi >= 0 and newi < imax:
                            if map_arr[newi][newj] == 1:
                                edges.append({'FinalNode': (newi, newj),
                                              'Pheromone': 1.0, 'Probability': 0.0})
            return edges
        
    def __init__(self, occupancy, init_node, final_node):
        ## resume constructor to solver alg. 
        self.occupancy_grid = occupancy
        self.initial_node = init_node
        self.final_node = final_node
        self.nodes_array = self._create_nodes()
    
    def _create_nodes(self):
        return [[self.Nodes(i, j, self.occupancy_grid) 
                for j in range(self.occupancy_grid.shape[1])] 
                for i in range(self.occupancy_grid.shape[0])]
        
    def _check_point_out_limit(self, point, limit):
        return point < 0 or point > limit-1
    
    
    def cut_occupancy_grid_from_point(self, point, radius_vision):
        ## to facilite, the new view load the size of full map but with only region 
        # of ant's field vision         
        x_max = self.occupancy_grid.shape[0]
        y_max = self.occupancy_grid.shape[1]
        new_view_world  = [[0 for _ in range(y_max)] for _ in range(x_max)]
        
        up_left_point_view = (point[0] - radius_vision, point[1] - radius_vision)
        down_right_point_view = ( point[0] + radius_vision , point[1] + radius_vision)
        
        for i in range(up_left_point_view[0],down_right_point_view[0]):
            if self._check_point_out_limit(i, x_max):
                continue
            for j in range(up_left_point_view[1],down_right_point_view[1]):
                if self._check_point_out_limit(j, y_max) :
                    continue
                new_view_world[i][j] = self.occupancy_grid[i][j]
        
        return np.copy(new_view_world)

    
    def represent_map(self):
        ''' Represents the map '''
        # Map representation
        plt.plot(self.initial_node[1], self.initial_node[0], 'ro', markersize=10)
        plt.plot(self.final_node[1], self.final_node[0], 'bo', markersize=10)
        plt.imshow(self.occupancy_grid, cmap='gray', interpolation='nearest')
        plt.show()
        plt.close()

    def represent_path(self, path):
        ''' Represents the path in the map '''
        x = []
        y = []
        for p in path:
            x.append(p[1])
            y.append(p[0])
        plt.plot(x, y)
        self.represent_map()
