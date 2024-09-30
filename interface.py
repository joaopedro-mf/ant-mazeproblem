#!/usr/bin/env python

from tkinter import *
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
import argparse

PAD_GUI_SIZE = 50

class GuiInterface:    
        
    def arguments_parsing(self):
        ''' Function used for handling the command line argument options '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-a','--ants', help='the number of ants that made up the colony', type=int)
        parser.add_argument('-i','--iterations', help='the number of iterations to be performed by the algorithm', type=int)
        parser.add_argument('-m','--map', help='the map to calculate the path from', type=str)
        parser.add_argument('-p','--pheromone', help='controls the amount of pheromone that is evaporated, range[0-1], precision 0.05', type=float, choices=np.around(np.arange(0.0, 1.05, 0.05), decimals=2))
        parser.add_argument('-pa','--pheradd', help='controls the amount of pheromone that is added', type=float)
        parser.add_argument('-r','--radius', help='radius of vision of ants in maze', type=int)
        parser.add_argument('-d', '--display', action='count', help='display the map and the resulting path')
        
        args = parser.parse_args()
        
        return {"map": args.map,"ants":args.ants,"itt":args.iterations,
                "phr": args.pheromone,"add_var": args.pheradd,"rad": args.radius, "disp": args.display}
        
    def params_interface(self):
        root = Tk()
        root.title("Ant Colony Optimization Params")
        frm = ttk.Frame(root, padding=PAD_GUI_SIZE)
        frm.grid()
        
        ## variables inputs
        map_var=    StringVar(value="map1.txt")
        ant_var=    IntVar(value = 10)
        itt_var=    IntVar(value = 100)
        phr_var=    DoubleVar(value = 0.1)
        add_var=    DoubleVar(value = 1)
        disp_var=   IntVar(value = 1)
        rad_var =   IntVar(value = 5)
        
        ## labels
        ttk.Label(frm, text="Map name in folder maps", justify="left").grid(column=0, row=0)
        ttk.Label(frm, text="Number of ants", justify="left").grid(column=0, row=1)
        ttk.Label(frm, text="Number of iterations", justify="left").grid(column=0, row=2)
        ttk.Label(frm, text="Amount of pheromone evaporated", justify="left").grid(column=0, row=3)
        ttk.Label(frm, text="Amount of pheromone added", justify="left").grid(column=0, row=4)
        ttk.Label(frm, text="Radius of vision of ants", justify="left").grid(column=0, row=5)
        ttk.Label(frm, text="Display execution of algoritm", justify="left").grid(column=0, row=6)
        
        ##inputs
        ttk.Entry(frm, textvariable = map_var).grid(column=1, row=0)
        ttk.Entry(frm, textvariable = ant_var).grid(column=1, row=1)
        ttk.Entry(frm, textvariable = itt_var).grid(column=1, row=2)
        ttk.Entry(frm, textvariable = phr_var).grid(column=1, row=3)
        ttk.Entry(frm, textvariable = add_var).grid(column=1, row=4)
        ttk.Entry(frm, textvariable = rad_var).grid(column=1, row=5)
        ttk.Checkbutton(frm, variable= disp_var).grid(column=1, row=6)


        ttk.Button(frm, text="Load", command=root.destroy).grid(column=1, row=7)
        root.mainloop()
        
        
        return {"map": map_var.get(),"ants":ant_var.get(),"itt":itt_var.get(),
                "phr": phr_var.get(),"add_var": add_var.get(),"rad": rad_var.get(), "disp": disp_var.get()}
    
    def view_path_construction(self, path, occupancy_map, initial_node, final_node):
        ''' Represents the path in the map '''
        x = []
        y = []
        for p in path:
            x.append(p[1])
            y.append(p[0])
            
        plt.plot(x, y)
        
        plt.plot(initial_node[1], initial_node[0], 'ro', markersize=10)
        plt.plot(final_node[1], final_node[0], 'bo', markersize=10)
        plt.imshow(occupancy_map, cmap='gray', interpolation='nearest')
        plt.pause(0.1)
        plt.clf()
        
    def view_path(self, path, occupancy_map, initial_node, final_node):
        ''' Represents the path in the map '''
        x = []
        y = []
        for p in path:
            x.append(p[1])
            y.append(p[0])
            
        plt.plot(x, y)
        
        plt.plot(initial_node[1], initial_node[0], 'ro', markersize=10)
        plt.plot(final_node[1], final_node[0], 'bo', markersize=10)
        plt.imshow(occupancy_map, cmap='gray', interpolation='nearest')
        plt.show()
