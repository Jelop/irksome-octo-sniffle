import bpy
import math
import random

PLANE_ROW = 10
PLANE_COL = 10
STREET_WIDTH = 0.2
WIDTH_RAND = 0.2
STRAIGHT_WIDTH_MAX = 2
POINT_WIDTH_MAX = 2
HEIGHT_RAND = 0.2
STRAIGHT_HEIGHT_MAX = 2
POINT_HEIGHT_MAX = 2

blocks_array = []
col = 0

def obtain_ref(object):
    select_object(object)
    return bpy.context.active_object
    
def select_object(object):
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(object)
    return

def create_block(name, origin, verts):
    mesh = bpy.data.meshes.new(name+'Mesh')
    obj = bpy.data.objects.new(name, mesh)
    obj.location = origin
    
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.objects.active = obj
    obj.select = True
    faces = [[]]
    for i in range (len(verts)):
        faces[0].append(i,)
        print(faces)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    return obj

def position_vertex(row, col, num, vert_num, vert_ref, col_index):
    vertex = [0,0,0]
    if row == 0 and col == 0:
        if num == 0:
            vertex[0] = 0 - PLANE_ROW/2
            vertex[1] = 0 - PLANE_COL/2
        if num == 1:
            vertex[0] = 0 - PLANE_ROW/2
            vertex[1] = vert_ref[0][1] + random.uniform(WIDTH_RAND, STRAIGHT_WIDTH_MAX)
        if num == 2:
            if vert_num == 3:
                vertex[0] = vert_ref[0][0] + random.uniform(HEIGHT_RAND, POINT_HEIGHT_MAX)
                vertex[1] = vert_ref[0][1] if random.uniform(0,1) <= 0.5 else vert_ref[1][1]
            if vert_num == 4 or vert_num == 5:
                vertex[0] = vert_ref[1][0] + random.uniform(HEIGHT_RAND, STRAIGHT_HEIGHT_MAX)
                vertex[1] = vert_ref[1][1]
        if num == 3:
            if vert_num == 4:
                vertex[0] = vert_ref[2][0]
                vertex[1] = vert_ref[0][0]
            if vert_num == 5:
                vertex[0] = vert_ref[2][0] + random.uniform(HEIGHT_RAND, POINT_HEIGHT_MAX)
                vertex[1] = random.uniform(vert_ref[0][1], vert_ref[2][1])
        if num == 4:
            vertex[0] = vert_ref[2][0]
            vertex[1] = vert_ref[0][0]
            
  
    elif row == 0:
        if num == 0:
            vertex[0] = 0 - PLANE_ROW/2
            block_ref = obtain_ref(blocks_array[row][col_index - 1])
            vertex[1] = block_ref.data.vertices[1].co.y + STREET_WIDTH
        if num == 1:
            vertex[0] = 0 - PLANE_ROW/2
            vertex[1] = (vert_ref[0][1] + random.uniform(WIDTH_RAND, STRAIGHT_WIDTH_MAX)) % PLANE_COL
        if num == 2:
            
            
        
        
        
              
    vertex[2] = 0;
    return vertex
  
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

#plane = bpy.ops.mesh.primitive_plane_add()
print ("hello")

#verts = [[-1,-1,0],[-1,1,0],[1,1,0],[random.uniform(1,3),random.uniform(-1,1),0],[1,-1,0]]
#create_block('plane1', (0,0,0), verts)



for row in range (0, 10):
    
    col_index = 0
    col = 0 #keeps track of row units, used for varible length rows
    #for col in range(int((-col_max/2)), int((col_max - col_max/2))):
    #while col < PLANE_COL:
    while col_index < 1:
        vert_chance = random.uniform(0, 1)
        if vert_chance > 0.2:
           vert_num = 4
        elif vert_chance > 0.1 and vert_chance <= 0.2:
            vert_num = 5
        else:
            vert_num = 3
        
        #max_width = col/PLANE_COL
        
        #need to figure out origin. Depends on position in grid... Equidistant from 
        # nearest points in blocks_array[row][col-1] and blocks_array[row-1][col]?
        blocks_array.append([0])
        verts = [[0 for x in range(3)]for y in range(vert_num)]
        #second point needs to be equidistant from the block above and above right?
        # 3rd / 5th is dependent? 
        for i in range (vert_num):
            verts[i] = position_vertex(row, col, i, vert_num, verts, col_index)
            
        col += verts[1][1] + STREET_WIDTH
        name = 'block' + str(row) + str(col_index)   
        blocks_array[row][col_index] = create_block(name, (0,0,0), verts) 
        col_index+= 1
        
        block_ref = obtain_ref(blocks_array[row][col_index -1])
        print(block_ref.data.vertices[2].co.y) # gets a given vertex's coordinate 
        #blocks_array[row][col] = 
        
        
'''
for i in range (-5, 6):
    for j in range (-5, 6):
        block = bpy.ops.mesh.primitive_cube_add(location = (0 + i, 0 + j, 0))
        select_object(block)
        bpy.ops.transform.resize(value = (0.25, 0.25, random.uniform(0.5, 3)))
        block_ref = bpy.context.active_object
        block_ref.location.z += block_ref.dimensions.z/2
        '''