from map import Map, MapFile
from ant_colony import AntColony
from interface import GuiInterface

FAKE_AREA_SIZE = 1
FAKE_AREA_LENGTH = 4

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
    return ((pont_b[0]-pont_a[0])**2 + (pont_b[1]-pont_a[1])**2 ) **0.5

def _check_point_out_limit(pont, limit):
    return pont < 0 or pont > limit-1

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

    interface = GuiInterface()
    params = interface.arguments_parsing()
    
    if params["ants"] is None:
        params = interface.params_interface()
    
    try: 
        full_map = MapFile(params["map"]).get_map()
        
        it = 0
        pos_ant = full_map.initial_node
        final_obj = full_map.final_node
        vision_rad_ant = params["rad"] - 1 
        
        real_path = [pos_ant]
        
        while(it < params["itt"]):
            view_occupancy = full_map.cut_occupancy_grid_from_point(pos_ant, params["rad"])
            
            if not final_objetive_inside_radius_vision(pos_ant, params["rad"], final_obj):
                obj_point_itt = get_objective_point_in_cut_ant_vision(pos_ant, vision_rad_ant, final_obj )
                view_occupancy = create_fake_occupancy_area_in_micro_objective_point(view_occupancy,obj_point_itt, 
                                                                                        pos_ant, vision_rad_ant)
            else:
                obj_point_itt = final_obj
            
            reduce_map = Map(view_occupancy, pos_ant, obj_point_itt)
            
            colony = AntColony(reduce_map, params["ants"],  params["itt"],  params["phr"],  params["add_var"])
            path = colony.calculate_path()
            
            for point in path:
                if _dist_between_point(point,pos_ant) >= vision_rad_ant:
                    break
                real_path.append(point)
            
            if(params["disp"]): 
                interface.view_path_construction(real_path, full_map.occupancy_grid, full_map.initial_node, full_map.final_node)
            
            pos_converted = real_path[-1]
            
            if(pos_converted[0] == final_obj[0] and pos_converted[1] == final_obj[1]):
                break
            
            pos_ant = pos_converted
            
            it += 1
        
    except Exception as e:
        print(e)
        print("nao convergiu")
    
    print(f"size of path -> {len(real_path)}")
    interface.view_path(real_path, full_map.occupancy_grid, full_map.initial_node, full_map.final_node)
    