import random, sys

seed = random.randint(0,1000000000000)
random.seed(seed)


# Sees how many neighbors of type symbol item at x,y has (depth = length of search)
def check_neighbors( x, y, symbol, depth):
  
  n = 0
  try: # ul ,u ,ur ,l ,r ,dl ,d ,dr
    if floor[x-1][y-1] == "#" : n += 1 
    if floor[x-1][y]   == "#" : n += 1
    if floor[x-1][y+1] == "#" : n += 1    
    if floor[x][y-1]   == "#" : n += 1 
    if floor[x][y+1]   == "#" : n += 1
    if floor[x+1][y-1] == "#" : n += 1    
    if floor[x+1][y]   == "#" : n += 1
    if floor[x+1][y+1] == "#" : n += 1
  except:
    pass

  return n

def check_cardinals( x, y, symbol, depth):
  
  n = 0

  try: # ul ,u ,ur ,l ,r ,dl ,d ,dr
    if floor[x-1][y]   == "#" : n += 1
    if floor[x][y-1]   == "#" : n += 1 
    if floor[x][y+1]   == "#" : n += 1
    if floor[x+1][y]   == "#" : n += 1
  except:
    pass

  return n

  
def out():
  for x in range( h ):
    sys.stdout.write("\n")
    for y in range( w ):
      if str(floor[x][y]) == "#":
        sys.stdout.write( "#" )
      else:
        sys.stdout.write( str(floor[x][y]) )
        
  sys.stdout.write("\n")


floor = []
#h = 30 # height
#w = 50 # width
h=30
w=50 #30 for seeds

# KEY
# # = wall
# " " = sapce
# E = enemy


# Makes each cell have a 65% chance to become a wall
# Note: 60 is best?
# due to the discriminitory nature of the proccess
for x in range( h ):
  floor.append([])
  
  for y in range( w ):
    
    # Creates walls around side
    if ( y < 1) or ( x < 1) or (y is w - 1) or (x is h - 1):
      floor[x].append("#")
    elif random.randint(0,100) > 50 : # norm 60
      floor[x].append("#")
    else:
      floor[x].append(" ")


# This takes semi-neighbored spaces and tells them to fill in
for x in range( h ):
  for y in range( w ):
    if floor[x][y] is " ": # only check spaces
    
      # Check surrounding tiles
      if check_neighbors( x, y, "#", 1 ) > 4 and random.randint(0,100) > 40: # 50
        floor[x][y] = "#"
        #print "CASE"
    
out()

for x in range( h ):
  for y in range( w ):
    if floor[x][y] is " ": # only check spaces
    
      # Check surrounding tiles
      if check_neighbors( x, y, "#", 1 ) > 5 :
        floor[x][y] = "#"
        #print "CASE2"

    
out()
    
for x in range( h ):
  for y in range( w ):
    if floor[x][y] is "#": # only check spaces
    
      # Check surrounding tiles
      if (check_neighbors( x, y, "#", 1 ) < 2) and ( y > 1) and ( x > 1) and (y != w - 1) and (x != h - 1):
        floor[x][y] = " "
        #print "CASE4"

out()

empty_spaces = []


# Fill early holes
for x in range( h ):
  for y in range( w ):
    if floor[x][y] is " ": # only check spaces
    
      empty_spaces.append([x,y])
    
      # Check surrounding tiles
      if check_neighbors( x, y, " ", 1 ) > 4:
          m_x = x
          m_y = y
          #print "casebreak"



#for z in range(0, len(empty_spaces) - 1):
# determine cells
# find cell closest to cell
# make 1 connection per cell

cells = []
#determine cells
for x in empty_spaces:
  
  if check_neighbors(x[0], x[1], " ", 1) > 0:
    pass


# Boxify the map by removing corners
for x in empty_spaces:
  
  if (x[0] > 2) and (x[0] < h - 2) and (x[1] > 2) and (x[1] < w - 2):
    
    try:
      if floor[x[0]-1][x[1]] == "#" : floor[x[0]-1][x[1]] = " "
      if floor[x[0]][x[1]-1] == "#" : floor[x[0]][x[1]-1] = " " 
      if floor[x[0]][x[1]+1] == "#" : floor[x[0]][x[1]+1] = " "    
      if floor[x[0]+1][x[1]] == "#" : floor[x[0]+1][x[1]] = " "
    except:
      pass


split_empty = []
for x in range( h ):
  for y in range( w ):
    if floor[x][y] is " " and check_neighbors(x, y, "#", 1) > 1: # only check spaces
      split_empty.append([x,y])


# Finally, break apart large rooms with a single connector
for x in split_empty:
  try:
    l = floor[x[0]-1][x[1]]
    r = floor[x[0]+1][x[1]]
    d = floor[x[0]][x[1]-1]
    u = floor[x[0]][x[1]+1]
     
    if (l == r) and (u == d) and (l != (d or u)) and (r != d or u):
      floor[x[0]][x[1]] = "#"
  except:
    pass


# Map now begins cell division, to make sure all empty spaces can be reached

# Reset empty_spaces
cell_spaces = []
cells = []

for x in range( h ):
  for y in range( w ):
    if floor[x][y] is " ": # only check spaces
      cell_spaces.append([x,y])


