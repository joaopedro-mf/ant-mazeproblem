from tkinter import *
from tkinter import ttk
from map import Map, MapFile
from ant_colony import AntColony

import numpy as np
import matplotlib.pyplot as plt
import argparse

PAD_GUI_SIZE = 50
FAKE_AREA_SIZE = 1
FAKE_AREA_LENGTH = 2

def arguments_parsing():
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
    
def params_interface():
    root = Tk()
    root.title("Ant Colony Optimization Params")
    frm = ttk.Frame(root, padding=PAD_GUI_SIZE)
    frm.grid()
    
    ## variables inputs
    map_var=    StringVar(value="map2.txt")
    ant_var=    IntVar(value = 10)
    itt_var=    IntVar(value = 100)
    phr_var=    DoubleVar(value = 0.5)
    add_var=    DoubleVar(value = 100)
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

def get_objective_point_in_cut_ant_vision(ant_position, rad_vision, objective_point):
    # thales theorem
    diff_x  =  objective_point[0] - ant_position[0]
    diff_y = objective_point[1] - ant_position[1]
    ref_point =  rad_vision + FAKE_AREA_SIZE
    
    if diff_x < diff_y:  
        return ( ant_position[0] + int( diff_x * (ref_point / diff_y) ) ,  ant_position[1] + ref_point ) 
    else:
        return ( ant_position[0] + ref_point , ant_position[1] + int( diff_y * (ref_point / diff_x) )) 

def final_objetive_inside_radius_vision(ant_position, rad_vision, objective_point):
    return ant_position[0] + rad_vision >= objective_point[0] and ant_position[1] + rad_vision >= objective_point[1]

def _dist_between_point(pont_a, pont_b):
    return ((pont_b[0]-pont_a[0])^2+(pont_b[1]-pont_a[1])^2 ) **0.5

def _check_point_out_limit(pont, limit):
    return pont < 0 or pont > limit

def represent_path(path, occupancy_map, initial_node, final_node):
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
    #plt.show()
    plt.pause(0.1)
    #plt.close("Figure 1")
    
def represent_path_static(path, occupancy_map, initial_node, final_node):
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
    plt.pause(30)
    #plt.close("Figure 1")

  
def create_fake_occupancy_area_in_micro_objective_point(view_occupancy, final_obj, ant_position, rad_vision ):
    
    view_occupancy[final_obj[0]][final_obj[1]] = 1
    incr_area = rad_vision + FAKE_AREA_SIZE # consider 0
    
    rang_x = range(ant_position[0]- incr_area, ant_position[0]+ incr_area )    
    rang_y = range(ant_position[1]- incr_area, ant_position[1]+ incr_area )
    
    x_ref = ant_position[0] + incr_area if final_obj[0] > ant_position[0] else ant_position[0] - incr_area
    y_ref = ant_position[1] + incr_area if final_obj[1] > ant_position[1] else ant_position[1] - incr_area
    
    if not _check_point_out_limit( y_ref , view_occupancy.shape[1]):
        for x in rang_x:
            if _check_point_out_limit(x, view_occupancy.shape[0]):
                continue
            if _dist_between_point((x, y_ref),final_obj) < FAKE_AREA_LENGTH :
                view_occupancy[x][y_ref] = 1 
                
    if not _check_point_out_limit( x_ref , view_occupancy.shape[0]):
        for y in rang_y:
            if _check_point_out_limit(y, view_occupancy.shape[1]):
                continue
            if _dist_between_point((x_ref, y),final_obj) < FAKE_AREA_LENGTH :
                view_occupancy[x_ref][y] = 1 
        
    return view_occupancy
    
if __name__ == '__main__':

    params = arguments_parsing()
    
    if params["ants"] is None:
        params = params_interface()
    
    try: 
        full_map = MapFile(params["map"]).get_map()
        
        it = 0
        pos_ant = full_map.initial_node
        final_obj = full_map.final_node
        real_path = [full_map.initial_node]
        vision_rad_ant = params["rad"] - 1 
        
        while(it < params["itt"]):
            view_occupancy = full_map.cut_occupancy_grid_from_point(pos_ant, params["rad"])
            
            if not final_objetive_inside_radius_vision(pos_ant, params["rad"], final_obj):
                obj_point_itt = get_objective_point_in_cut_ant_vision(pos_ant, vision_rad_ant, final_obj )
                view_occupancy = create_fake_occupancy_area_in_micro_objective_point(view_occupancy,obj_point_itt, 
                                                                                        pos_ant, vision_rad_ant)
            else:
                obj_point_itt = final_obj
            
            reduce_map = Map(view_occupancy, pos_ant, obj_point_itt)
            reduce_map.represent_map()
            
            colony = AntColony(reduce_map, params["ants"],  params["itt"],  params["phr"],  params["add_var"])
            path = colony.calculate_path()
            
            for point in path:
                if(point[0] > ( (vision_rad_ant) + pos_ant[0]) or point[1]> ((vision_rad_ant) + pos_ant[1]-1 )):
                    break
                real_path.append(point)
            
            pos_converted = real_path[-1]
            
            if(pos_converted == final_obj):
                break
            
            pos_ant = pos_converted
            
            it += 1
        
    except:
        print("nao convergiu")
    
    print(real_path)
    print(f"tamanho -> {len(real_path)}")
    represent_path_static(real_path, full_map.occupancy_grid, full_map.initial_node, full_map.final_node)
    