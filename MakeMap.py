from PIL import Image
import random as r
import math

h=100
w=100
known_islands = []

def create_grid(height=10, width=10, populate=True):
    '''
    Creates a height x width array.
    If populate is true randomizes numbers placed in list.
    '''
    grid = []
    
    for _ in range(height):
        temp = []
        
        for _ in range(width):
            temp.append(r.randint(5,99))
        grid.append(temp)
            
    return grid

g = create_grid(height=h, width=w)


def center_bias(grid):
    '''
    Raises the center quarter of the map to increase the chance of being above
    sea level.
    '''
    h = len(grid)
    w = len(grid[0])

    part = 6
    for y in range(int(h / part), (part - 1) * int(h / part)):
        for x in range(int(w / part), (part - 1) * int(w / part)):
            
            grid[x][y] += 4
            
    return grid

#g = center_bias(g)

def add_bump(grid, mode='raise', bounds=1.0, steepness=1.0, size=1.0):
    '''
    Adds a disruption in the terrain
    
    bounds: % bounds of the map it could take up
    steepness: how steep the slope should be
    size: % size of the map the disruption could be
    raise_level: if true, raise. else depress
    '''
    
    # Generate bounds to select the centerpoint for
    m = (1.0 - bounds) / 2
    mod_mag = int(w * bounds)
    
    x_min = 0 + int(w * m)
    x_max = w - (1 * int(w * m))
    
    y_min = 0 + int(h * m)
    y_max = h - (1 * int(h * m))
    
    # Select center point
    r_x = r.randint(x_min, x_max)
    r_y = r.randint(y_min, y_max)


    max_dist = (w / 2) + 2
    max_height_added = int(70 * steepness)

    
    for y in range(x_min, x_max):
        for x in range(y_min, y_max):
    
            # sqrt(x^2 + y^2)
            d_x = r_x - x
            d_y = r_y - y
            
            d_x *= r.uniform(0.5,3)
            d_y *= r.uniform(0.5,3)
            dist = math.sqrt( (d_x)**2 + (d_y)**2 )# + r.randint(5,15)
            #dist = math.sqrt( (d_x)**2 + (d_y)**2 )
            
            #(dist * max_height_added)
            added_height = max_height_added * ((max_dist - dist) / 100)
            
            if mode is 'raise':
                grid[x][y] += added_height
            elif mode is 'lower':
                grid[x][y] -= added_height
    
    return grid
    
g = add_bump(g, mode='raise', bounds=0.8, steepness=1)
#g = add_bump(g, mode='lower', bounds=0.8, steepness=0.4)


def flatten(grid, cutoff=40):
    '''
    Seperates the map into two planes of height
    '''
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            
            if grid[x][y] > cutoff:
                grid[x][y] = 9
            else:
                grid[x][y] = 1
    return grid
    
g = flatten(g)


def cleanup_islands(grid, land=9, sea=1, cutoff=4, rounds=1):
    '''
    Cleanup pieces of land with no surrounding neighbors
    '''
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
    
            n = 0
            if grid[x-1][y-1] == land : n += 1 
            if grid[x-1][y]   == land : n += 1
            if grid[x-1][y+1] == land : n += 1    
            if grid[x][y-1]   == land : n += 1 
            if grid[x][y+1]   == land : n += 1
            if grid[x+1][y-1] == land : n += 1    
            if grid[x+1][y]   == land : n += 1
            if grid[x+1][y+1] == land : n += 1

            if n < cutoff:
                grid[x][y] = sea
                
    if rounds > 0:
        cleanup_islands(grid=grid, land=land, sea=sea,
                      cutoff=cutoff, rounds=(rounds - 1))
                
    return grid

g = cleanup_islands(g, rounds=2)


def fill_land(grid, land=9, sea=1, cutoff=6, rounds=1):
    '''
    Fill in ocean surrounded by land
    '''
    added_land = False
    
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
    
            if grid[x][y] is sea:
                n = 0
                if grid[x-1][y-1] == land : n += 1 
                if grid[x-1][y]   == land : n += 1
                if grid[x-1][y+1] == land : n += 1    
                if grid[x][y-1]   == land : n += 1 
                if grid[x][y+1]   == land : n += 1
                if grid[x+1][y-1] == land : n += 1    
                if grid[x+1][y]   == land : n += 1
                if grid[x+1][y+1] == land : n += 1

                if n > cutoff:
                    grid[x][y] = land
                    added_land = True
                    
                
    if (rounds > 0) and (added_land == True):
        fill_land(grid=grid, land=land, sea=sea,
                      cutoff=cutoff, rounds=(rounds - 1))
                
    return grid

g = fill_land(g, rounds=2)
g = fill_land(g, cutoff=4, rounds=4)


def remove_islands(grid, size_required=0.1):
    '''
    Removes islands on the map that don't make up more than size_required % of
    the map itself
    
    '''
    # First, make a list of all land points
    land_points = []

    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            # If we find land
            if grid[x][y] != 1:
                land_points.append([x,y])
            
    for point in land_points:           
        pass






def raise_shoreline(grid, land=9, sea=1, sand=2, cutoff=1, rounds=1):
    '''
    Fill in ocean surrounded by land
    '''
    added_shoreline = False
    
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
    
            if grid[x][y] is land:
                
                neighbors = [grid[x-1][y-1], grid[x-1][y], grid[x-1][y+1],
                             grid[x][y-1], grid[x][y+1], grid[x+1][y-1],
                             grid[x+1][y], grid[x+1][y+1]]
                
                if neighbors.count(sea) > cutoff:
                    grid[x][y] = sand
                    added_shoreline = True
                    
                
    if (rounds > 0) and (added_shoreline == True):
        raise_shoreline(grid=grid, land=land, sea=sea, sand=sand,
                      cutoff=cutoff, rounds=(rounds - 1))
                
    return grid

g = raise_shoreline(g, rounds=2)


def add_border(grid):

    for x in range(0, len(grid)):
        grid[0][x] = -1
        grid[-1][x] = -1
        grid[x][0] = -1
        grid[x][-1] = -1
    
    return grid
    
g = add_border(g)
        

def create_map(grid=None):
    '''
    Outputs a map based on previous list passed
    '''
    
    ocean = (88, 109, 157)
    land = (79, 110, 39)
    sand = (200, 182, 111)
    border = (47, 45, 40)
    brown= (87, 61, 11)
    
    # Base ocean image
    img = Image.new('RGB', (w, h), color=ocean)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
  
            color = None
            
            if grid[x][y] == -1:
                color = border
            if grid[x][y] == 1:
                color = ocean
            if grid[x][y] == 2:
                color = sand
            if grid[x][y] == 9:
                color = land
  
            img.putpixel((x,y), color)
    
    
    img.save('gen.png')    

create_map(g)
