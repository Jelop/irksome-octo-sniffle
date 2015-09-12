import bpy
import random
import math
import time

PLANE_ROW = 15
PLANE_COL = 15
GRID = 2
BLOCK_HEIGHT = 0.1
STREET = 1
BLOCKS = [[0 for i in range(PLANE_ROW)] for j in range(PLANE_COL)]
ZONE_FACTOR = (PLANE_ROW-1)/2
NUM_ZONES = ZONE_FACTOR + 1
ZONE_THRESH = []

def get_world_vert(num, row, col):
    block_ref = BLOCKS[row][col]
    return block_ref.matrix_world * block_ref.data.vertices[num].co

def calc_zone_thresh():
    for i in range(0, int(NUM_ZONES)):
        cosIn = (math.pi/2)*((ZONE_FACTOR - i)/ZONE_FACTOR)
        ZONE_THRESH.append(math.cos(cosIn))

def rbt_non_uniform(zone):
    chance = random.uniform(0,1)
    if zone == 0:
        return 1
    elif zone == ZONE_FACTOR:
        return -1
    else:
        if chance > ZONE_THRESH[zone]:
            return 1
        else:
            rb_chance = random.uniform(0, ZONE_THRESH[zone])
            if rb_chance > ZONE_THRESH[zone-1] :
                return 0
            else:
                return -1

def rbt_uniform(zone):
    chance = random.uniform(0,1)
    if zone == 0:
        return 1
    elif zone == ZONE_FACTOR:
        return -1
    else:
        if chance > ZONE_THRESH[zone]:
            return 1
        elif chance > ZONE_THRESH[zone-1] and chance < ZONE_THRESH[zone]:
            return 0
        else:
            return -1
        
def chance_selector(chance):
    if random.uniform(0,1) < chance:
        return True
    return False

def select_object(object):
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(object)
    return

def create_block(name, origin, verts, faces):
    mesh = bpy.data.meshes.new(name+'Mesh')
    obj = bpy.data.objects.new(name, mesh)
    obj.location = origin
    
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.objects.active = obj
    obj.select = True
    #faces = [[]]
    #for i in range (len(verts)):
    #    faces[0].append(i,)
    #    #print(faces)
    mesh.from_pydata(verts, [], faces)
    #snap origin to itself here
    bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS')
    mesh.update()
    return obj

bpy.ops.object.select_pattern()
bpy.ops.object.delete()

start_time = time.time()

for i in range(0, PLANE_ROW):   
    for j in range(0, PLANE_COL):
        
        x = ((i-(PLANE_ROW/2)) * GRID) + (STREET * i)
        y = ((j-(PLANE_COL/2)) * GRID) + (STREET * j)

        verts = [[x, y, 0],[x, y + GRID, 0], [x + GRID, y + GRID, 0], [x + GRID, y, 0],
                [x, y, BLOCK_HEIGHT],[x, y + GRID, BLOCK_HEIGHT], [x + GRID, y + GRID,
                BLOCK_HEIGHT], [x + GRID, y, BLOCK_HEIGHT]]
        faces = [[0,1,2,3], [0,4,5,1], [1,5,6,2], [2,6,7,3], [3,7,4,0], [4,5,6,7]]
        BLOCKS[i][j] = create_block('block' + str(i) + str(j), (0,0,0), verts, faces)  
        

bpy.ops.transform.translate(value = (-(PLANE_ROW-1)/2, -(PLANE_COL-1)/2, 0))

calc_zone_thresh()
#for thresh in ZONE_THRESH:
#    print(thresh)
    

