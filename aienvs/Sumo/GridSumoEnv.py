from .SumoGymAdapter import SumoGymAdapter
import os
import copy
import aienvs

class GridSumoEnv(SumoGymAdapter):

    __DEFAULT_PARAMETERS = {
        'shape': (2, 2),
        'lane_length': 100,
        'car_pr': 0.1,
        'car_tm': 1000,
        'gui': False,
        'resolutionInPixelsPerMeterX': 0.1,
        'resolutionInPixelsPerMeterY': 0.1
    }
    
    @staticmethod
    def create_scenario(grid_shape, lane_length, folder_path):

        scenario_name = "grid_{}x{}".format(grid_shape[0], grid_shape[1])
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        # generate node xml file
        content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        content += '<nodes">\n'
        # add nodes of traffic lights
        for rowID in range(1, grid_shape[1]+1):
            for colID in range(1, grid_shape[0]+1):
                y_coord = lane_length * (rowID)
                x_coord = lane_length * (colID)
                node_name = "l_{}_{}".format(colID, rowID)
                content += '   <node id="{}" x="{}" y="{}" type="traffic_light" />\n'.format(node_name, x_coord, y_coord)
        # add nodes of entrances
        for rowID in range(1, grid_shape[1]+1):
            y_coord = lane_length * (rowID)
            for i, colID in enumerate([0, grid_shape[0]+1]):
                x_coord = colID * lane_length
                node_name = "e_{}_{}".format(colID, rowID)
                content += '   <node id="{}" x="{}" y="{}" type="priority" />\n'.format(node_name, x_coord, y_coord)
        for colID in range(1, grid_shape[0]+1):
            x_coord = lane_length * (colID)
            for i, rowID in enumerate([0, grid_shape[1]+1]):
                y_coord = rowID * lane_length
                node_name = "e_{}_{}".format(colID, rowID)
                content += '   <node id="{}" x="{}" y="{}" type="priority" />\n'.format(node_name, x_coord, y_coord)
        content += '</nodes>\n'

        node_file_path = os.path.join(folder_path, "{}.nod.xml".format(scenario_name))
        with open(node_file_path, "w") as f:
            f.write(content)

        # generate edg xml file
        content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        content += '<edges">\n'

        def get_edge(from_node, to_node):
            return '   <edge id="{}_{}" from="{}" to="{}" numLanes="1" speed="70.0" />\n'.format(from_node, to_node, from_node, to_node)

        # horizontal edges
        for rowID in range(1, grid_shape[1]+1):
            for colID in range(grid_shape[0]+1):
                pre_from = "l"
                pre_to = "l"
                if colID == 0:
                    pre_from = "e"
                if colID == grid_shape[0]:
                    pre_to = "e"
                from_edge = pre_from + "_{}_{}".format(colID, rowID)
                to_edge = pre_to + "_{}_{}".format(colID+1, rowID)
                content += get_edge(from_edge, to_edge)
                content += get_edge(to_edge, from_edge)
        for colID in range(1, grid_shape[0]+1):
            for rowID in range(grid_shape[1]+1):
                pre_from = "l"
                pre_to = "l"
                if rowID == 0:
                    pre_from = "e"
                if rowID == grid_shape[1]:
                    pre_to = "e"
                from_edge = pre_from + "_{}_{}".format(colID, rowID)
                to_edge = pre_to + "_{}_{}".format(colID, rowID+1)
                content += get_edge(from_edge, to_edge)
                content += get_edge(to_edge, from_edge)
                
            
        # vertical edges
        content += '</edges>\n'
        edge_file_path = os.path.join(folder_path, "{}.edg.xml".format(scenario_name))
        with open(edge_file_path, "w") as f:
            f.write(content)

        def get_connection(from_edge, to_edge):
            return '   <connection from="{}" to="{}" />\n'.format(from_edge, to_edge)

        def get_node_name(colID, rowID):
            if colID == 0 or colID == grid_shape[0]+1 or rowID == 0 or rowID == grid_shape[1]+1:
                prefix = "e"
            else:
                prefix = "l"
            return "{}_{}_{}".format(prefix, colID, rowID)

        def get_edge_name(from_node_coord, to_node_coord):
            return "{}_{}".format(get_node_name(*from_node_coord), get_node_name(*to_node_coord))

        # connection files
        content = '<?xml version="1.0" encoding="iso-8859-1"?>\n'
        content += '<connections">\n'

        # horizontal connections
        for rowID in range(1, grid_shape[1]+1):
            for colID in range(grid_shape[0]):
                node1 = get_node_name(colID, rowID)
                node2 = get_node_name(colID+1, rowID)
                node3 = get_node_name(colID+2, rowID)
                content += get_connection(node1+"_"+node2, node2+"_"+node3)
                content += get_connection(node3+"_"+node2, node2+"_"+node1)
        for colID in range(1, grid_shape[0]+1):
            for rowID in range(grid_shape[1]):
                node1 = get_node_name(colID, rowID)
                node2 = get_node_name(colID, rowID+1)
                node3 = get_node_name(colID, rowID+2)
                content += get_connection(node1+"_"+node2, node2+"_"+node3)
                content += get_connection(node3+"_"+node2, node2+"_"+node1)


        content += '</connections>\n'
        connection_file_path = os.path.join(folder_path, "{}.con.xml".format(scenario_name))
        with open(connection_file_path, "w") as f:
            f.write(content)
        
        # generate tl light file
        content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        content += '<tlLogics">\n'
        for rowID in range(1, grid_shape[1]+1):
            for colID in range(1, grid_shape[0]+1):
                ID = "l_{}_{}".format(colID, rowID)
                content += '   <tlLogic id="{}" type="static" programID="0" offset="0">\n'.format(ID)
                content += '      <phase duration="32" state="GrGr"/>\n'
                content += '      <phase duration="13" state="yryr"/>\n'
                content += '      <phase duration="32" state="rGrG"/>\n'
                content += '      <phase duration="13" state="ryry"/>\n'
                content += '   </tlLogic>\n'
        content += '</tlLogics>\n'

        tllogic_file_path = os.path.join(folder_path, "{}.tll.xml".format(scenario_name))
        with open(tllogic_file_path, "w") as f:
            f.write(content)

        # generate network file
        net_file_path = os.path.join(folder_path, "{}.net.xml".format(scenario_name))
        command = 'netconvert --node-files={} --edge-files={} --connection-files={} --tllogic-files={} --output-file={}'.format(node_file_path, edge_file_path, connection_file_path, tllogic_file_path, net_file_path)
        os.system(command)

    @staticmethod
    def generate_route_starts(shape):

        def get_node_name(colID, rowID):
            if colID == 0 or colID == shape[0]+1 or rowID == 0 or rowID == shape[1]+1:
                prefix = "e"
            else:
                prefix = "l"
            return "{}_{}_{}".format(prefix, colID, rowID)

        route_starts = []
        for rowID in range(1, shape[1]+1):
            route = ''
            for colID in range(0, shape[0]+1):
                node1 = get_node_name(colID, rowID)
                node2 = get_node_name(colID+1, rowID)
                route += '{}_{} '.format(node1, node2)
            route = route[:-1]
            route_starts.append(route)
        for colID in range(1, shape[0]+1):
            route = ''
            for rowID in range(0, shape[1]+1):
                node1 = get_node_name(colID, rowID)
                node2 = get_node_name(colID, rowID+1)
                route += '{}_{} '.format(node1, node2)
            route = route[:-1]
            route_starts.append(route)
        return route_starts

    def __init__(self, parameters={}):
        # the purpose of this class is to automatically construct a grid sumo environment based on a subset of parameters
        
        # what are the parameters that we can compute automatically?
        # scene - we also need to generate scene if not exist
        # tlphasefile - konwn as scene is known
        # box_bottom_corner - gonna be (0,0)
        # box_top_corner - lane_length * (#col+1), lane_length * (#row+1)
        # route stuff

        # what are the parameters required by this environment?
        # shape 
        # resolutionInPixelsPerMeterX
        # resolutionInPixelsPerMeterY
        # y_t
        # car_pr
        # car_tm

        _parameters = copy.deepcopy(self.__DEFAULT_PARAMETERS)
        _parameters.update(parameters)

        shape = _parameters['shape']
        lane_length = _parameters['lane_length']
        
        # construct scenario if not exist
        sceanrio = "grid_{}x{}".format(shape[0], shape[1])
        scenario_path = os.path.join("/".join(aienvs.__file__.split("/")[:-2]), "scenarios/Sumo/{}".format(sceanrio))
        _parameters['scene'] = sceanrio
        _parameters['tlphasesfile'] = "{}.tll.xml".format(sceanrio)
        _parameters['box_bottom_corner'] = (0, 0)
        _parameters['box_top_corner'] = ((shape[0]+1)*lane_length, (shape[1]+1)*lane_length)
        
        self.create_scenario(shape, lane_length, scenario_path)

        # now automatically generate the route starts
        _parameters['route_starts'] = self.generate_route_starts(shape)

        super().__init__(parameters=_parameters)