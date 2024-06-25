import numpy as np
import time
from brick_dict import brick_dict
from utils import *
import os.path
from find_all_arrangements import *

ques_list = [
    # questions are found on lonpos website
    # http://lonpos.cc/onlinetest_detail.php?id=18
    list('GGGEEGEEEBGF.BBF..BB.....CCCCC...F.....................'),
    list('CCCC.C.JKKIIJKKI.J..IIJ................................'),
    list('CCAAAC.AKKC..KKC.......................................'),
    list('CCCCDAAACDA..DD....D...................................'),
    list('JAA..JA...JA...J.......................................'),
    list('KKC..KK................................................'),
    list('AE...AAA...............................................'),
]

ques = []

def setQuestion(idx):
    global ques, ques_list
    ques = ques_list[int(idx)]
    return ques

def setCustomQues(arr):
    global ques
    ques = arr

def find_ans():
    """
    Main function to solve the brick arrangement puzzle.
    
    This function allows the user to choose an initial arrangement, then attempts to solve
    the puzzle by filling in the remaining bricks in a valid configuration.
    """
    
    # Brick names and their corresponding colors for display
    global brick_name_color_dict
    brick_name_color_dict = {
        'F': ['white', '⚪ '],
        'K': ['light_green', '🍈 '],
        'A': ['orange', '🟠'],
        'J': ['purple', '🟣'],
        'L': ['gray', '🌚 '],
        'G': ['light_blue', '🌐 '],
        'H': ['pink', '🌺 '],
        'C': ['blue', '🔵 '],
        'E': ['green', '🟢'],
        'I': ['yellow', '🟡'],
        'D': ['skin', '👝 '],
        'B': ['red', '🔴 '],
        '.': ['none', ' . '],
    }

    # Initialize global variables
    global try_log, check_count, attempt_count
    init_brick_pos_dict = {}  # Stores all possible positions of unused bricks 
    unused_bricks = []  # Stores names of unused bricks
    brick_ok_pos_num = []  # Stores the number of valid positions for each brick

    # Generate lookup table and store in folder './arrangements'
    find_arrangements()
    start_time = time.time()

    # Load all possible positions of unused bricks in question
    total_combination_of_rest_bricks = 1
    for brick, (color_name, symbol) in brick_name_color_dict.items():
        if brick != '.':
            if len(brick_dict[color_name]['index']) != ques.count(brick):
                init_brick_pos_dict[brick] = np.load(f'./{folder_name}/{color_name}.npy')
                unused_bricks.append(brick)

    # Delete impossible positions of all unused bricks  
    for brick in unused_bricks:
        ok_pos_idx = []
        fixed_index = [i for i, x in enumerate(ques) if x == brick]
        for i, pos in enumerate(init_brick_pos_dict[brick]):
            if init_check_valid(pos, ques, fixed_index, brick, unused_bricks, init_brick_pos_dict):
                ok_pos_idx.append(i)

        print(f"{brick_name_color_dict[brick][0]}: {len(init_brick_pos_dict[brick])} -> {len(ok_pos_idx)}")
        total_combination_of_rest_bricks *= len(ok_pos_idx)

        init_brick_pos_dict[brick] = init_brick_pos_dict[brick][ok_pos_idx]
        brick_ok_pos_num.append(len(ok_pos_idx))
    
    # print(f"total_combination_of_rest_bricks = {total_combination_of_rest_bricks:e}")
    # Sort unused_bricks by the number of valid positions (increasing order)
    sorted_unused_bricks, brick_ok_pos_num = zip(*sorted(zip(unused_bricks, brick_ok_pos_num), key=lambda x: x[1]))

    # Initialize variables for the search
    attempt_count = 0
    check_count = 0 

    # print("\nQuestion")
    # print_arr_in_pyramid(ques)

    # Compute the answer and measure elapsed time
    ans = fill(ques, init_brick_pos_dict, sorted_unused_bricks)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print results
    # print('Answer')
    # print_arr_in_pyramid(ans)
    # print('Total attempts:', attempt_count)
    # print('Total checks:', check_count)
    # print(f"Elapsed time: {elapsed_time:.4f} seconds")
    return ans, attempt_count, check_count, elapsed_time

def fill(arr, brick_pos_dict, sorted_unused_bricks): 
    """
    Recursively fill the pyramid with bricks.

    Args:
        arr (list): Current state of the pyramid.
        brick_pos_dict (dict): Dictionary of possible positions for each brick.
        sorted_unused_bricks (list): List of unused bricks sorted by number of possible positions.

    Returns:
        list: Completed pyramid arrangement if successful, 'Fail' otherwise.
    """
    global try_log, check_count, attempt_count, brick_name_color_dict
    least_pos_brick = sorted_unused_bricks[0] # get brick with least arrangements

    # Place the least_pos_brick into the pyramid with different kinds of positions
    for pos in brick_pos_dict[least_pos_brick]:
        new_arr = arr.copy()
        check_count += 1
        # Check if the current position can be placed into the pyramid
        is_valid, new_sorted_unused_bricks, new_brick_pos_dict\
             = fill_check_valid(pos, arr, least_pos_brick, brick_pos_dict, sorted_unused_bricks[1:])
        
        # If valid, place it into the pyramid
        if is_valid:
            for p in pos:
                new_arr[p] = least_pos_brick
            attempt_count += 1
            # If it is the last brick, return result
            if len(sorted_unused_bricks) == 1:
                return new_arr
            else:
                # If not the last brick, continue to place the next brick
                result = fill(new_arr, new_brick_pos_dict, new_sorted_unused_bricks) 
                if result != 'Fail':
                    return result
    # If all the placements of the least_pos_brick are invalid
    return 'Fail'

