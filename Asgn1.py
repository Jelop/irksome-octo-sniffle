import bpy
import random
import math
import time

PLANE_ROW = 11
PLANE_COL = 11
GRID = 2
STREET = 1
BLOCKS = [[0 for i in range(PLANE_ROW)] for j in range(PLANE_COL)]
ZONE_FACTOR = (PLANE_ROW-1)/2

def chance_selector(chance):
    if random.uniform(0,1) < chance:
        return True
    return False

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
        #print(faces)
    mesh.from_pydata(verts, [], faces)
    #snap origin to itself here
    bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS')
    mesh.update()
    return obj

bpy.ops.object.select_pattern()
bpy.ops.object.delete()

for i in range(0, PLANE_ROW):   
    for j in range(0, PLANE_COL):
        
        x = ((i-(PLANE_ROW/2)) * GRID) + (STREET * i)
        y = ((j-(PLANE_COL/2)) * GRID) + (STREET * j)

        verts = [[x, y, 0],[x, y + GRID, 0], [x + GRID, y + GRID, 0], [x + GRID, y, 0]]
        BLOCKS[i][j] = create_block('block' + str(i) + str(j), (0,0,0), verts)  
        

bpy.ops.transform.translate(value = (-(PLANE_ROW-1)/2, -(PLANE_COL-1)/2, 0))


for i in range(0, PLANE_ROW):
    for j in range(0, PLANE_COL):
        zone = max(math.fabs(i - ZONE_FACTOR) , math.fabs(j - ZONE_FACTOR))
        cosIn = (math.pi/ZONE_FACTOR) * zone
        chance = (math.cos(cosIn) + 1) / 2
        
        block_origin = BLOCKS[i][j].location
        max_height = 10 - zone
        if chance_selector(chance):
            block = bpy.ops.mesh.primitive_cube_add(location = (block_origin.x, block_origin.y, 0))
            select_object(block)
            bpy.ops.transform.resize(value = (0.25, 0.25, random.uniform(max_height/2, max_height)))
            block_ref = bpy.context.active_object
            block_ref.location.z += block_ref.dimensions.z/2
            
'''
bpy.context.selected_objects.clear()
for i in range(0, PLANE_ROW):   
    for j in range(0, PLANE_COL):
        select_object(BLOCKS[i][j])
        bpy.ops.transform.translate(-(PLANE_ROW - 1)/2, -(PLANE_COL - 1)/2, 0)
   '''     
'''
for i in range (-5, 6):
    for j in range (-5, 6):
        block = bpy.ops.mesh.primitive_cube_add(location = (0 + i, 0 + j, 0))
        select_object(block)
        bpy.ops.transform.resize(value = (0.25, 0.25, random.uniform(0.5, 3)))
        block_ref = bpy.context.active_object
        block_ref.location.z += block_ref.dimensions.z/2
        '''
         