def define_cell( x, y ):

  # Don't count diagonals 
  curr_cell.append( [x,y] )
  cell_spaces.remove([x,y])
  if (floor[x-1][y]   == " ") and ([x-1,y] not in curr_cell) : define_cell( x-1, y ) 
  if (floor[x][y-1]   == " ") and ([x,y-1] not in curr_cell) : define_cell( x, y-1 ) 
  if (floor[x][y+1]   == " ") and ([x,y+1] not in curr_cell) : define_cell( x, y+1 ) 
  if (floor[x+1][y]   == " ") and ([x+1,y] not in curr_cell) : define_cell( x+1, y ) 


while len(cell_spaces) > 0:
  
  curr_cell = []
  
  define_cell( cell_spaces[0][0], cell_spaces[0][1] )

  cells.append( curr_cell )
  

#curr cell should now have all spaces in cell
room_num = 0
rooms = []
for x in cells:

  #print "Room " + str(room_num) + " is " + str(float(len(x))/float((h*w)) * 100) + "% of the map." 

  # Here we need to eliminate small rooms that comprise less than 1% of the map
  if float(len(x))/float((h*w)) * 100 > 3 or len(cells) < 4: # 1?
  
    for y in x:
      floor[y[0]][y[1]] = str(room_num)

    room_num += 1

    rooms.append(x)

  else: # Else fill in as wall
    
    for y in x:
      floor[y[0]][y[1]] = "#"

new_spaces = []

for x in range( h ):
  sys.stdout.write("\n")
  for y in range( w ):
    if floor[x][y] == "#":
     sys.stdout.write( "." )
    else:
      sys.stdout.write( str(floor[x][y]) )    
sys.stdout.write("\n")


# Calculate average x,y of each room
'''
Known bug -- curvy rooms may place the average outside of the room
'''
avg = []

for x in rooms:
  
  x_sum = 0
  y_sum = 0
  
  for y in x:
    
    x_sum += y[0]
    y_sum += y[1]
    
  x_sum /= len(x)
  y_sum /= len(x)
  
  avg.append([x_sum,y_sum])
  
# Show centers of rooms
for x in avg:
  #print str(x[0]) + "," + str(x[1])
  floor[x[0]][x[1]] = "X"


# Modify to not cross through spaces not contained in f's room
def draw_path( s, f ):
  
  new_spaces = []
  
  while (s[0] != f[0] ) :
    
    if s[0] < f[0]:
      new_spaces.append( [s[0] + 1,s[1]] )
      s[0] +=1
    elif s[0] > f[0]:
      new_spaces.append( [s[0] - 1,s[1]] )
      s[0] -=1
    
  while (s[1] != f[1]) :
    
    if s[1] < f[1]:
      new_spaces.append( [s[0] ,s[1] + 1])
      s[1] +=1
    elif s[1] > f[1]:
      new_spaces.append( [s[0] ,s[1] - 1])
      s[1] -=1

  #print str(s[0]) + " != " + str(f[0]) + " && " + str(s[1]) + " != " + str(f[1])

  for x in new_spaces:
    #print "Changing " + str(floor[x[0]][x[1]])
    floor[x[0]][x[1]] = " "
  


# Sorts rooms by closeness
for x in range(0,len(avg)-1):
  
  b_dist = h*w
  b_index = -1
  
  # Find closest
  for y in range(0,len(avg)-1):
    
    t_dist = abs(avg[y][1] - avg[y+1][1])/(abs(avg[y][0] - avg[y+1][0]) + 1) # +1 to avoid div/0

    if t_dist < b_dist:
      b_dist = t_dist
      b_index = y+1  

  # Switch x + 1 and closest
  temp_room = avg[x+1]  
  avg[x+1] = avg[b_index]
  avg[b_index] = temp_room

for x in range(0,len(avg)-1):
  draw_path(avg[x],avg[x+1])


    
# Show centers of rooms
for x in avg:
  print str(x[0]) + "," + str(x[1])
  floor[x[0]][x[1]] = "X"


# Purge map of room numbers
for x in range( h ):
  for y in range( w ):
    if floor[x][y] != "#":
      floor[x][y] = " "


#########################################################################  
#  Dead End Code
#########################################################################  


print "seed: " + str(seed)

count = 0
for x in rooms:
  print "Room " + str(count) + " : " + str(float(len(x)/float((h*w)) * 100)) + "%"
  count +=1



floor_num = 1
monsters = random.randint(10, floor_num*2+10)

monster_spots = []
for x in range( h ):
  for y in range( w ):
    if floor[x][y] == " " and check_neighbors(x,y," ",1) < 5:
      monster_spots.append([x,y])

# Show monsters as E
for x in range(0,monsters):

  i = monster_spots[random.randint(0,len(monster_spots)-1)]
  floor[i[0]][i[1]] = "E"
  monster_spots.remove(i) 

out()


# Starting and ending spots
start_or_end = []
for x in range( h ):
  for y in range( w ):
    if floor[x][y] == " " and check_neighbors(x,y," ",1) < 5:
      start_or_end.append([x,y])

i = random.randint(0,len(start_or_end))
start = start_or_end[i]

floor[start[0]][start[1]] = "S"

# Find furthest start_or_end canidate for exit
f_dist = 0
f_best = [start_or_end[0][0],start_or_end[0][1]]

for x in range(len(start_or_end)-1):
  
  t_dist = abs(start_or_end[x][0] - f_best[0])/(abs(start_or_end[x][1] - f_best[1]) + 1)
  if t_dist > f_dist:
    f_dist = t_dist
    f_best = start_or_end[x]
        
floor[f_best[0]][f_best[1]] = "F"


out()