def init_check_valid(pos, arr, fixed, current_brick, unused_bricks, init_brick_pos_dict):
    """
    Initial validity check for brick positions based on the initial arrangement.

    Args:
        pos (list): Potential position for the current brick.
        arr (list): Current state of the pyramid.
        fixed (list): Indices where the current brick is already fixed.
        current_brick (str): The brick being placed.
        unused_bricks (list): List of bricks not yet placed.
        init_brick_pos_dict (dict): Initial dictionary of possible positions for each brick.

    Returns:
        bool: True if the position is valid, False otherwise.
    """
    # Ensure fixed positions are included in pos
    for i in fixed:
        if i not in pos:
            return False
    # Ensure pos does not overlap with other bricks
    for p in pos:
        if arr[p] != '.' and p not in fixed:
            return False
        
    # Ensure ques+pos is not a dead end
    new_arr = arr.copy()
    for p in pos: new_arr[p] = current_brick
    all_space = set()
    for i, a in enumerate(new_arr):
        if a == '.' or (a in unused_bricks and a!= current_brick): 
            all_space.add(i)

    can_place = set()
    for brick in unused_bricks:
        if brick != current_brick:
            ok_pos_cnt = 0
            for _pos in init_brick_pos_dict[brick]:
                for p in _pos:
                    if new_arr[p] != '.' and new_arr[p] != brick: 
                        break
                else:
                    for p in _pos: can_place.add(p)
                    ok_pos_cnt += 1
            if ok_pos_cnt == 0: return False
    if can_place != all_space: return False
    return True

def fill_check_valid(pos, arr, current_brick, brick_pos_dict, sorted_unused_bricks):
    """
    Check if the brick can be placed at the given positions in the current arrangement.

    Args:
        pos (list): Potential position for the current brick.
        arr (list): Current state of the pyramid.
        current_brick (str): The brick being placed.
        brick_pos_dict (dict): Dictionary of possible positions for each brick.
        sorted_unused_bricks (list): List of unused bricks sorted by number of possible positions.

    Returns:
        tuple: (is_valid, new_sorted_unused_bricks, new_brick_pos_dict)
    """
    # Ensure pos does not overlap with other bricks
    for p in pos:
        if arr[p] != '.' and arr[p] != current_brick:
            return False, [], {} 
        
    # If it is the last brick, then there are no other unused bricks to return
    if len(sorted_unused_bricks) == 0: return True, [], {}

    # Ensure ques+pos is not a dead end
    new_arr = arr.copy()
    for p in pos: new_arr[p] = current_brick
    all_space = set()
    for i, a in enumerate(new_arr):
        if a == '.' or (a in sorted_unused_bricks and a!= current_brick): 
            all_space.add(i)

    can_place = set()
    new_brick_pos_dict = {}
    brick_ok_pos_num = []

    for brick in sorted_unused_bricks:
        ok_pos = []
        for pos in brick_pos_dict[brick]:
            # print(pos)
            for p in pos:
                if new_arr[p] != '.' and arr[p] != brick: 
                    break
            else:
                for p in pos: can_place.add(p)
                ok_pos.append(pos)
        if len(ok_pos) == 0: 
            return False, [], new_brick_pos_dict
        new_brick_pos_dict[brick] = np.array(ok_pos)
        brick_ok_pos_num.append(len(ok_pos))

    if can_place != all_space: 
        return False, [], new_brick_pos_dict

    new_sorted_unused_bricks, brick_ok_pos_num = zip(*sorted(zip(sorted_unused_bricks, brick_ok_pos_num), key=lambda x: x[1]))
    
    return True, new_sorted_unused_bricks, new_brick_pos_dict

def print_arr_in_pyramid(arr):
    """
    Print the question and answer in a pyramid shape.

    Args:
        arr (list): The pyramid arrangement to be printed.
    """
    global brick_name_color_dict

    def print_row(start_indices, lengths):
        for start, length in zip(start_indices, lengths):
            for i in range(start, start + length):
                # print(brick_name_color_dict[arr[i]][1], end='')
                print(arr[i], end='')
            print("   ", end='')
        print()

    print_row([0, 25, 41, 50, 54], [5, 4, 3, 2, 1])
    print_row([5, 29, 44, 52], [5, 4, 3, 2])
    print_row([10, 33, 47], [5, 4, 3])
    print_row([15, 37], [5, 4])
    print_row([20], [5])
    print()

# if __name__ == "__main__":
#     main()