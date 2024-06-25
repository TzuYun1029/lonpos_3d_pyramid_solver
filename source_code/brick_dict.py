from utils import *

coor = gen_coor()

# Dictionary containing information about different brick types and their properties
brick_dict = {
    'purple': {
        'index': [0,1,2,3],
    },
    'white': {
        'index': [0,1,5],
    },
    'light_green': {
        'index': [0,1,5,6],
    },
    'orange': {
        'index': [0,1,2,7],
    },
    'pink': {
        'index': [0,1,6,7,12],
        'bricks': ['white_pri', 'white_pri'],  # Component bricks
        'overlap_for_b1': [-1,-1,1],  # Overlap indices for the first brick
        'tight': [[1,2,distance(coor, 2,10)], [0,0,distance(coor, 1,5)]]  # Tight constraints
    },
    'skin': {
        'index': [0,1,2,3,7],
        'bricks': ['white_pri', 'purple_pri'], 
        'overlap_for_b1': [2,3,-1],
        'tight': [[2,0,distance(coor, 0,7)]]
    },
    'blue': {
        'index': [0,1,2,3,8],
        'bricks': ['white_pri', 'purple_pri'], 
        'overlap_for_b1': [3,-1,2],
        'tight': [[1,0,distance(coor, 8,0)]]
    },
    'gray': {
        'index': [1,5,6,7,11],
        'bricks': ['white_pri', 'white_pri'], 
        'overlap_for_b1': [0,-1,-1],
        'tight': [[1,1,distance(coor, 0,2)], [1,2,distance(coor, 1,5)]]
    },
    'yellow': {
        'index': [0,1,2,5,7],
        'bricks': ['white_pri', 'white_pri'], 
        'overlap_for_b1': [-1,2,-1],
        'tight': [[2,1,distance(coor, 0,2)], [0,0,distance(coor, 0,2)]]
    },
    'green': {
        'index': [0,1,2,7,8],
        'bricks': ['white_pri', 'orange_pri'], 
        'overlap_for_b1': [3,2,-1],
        'tight': [[2,0,distance(coor, 0,8)]]
    },
    'red': {
        'index': [0,1,2,5,6],
        'bricks': ['white_pri', 'light_green_pri'], 
        'overlap_for_b1': [0,2,-1],
        'tight': [[2,1,distance(coor, 0,2)]]
    },
    'light_blue': {
        'index': [0,1,2,5,10],
        'bricks': ['orange_pri', 'orange_pri'], 
        'overlap_for_b1': [-1,3,2,1],
        'tight': []
    }
}