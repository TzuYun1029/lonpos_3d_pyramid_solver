import numpy as np
from brick_dict import brick_dict
from utils import *
import os.path

folder_name = 'arrangements'    
def find_arrangements():
    """
    Find and save all possible arrangements for each brick type.
    This function generates a lookup table for brick arrangements and stores them in the './arrangements' folder.
    """
    coor = gen_coor()
    if not os.path.exists(folder_name): os.makedirs(folder_name)
    for brick_color in brick_dict.keys():
        if os.path.exists(f'./{folder_name}/{brick_color}.npy') == False:
            print(f"Finding all arrangements of the {brick_color} brick...")
            index = brick_dict[brick_color]['index']
            if len(index) < 5:
                # For bricks with less than 5 components
                d_comb = get_brick_distance(coor, index)
                pos = find_pos(coor, index, d_comb)
                np.save(f'./{folder_name}/{brick_color}_pri.npy', pos)
                final_result = eli_same(pos)
                np.save(f'./{folder_name}/{brick_color}.npy', final_result)

            else:
                # For bricks with 5 or more components (composed of two smaller bricks)
                brick1, brick2 = brick_dict[brick_color]['bricks']
                final_result = find_combine(coor, f'./{folder_name}/{brick1}.npy', f'./{folder_name}/{brick2}.npy',
                                            brick_dict[brick_color]['overlap_for_b1'],
                                            brick_dict[brick_color]['tight'])
                np.save(f'./{folder_name}/{brick_color}.npy', final_result)
            print("\n", '='*60, "\n")