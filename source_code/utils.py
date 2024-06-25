from itertools import permutations, combinations
import numpy as np
from tqdm import tqdm

def gen_coor():
    """Generate coordinates for the pyramid structure.
     (grid size in x, y is 2; in z is square root of 2)
    
    Returns:
        list: A list of tuples (x, y, z) representing coordinates in the pyramid.
    """
    coor = []
    for i in range(55):
        if i < 25:
            x = (i%5)*2
            y = (i//5)*2
            z = 0
        elif i < 41: # 25+16
            x = 1+((i-25)%4)*2
            y = 1+((i-25)//4)*2
            z = round(pow(2,0.5),3)
        elif i < 50: # 41+9
            x = 2+((i-41)%3)*2
            y = 2+((i-41)//3)*2
            z = round((pow(2,0.5)*2),3)
        elif i < 54: # 50+4
            x = 3+((i-50)%2)*2
            y = 3+((i-50)//2)*2
            z = round((pow(2,0.5)*3),3)
        else: # i == 54
            x = 4
            y = 4
            z = round((pow(2,0.5)*4),3)
        c = (x,y,z)
        coor.append(c)
    return coor

def print_fill_result(pos):
    """Print the pyramid structure with filled positions.
    
    Args:
        pos (list): A list of indices representing filled positions in the pyramid.
    """
    global brick_name_color_dict

    def print_row(start_indices, lengths):
        for start, length in zip(start_indices, lengths):
            for i in range(start, start + length):
                print_fill_type(i, pos)
            print("   ", end='')
        print()

    print_row([0, 25, 41, 50, 54], [5, 4, 3, 2, 1])
    print_row([5, 29, 44, 52], [5, 4, 3, 2])
    print_row([10, 33, 47], [5, 4, 3])
    print_row([15, 37], [5, 4])
    print_row([20], [5])
    print()

def print_fill_type(index, pos):
    """Print a single position in the pyramid structure.
    
    Args:
        index (int): The index of the position to print.
        pos (list): A list of indices representing filled positions in the pyramid.
    """
    if index in pos:
        print("■ ", end='')
    else:
        print("□ ", end='')

def distance(coor,x,y):
    """Calculate Euclidean distance between two points in the pyramid.
    
    Args:
        coor (list): A list of tuples (x, y, z) representing coordinates.
        x (int): Index of the first point in coor.
        y (int): Index of the second point in coor.
    
    Returns:
        float: The Euclidean distance between points x and y.
    """
    d_square = pow((coor[x][0] - coor[y][0]),2) + pow((coor[x][1] - coor[y][1]),2) + pow((coor[x][2] - coor[y][2]),2)
    d = round(pow(d_square,0.5),2)
    return d

def find_pos(coor, brick, d_comb):
    """Find all possible positions for a brick in the pyramid.
    
    Args:
        coor (list): A list of tuples (x, y, z) representing coordinates.
        brick (list): A list of indices representing a brick's shape.
        d_comb (list): A list of distances between brick components.
    
    Returns:
        np.array: An array of tuples, each representing a valid position for the brick.
    """
    l = len(brick)
    pos = []
    perm = permutations(list(range(0,55)), l)

    if l == 5:
        total = 55*54*53*52*51
    elif l == 4:
        total = 55*54*53*52
    else:
        total = 55*54*53

    with tqdm(total=total) as pbar:
        for p in tqdm(perm):
            pbar.update(1)

            comb = combinations(p, 2)
            i = 0
            fit = True
            for c in comb:
                if distance(coor, c[0], c[1]) != d_comb[i]:
                    fit = False
                    break
                else:
                    i+=1
            if(fit):
                pos.append(p)

    print(f"\n-----------FINISH------total: {len(pos)} arrangements -----------------")
    return np.array(pos)

def get_brick_distance(coor, brick):
    """Get all pairwise distances within a brick.
    
    Args:
        coor (list): A list of tuples (x, y, z) representing coordinates.
        brick (list): A list of indices representing a brick's shape.
    
    Returns:
        list: A list of distances between all pairs of points in the brick.
    """
    d_comb = []
    comb = combinations(brick, 2)
    for c in comb:
        d_comb.append(distance(coor, c[0],c[1]))
    return d_comb

def find_combine(coor, brick1_path, brick2_path, overlap_for_b1, tight):
    """Find valid combinations of two bricks to form a larger brick.
    
    Args:
        coor (list): A list of tuples (x, y, z) representing coordinates.
        brick1_path (str): File path to the first brick's positions.
        brick2_path (str): File path to the second brick's positions.
        overlap_for_b1 (list): List indicating which parts of brick1 should overlap with brick2.
        tight (list): List of tuples (i, j, d) specifying tight distance constraints.
    
    Returns:
        np.array: An array of lists, each representing a valid combined brick.
    """
    brick1 = np.load(brick1_path)
    brick2 = np.load(brick2_path) 
    total = len(brick1)*len(brick2)
    
    pos = []
    with tqdm(total=total) as pbar:
        for b1 in brick1:
            for b2 in brick2:
                pbar.update(1)
                
                p = []
                if(test_correct_comb(coor,b1,b2,overlap_for_b1,tight) == True):
                    for i in range(len(b1)):
                        if overlap_for_b1[i] == -1: # not overlap
                            p.append(b1[i])
                    for i in b2:
                        p.append(i)
                if len(p) != 0:
                    pos.append(p)
    final_result = eli_same(pos)

    return final_result
            
def test_correct_comb(coor,b1,b2,overlap_for_b1,tight):
    """Test if two bricks can be correctly combined based on overlap and tight constraints.
    
    Args:
        coor (list): A list of tuples (x, y, z) representing coordinates.
        b1 (list): A list of indices representing the first brick's position.
        b2 (list): A list of indices representing the second brick's position.
        overlap_for_b1 (list): List indicating which parts of b1 should overlap with b2.
        tight (list): List of tuples (i, j, d) specifying tight distance constraints.
    
    Returns:
        bool: True if the combination is valid, False otherwise.
    """
    for i in range(len(b1)):
        if overlap_for_b1[i] == -1: # not overlap
            if b1[i] in b2: # but overlap
                return False
        else: # overlap
            if b1[i] != b2[overlap_for_b1[i]]: # not the same
                return False
    
    for i in range(len(tight)):
        if distance(coor, b1[tight[i][0]], b2[tight[i][1]]) != tight[i][2]:
            return False
    return True

def eli_same(pos):
    """Eliminate duplicate positions.
    
    Args:
        pos (list): A list of possible positions (each a list of indices).
    
    Returns:
        np.array: An array of unique positions.
    """
    num_of_pos = len(pos)
    sorted_pos = []
    for p in pos:
        sorted_pos.append(sorted(p))
    final_result = []
    for i in range(num_of_pos):
        p = sorted_pos.pop(0)
        if p not in sorted_pos:
            final_result.append(pos[i])
    print_fill_result(final_result[0])
    print(f"\n-----------FINISH------total: {len(final_result)} different arrangements -----------------")
    return np.array(final_result)