for i in range(0, PLANE_ROW):
    for j in range(0, PLANE_COL):
        zone = int(max(abs(i - ZONE_FACTOR) , abs(j - ZONE_FACTOR)))
        
        #cosIn =  (math.pi/2) * ((ZONE_FACTOR + 1) - zone)/(ZONE_FACTOR + 1)
        #chance = math.cos(cosIn)
        #cosIn = (math.pi/ZONE_FACTOR) * zone
        #chance = (math.cos(cosIn) + 1) / 2
        
        block_origin = BLOCKS[i][j].location
        max_height = 10 - zone
        #building = rbt_uniform(zone)
        building = rbt_non_uniform(zone)
        
        if building == 1:
            block = bpy.ops.mesh.primitive_cube_add(location = (block_origin.x, block_origin.y, BLOCK_HEIGHT))
            select_object(block)
            bpy.ops.transform.resize(value = (0.25, 0.25, random.uniform(max_height/2, max_height)))
            block_ref = bpy.context.active_object
            block_ref.location.z += block_ref.dimensions.z/2
            
        elif building == 0:
            block = bpy.ops.mesh.primitive_cube_add(location = (block_origin.x, block_origin.y, BLOCK_HEIGHT))
            select_object(block)
            bpy.ops.transform.resize(value = (0.5, 0.8, random.uniform(2,4)))
            block_ref = bpy.context.active_object
            block_ref.location.z += block_ref.dimensions.z/2
        else:
            block = bpy.ops.mesh.primitive_cube_add(location = (block_origin.x, block_origin.y, BLOCK_HEIGHT))
            select_object(block)
            bpy.ops.transform.resize(value = (0.4, 0.4, random.uniform(0.5,2)))
            block_ref = bpy.context.active_object
            block_ref.location.z += block_ref.dimensions.z/2
            
#verts = [BLOCKS[0][0].data.vertices[0], BLOCKS[0][PLANE_COL-1].data.vertices[1], #BLOCKS[PLANE_ROW-1][PLANE_COL-1].data.vertices[2], BLOCKS[PLANE_ROW-1][0].data.vertices[3]]

#verts = [[BLOCKS[0][0].data.vertices[0].co.x, BLOCKS[0][0].data.vertices[0].co.y, 0],
#[BLOCKS[0][PLANE_COL-1].data.vertices[1].co.x, 
#BLOCKS[0][PLANE_COL-1].data.vertices[1].co.y, 0], 
#[BLOCKS[PLANE_ROW-1][PLANE_COL-1].data.vertices[2].co.x, 
#BLOCKS[PLANE_ROW-1][PLANE_COL-1].data.vertices[2].co.y, 0],
#[BLOCKS[PLANE_ROW-1][0].data.vertices[3].co.x,
#BLOCKS[PLANE_ROW-1][0].data.vertices[3].co.y, 0]]

verts = [get_world_vert(0,0,0), get_world_vert(1,0,PLANE_COL-1), get_world_vert(2, PLANE_ROW-1, PLANE_COL-1), get_world_vert(3, PLANE_ROW-1, 0)]

faces = [[0,1,2,3]]
road = create_block('road', (0,0,0), verts, faces)


mat = bpy.data.materials.new("roadMat")
mat.diffuse_color = (0.014,0.014,0.014)
mat.diffuse_shader = 'LAMBERT' 
mat.diffuse_intensity = 0.545
mat.specular_color = (1,1,1)
mat.specular_shader = 'COOKTORR'
mat.specular_intensity = 0.0
mat.alpha = 1
mat.ambient = 1

roadTex = bpy.data.textures.new('roadTex', type = 'NOISE')
mtex = mat.texture_slots.add()
mtex.texture = roadTex
mtex.color = (0.139,0.145,0.145)
mtex.texture_coords = 'UV'
mtex.use_map_color_diffuse = True 
   # mtex.use_map_color_emission = True 
mtex.diffuse_color_factor = 1.0
    #mtex.use_map_density = True 
mtex.mapping = 'FLAT' 
    
road.data.materials.append(mat)

bpy.ops.object.lamp_add(type = "SUN", location = (PLANE_ROW+10, 0, 15))


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
print("Generation time = " , time.time() - start_time)