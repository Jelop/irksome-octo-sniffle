# Joshua La Pine 
# COSC450 Asgn1
# 14 September 2015
# Procedural City Generation Script

import bpy
import random
import math
import time

#GLOBALS
PLANE_ROW = 11
PLANE_COL = 11
GRID = 2
BLOCK_HEIGHT = 0.1
STREET = 0.5
BLOCKS = [[0 for i in range(PLANE_ROW)] for j in range(PLANE_COL)]
ZONE_FACTOR = (PLANE_ROW-1)/2
NUM_ZONES = ZONE_FACTOR + 1
ZONE_THRESH = []

# Used to texture the road plane underneath the city, just to keep things tidy
def texture_plane(object):

    mat = bpy.data.materials.new("roadMat")
    mat.diffuse_color = (0.014,0.014,0.014)
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 0.545
    mat.specular_color = (1,1,1)
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.0
    mat.alpha = 1
    mat.ambient = 1

    planeTex = bpy.data.textures.new('planeTex', type = 'NOISE')
    mtex = mat.texture_slots.add()
    mtex.texture = planeTex
    mtex.color = (0.139,0.145,0.145)
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.diffuse_color_factor = 1.0
    mtex.mapping = 'FLAT' 
    
    object.data.materials.append(mat)
    
    return

# Applies a colour material and noise texture to the given object, colour determined
# by the num argument
def texture_object(object, num):
     
    if num == 1:
        mat = bpy.data.materials.new("blue")
        mat.diffuse_color = (0.029,0.142,0.311)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
     
    elif num == 2:
        mat = bpy.data.materials.new("light_brown")
        mat.diffuse_color = (0.150,0.127,0.123)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
        
    elif num == 3:
        mat = bpy.data.materials.new("build_green")
        mat.diffuse_color = (0.080,0.150,0.103)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
        
    elif num == 4:
        mat = bpy.data.materials.new("deep_purple")
        mat.diffuse_color = (0.171,0.101,0.153)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
        
    elif num == 5:
        mat = bpy.data.materials.new("slate")
        mat.diffuse_color = (0.472,0.410,0.397)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
        
    elif num == 6:
        mat = bpy.data.materials.new("red")
        mat.diffuse_color = (0.692,0.085,0.091)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
        
    elif num == 7:
        mat = bpy.data.materials.new("pale_yellow")
        mat.diffuse_color = (0.990,1.000,0.238)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.126
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.033
        mat.emit = 0.16
        mat.alpha = 1
        mat.ambient = 1
        
     
    buildingTex = bpy.data.textures.new('buildingTex', type = 'NOISE')
    mtex = mat.texture_slots.add()
    mtex.texture = buildingTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = False
    mtex.mapping = 'FLAT'
    mtex.use_map_normal = True
    mtex.normal_factor = 0.565
    
    object.data.materials.append(mat)
    
    return

# Given an object reference and a vertex number its world coordinates are returned
def general_get_world(object_ref, num):
    return object_ref.matrix_world * object_ref.data.vertices[num].co

# Same as above but used only for blocks. Earlier code, not worth rewriting.
def get_world_vert(num, row, col):
    block_ref = BLOCKS[row][col]
    return block_ref.matrix_world * block_ref.data.vertices[num].co

# Calculates the building thresholds for each zone according to the cosine function
def calc_zone_thresh():
    for i in range(0, int(NUM_ZONES)):
        cosIn = (math.pi/2)*((ZONE_FACTOR - i)/ZONE_FACTOR)
        ZONE_THRESH.append(math.cos(cosIn))

# Given a zone number this function returns which type of building should be rendered
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
            
# Creates a cube and then scales and translates it according to given arguments,
# Is set up to handle most common cases when given specific input            
def create_quad(loc, resize, translation, calc_scale):
    block = bpy.ops.mesh.primitive_cube_add(location = loc)
    select_object(block)
    block_ref = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT')
    if calc_scale:
        resize[2] = resize[2] / block_ref.dimensions.z
    bpy.ops.transform.resize(value = resize)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if translation[2] == -100:
       translation[2] = block_ref.dimensions.z/2
    bpy.ops.transform.translate(value = translation)
    block_ref.data.update()
    return block_ref
   
# Returns a random element from a given list, used to ensure different colours
# are assigned to different parts of buildings 
def choose_element(list):
    num = random.randint(0,len(list)-1)
    return list[num]

# Creates a tower building based on the given critera.
def generate_tower(block, origin, size, max_height):
    
    #Size of the block
    if size == 4:
        
        #Used to produces several different types of tower
        type = random.randint(1,3)
        
        if type == 1:
            
            block_ref1 = create_quad(sub_origin,
            [0.6,0.6,random.uniform(max_height/2,max_height)], [-0.3, -0.3,-100], False)
            texture_object(block_ref1, 1)
            topright = general_get_world(block_ref1, 2)
            botright = general_get_world(block_ref1, 6)
            botleft = general_get_world(block_ref1, 4)
            
            new_height = random.uniform((block_ref1.dimensions.z/3)*2, 
            (block_ref1.dimensions.z/4) *3)
            block_ref2 = create_quad((topright.x + (abs(botright.x - topright.x)/2),
            topright.y, 0), [0.40, 0.40,new_height], [0,0,-100], True)
             
            new_height = random.uniform((block_ref1.dimensions.z/3)*2,
            (block_ref1.dimensions.z/4)*3)
            block_ref3 = create_quad((botright.x, botleft.y + (abs(botright.y - botleft.y)/2), 0),
            [0.35, 0.35,new_height], [0,0,-100], True)
            
            
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
            texture_object(block_ref3, num2)
         
        elif type == 2:
            
            height = random.uniform(max_height/2, max_height)
            seg_height = height / 9
            
            num1 = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num1)
            num2 = choose_element(elements)
            
            prev_block_z = 0;
            
            for i in range(0, 9):
                
                block1 = bpy.ops.mesh.primitive_cube_add(location = sub_origin)
                select_object(block1)
                bpy.ops.object.mode_set(mode = 'EDIT')
                if i == 8:
                    bpy.ops.transform.resize(value = (0.9-(i*0.1), 0.9-(i*0.1), seg_height/2))
                else:
                    bpy.ops.transform.resize(value = (0.9-(i*0.1), 0.9-(i*0.1), seg_height))
                bpy.ops.object.mode_set(mode = 'OBJECT')
                block_ref1 = bpy.context.active_object
                if i == 0:
                    bpy.ops.transform.translate(value = (0,0,block_ref1.dimensions.z/2))
                else:
                    bpy.ops.transform.translate(value = (0,0,prev_block_z + seg_height))
                
                texture_object(block_ref1, num1 if i%2 == 0 else num2)
                prev_block_z = block_ref1.location.z
                block_ref1.data.update()
                
        elif type == 3:
            block_ref1 = create_quad(sub_origin, [0.9,0.9,random.uniform(max_height/2,max_height)],
            [0,0,-100], False)
            
            toptopleft = general_get_world(block_ref1, 1)
            topbotright = general_get_world(block_ref1, 7)
            
            block_ref2 = create_quad((toptopleft.x + (abs(topbotright.x-toptopleft.x)/2),
            toptopleft.y + (abs(topbotright.y - toptopleft.y)/2), toptopleft.z), 
            [0.4,0.4,0.4],[0,0,0], False)
            
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
            
            
    elif size == 2:
        
        type = random.randint(1, 3)
        vertical = abs(block[2] - block[0])
        horizontal = abs(block[3]-block[1])
        
        if type == 1:
            if vertical > horizontal:
                
                block_ref1 = create_quad(sub_origin, [0.5, 0.25,
                random.uniform(max_height/2,max_height)], [0,0,-100], False)
  
                botright = general_get_world(block_ref1, 6)
                botleft = general_get_world(block_ref1, 4)
             
                new_height = random.uniform((block_ref1.dimensions.z/3)*2,
                (block_ref1.dimensions.z/4) *3)
                block_ref2 = create_quad((botright.x, botleft.y + (abs(botright.y - botleft.y)/2), 0), [0.3,0.1,new_height], [0,0,-100], True)
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)

            else:
                
                block_ref1 = create_quad(sub_origin, [0.25, 0.5,
                random.uniform(max_height/2,max_height)], [0,0,-100], False)
                
                topleft = general_get_world(block_ref1, 0)
                botleft = general_get_world(block_ref1, 4)
             
             
                new_height = random.uniform((block_ref1.dimensions.z/3)*2,
                (block_ref1.dimensions.z/4) *3)
                block_ref2 = create_quad((topleft.x + (abs(botleft.x - topleft.x)/2), 
                topleft.y,0), [0.1,0.3,new_height], [0,0,-100], True)
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
                
        elif type == 2:
            
             if vertical > horizontal:
                
                block_ref1 = create_quad(sub_origin, [0.5, 0.2,
                random.uniform(max_height/2,max_height)], [0,0,-100], False)
  
                topleft = general_get_world(block_ref1, 0)
                botleft = general_get_world(block_ref1, 4)
             
                new_height = random.uniform((block_ref1.dimensions.z/3)*2,
                (block_ref1.dimensions.z/4) *3)
                block_ref2 = create_quad((topleft.x + (abs(botleft.x-topleft.x)/2), botleft.y, 0),
                [0.15,0.3,new_height], [0,0,-100], True)
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
  
             else:
                
                block_ref1 = create_quad(sub_origin, [0.2, 0.5,
                random.uniform(max_height/2,max_height)], [0,0,-100], False)
                
                botleft = general_get_world(block_ref1, 4)
                botright = general_get_world(block_ref1, 6)
             
             
                new_height = random.uniform((block_ref1.dimensions.z/3)*2,
                (block_ref1.dimensions.z/4) *3)
                block_ref2 = create_quad((botleft.x, botleft.y +(abs(botright.y - botleft.y)/2),0)
                ,[0.3,0.15,new_height], [0,0,-100], True)
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
                
        elif type == 3:
             
              if vertical > horizontal:
                
                block_ref1 = create_quad(sub_origin, [0.5, 0.075,
                random.uniform(max_height/2,max_height)], [0,-0.09,-100], False)
                
                block_ref2 = create_quad(sub_origin, [0.5, 0.075,
                random.uniform(max_height/2,max_height)], [0,0.09,-100], False)
        
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
             
              else:
                
                block_ref1 = create_quad(sub_origin, [0.075, 0.5,
                random.uniform(max_height/2,max_height)], [-0.09,0,-100], False)
                
                block_ref2 = create_quad(sub_origin, [0.075, 0.5,
                random.uniform(max_height/2,max_height)], [0.09,0,-100], False)
                
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)

    else:
        
        type = random.randint(1,2)
        
        if type == 1:
            block_ref1 = create_quad(sub_origin, [0.3,0.3,random.uniform(max_height/2,max_height)],
            [0,0,-100], False)
            
            toptopleft = general_get_world(block_ref1, 1)
            topbotright = general_get_world(block_ref1, 7)
            
            block_ref2 = create_quad((toptopleft.x + (abs(topbotright.x-toptopleft.x)/2),
            toptopleft.y + (abs(topbotright.y - toptopleft.y)/2), toptopleft.z), 
            [0.15,0.15,0.15],[0,0,0], False)
                   
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
      
        else:         
            block_ref1 = create_quad(sub_origin,
            [0.25,0.25,random.uniform(max_height/2,max_height)],
            [0,0,-100], False)
            
            topleft = general_get_world(block_ref1, 0)
            botright = general_get_world(block_ref1, 6)
            
            midx = topleft.x + (abs(botright.x - topleft.x)/2)
            midy = topleft.y + (abs(botright.y - topleft.y)/2)
            
            new_height = random.uniform((block_ref1.dimensions.z/3)*2,
            (block_ref1.dimensions.z/4) *3)
            
            block_ref2 = create_quad((midx, botright.y, 0), [0.1,0.1,new_height],
            [0,0,-100], True)    
            block_ref3 = create_quad((botright.x, midy, 0), [0.1,0.1,new_height],
            [0,0,-100], True)    
            block_ref4 = create_quad((midx, topleft.y, 0), [0.1,0.1,new_height],
            [0,0,-100], True)    
            block_ref5 = create_quad((topleft.x, midy, 0), [0.1,0.1,new_height],
            [0,0,-100], True)    
           
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
            texture_object(block_ref3, num2)
            texture_object(block_ref4, num2)
            texture_object(block_ref5, num2)
            
            
    return

# Creates a business type building based on the passed arguments
def generate_business(block, origin, size, max_height):
    
    if size == 4:
        
        type = random.randint(1,3)
        if type == 1:
            block_ref1 = create_quad(sub_origin,[0.8,0.5,random.uniform(max_height/2,max_height)],
            [0,-0.3,-100], False)
            break_step = block_ref1.dimensions.z/4 
            block_ref2 = create_quad(sub_origin,[0.85,0.65,0.1],[0,-0.3,break_step], False)
            block_ref3 = create_quad(sub_origin,[0.85,0.65,0.1],[0,-0.3,break_step*2], False)
            block_ref4 = create_quad(sub_origin,[0.85,0.65,0.1],[0,-0.3,break_step*3], False)
            
            topleft = general_get_world(block_ref1, 0)
            botright = general_get_world(block_ref1, 6)
            midx = topleft.x + (abs(botright.x - topleft.x)/2)
            
            new_height = 0.8*block_ref1.dimensions.z
            block_ref5 = create_quad((midx, botright.y, 0), [0.6,0.6,new_height],
            [0,0,-100], True)
            
            toptopleft = general_get_world(block_ref1, 1)
            topbotright = general_get_world(block_ref1, 7)
            
            block_ref6 = create_quad((toptopleft.x + (abs(topbotright.x-toptopleft.x)/2),
            toptopleft.y + (abs(topbotright.y - toptopleft.y)/2), toptopleft.z), 
            [0.45,0.25,0.15],[0,0,0], False)
            
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            elements.remove(num2)
            num3 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
            texture_object(block_ref3, num2)
            texture_object(block_ref4, num2)
            texture_object(block_ref5, num3)
            texture_object(block_ref6, num2)
            
        elif type == 2:
            block_ref1 = create_quad(sub_origin,[0.45,0.8,random.uniform(max_height/2,max_height)],
            [0.3,0,-100], False)
            break_step = block_ref1.dimensions.z/4 
            block_ref2 = create_quad(sub_origin,[0.6,0.9,0.1],[0.3,0,break_step], False)
            block_ref3 = create_quad(sub_origin,[0.6,0.9,0.1],[0.3,0,break_step*2], False)
            block_ref4 = create_quad(sub_origin,[0.6,0.9,0.1],[0.3,0,break_step*3], False)
            
            topleft = general_get_world(block_ref1, 0)
            botright = general_get_world(block_ref1, 6)
            quarter_y = topleft.y + (abs(botright.y - topleft.y)/4)
            quarter3_y = topleft.y + ((abs(botright.y - topleft.y)/4) * 3)
            new_height = 0.9*block_ref1.dimensions.z
            block_ref5 = create_quad((topleft.x-0.2,quarter_y,0), [0.3,0.3,new_height],[0,0,-100], True)
            new_height = 0.9*block_ref1.dimensions.z
            block_ref6 = create_quad((topleft.x-0.2,quarter3_y,0), [0.3,0.3,new_height],[0,0,-100], True)
            
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            elements.remove(num2)
            num3 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
            texture_object(block_ref3, num2)
            texture_object(block_ref4, num2)
            texture_object(block_ref5, num3)
            texture_object(block_ref6, num3)
            
        else:
                    
            block_ref1 = create_quad(sub_origin,[0.8,0.8,random.uniform(max_height/2,max_height)],
            [0.0,0,-100], False)
            break_step = block_ref1.dimensions.z/4 
            block_ref2 = create_quad(sub_origin,[0.9,0.9,0.1],[0,0,break_step], False)
            block_ref3 = create_quad(sub_origin,[0.9,0.9,0.1],[0,0,break_step*2], False)
            block_ref4 = create_quad(sub_origin,[0.9,0.9,0.1],[0,0,break_step*3], False)
        
            num = random.randint(1,5)
            elements = list(range(1,6))
            elements.remove(num)
            num2 = choose_element(elements)
            texture_object(block_ref1, num)
            texture_object(block_ref2, num2)
            texture_object(block_ref3, num2)
            texture_object(block_ref4, num2)
            
    elif size == 2:
        type = random.randint(1,2)
        vertical = abs(block[2] - block[0])
        horizontal = abs(block[3]-block[1])
        
        if type == 1:
            if vertical > horizontal:
                block_ref1 = create_quad(sub_origin,[0.8,0.3,random.uniform(max_height/2,max_height)],
                [0.0,0,-100], False)
                break_step = block_ref1.dimensions.z/4 
                block_ref2 = create_quad(sub_origin,[0.9,0.4,0.1],[0,0,break_step], False)
                block_ref3 = create_quad(sub_origin,[0.9,0.4,0.1],[0,0,break_step*2], False)
                block_ref4 = create_quad(sub_origin,[0.9,0.4,0.1],[0,0,break_step*3], False)
            
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
                texture_object(block_ref3, num2)
                texture_object(block_ref4, num2)
               
            else:
                block_ref1 = create_quad(sub_origin,[0.3,0.8,random.uniform(max_height/2,max_height)],
                [0.0,0,-100], False)
                break_step = block_ref1.dimensions.z/4 
                block_ref2 = create_quad(sub_origin,[0.4,0.9,0.1],[0,0,break_step], False)
                block_ref3 = create_quad(sub_origin,[0.4,0.9,0.1],[0,0,break_step*2], False)
                block_ref4 = create_quad(sub_origin,[0.4,0.9,0.1],[0,0,break_step*3], False)
            
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
                texture_object(block_ref3, num2)
                texture_object(block_ref4, num2)
          
        else:
            if vertical > horizontal:
                block_ref1 = create_quad(sub_origin, [0.8,0.25,random.uniform(max_height/2,max_height)],
                [0.0,0,-100], False)
                break_step = block_ref1.dimensions.z/4 
                block_ref2 = create_quad(sub_origin,[0.9,0.4,0.1],[0,0,break_step], False)
                block_ref3 = create_quad(sub_origin,[0.9,0.4,0.1],[0,0,break_step*2], False)
                block_ref4 = create_quad(sub_origin,[0.9,0.4,0.1],[0,0,break_step*3], False)
                
                topleft = general_get_world(block_ref1, 0)
                botright = general_get_world(block_ref1, 6)
                
                new_height = random.uniform((block_ref1.dimensions.z/3)*2,
                (block_ref1.dimensions.z/4) *3)
                block_ref5 = create_quad((topleft.x+(abs(botright.x-topleft.x)/2), topleft.y,0),
                [0.6,0.2,new_height],
                [0,0,-100], True)
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                elements.remove(num2)
                num3 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
                texture_object(block_ref3, num2)
                texture_object(block_ref4, num2)
                texture_object(block_ref5, num3)
                
            else:
                block_ref1 = create_quad(sub_origin, [0.25,0.8,random.uniform(max_height/2,max_height)],
                [0.0,0,-100], False)
                break_step = block_ref1.dimensions.z/4 
                block_ref2 = create_quad(sub_origin,[0.4,0.9,0.1],[0,0,break_step], False)
                block_ref3 = create_quad(sub_origin,[0.4,0.9,0.1],[0,0,break_step*2], False)
                block_ref4 = create_quad(sub_origin,[0.4,0.9,0.1],[0,0,break_step*3], False)
                
                topleft = general_get_world(block_ref1, 0)
                botright = general_get_world(block_ref1, 6)
                
                new_height = random.uniform((block_ref1.dimensions.z/3)*2,
                (block_ref1.dimensions.z/4) *3)
                block_ref5 = create_quad((botright.x,topleft.y+(abs(botright.y-topleft.y)/2),0),
                [0.2,0.6,new_height], [0,0,-100], True)
                
                num = random.randint(1,5)
                elements = list(range(1,6))
                elements.remove(num)
                num2 = choose_element(elements)
                elements.remove(num2)
                num3 = choose_element(elements)
                texture_object(block_ref1, num)
                texture_object(block_ref2, num2)
                texture_object(block_ref3, num2)
                texture_object(block_ref4, num2)
                texture_object(block_ref5, num3)
                
    else:
        
        block_ref1 = create_quad(sub_origin, [0.25,0.25,random.uniform(max_height/2,max_height)],
        [0.0,0,-100], False)
        break_step = block_ref1.dimensions.z/4 
        block_ref2 = create_quad(sub_origin,[0.3,0.3,0.1],[0,0,break_step], False)
        block_ref3 = create_quad(sub_origin,[0.3,0.3,0.1],[0,0,break_step*2], False)
        block_ref4 = create_quad(sub_origin,[0.3,0.3,0.1],[0,0,break_step*3], False)
    
        toptopleft = general_get_world(block_ref1, 1)
        topbotright = general_get_world(block_ref1, 7)
            
        block_ref5 = create_quad((toptopleft.x + (abs(topbotright.x-toptopleft.x)/2),
        toptopleft.y + (abs(topbotright.y - toptopleft.y)/2), toptopleft.z), 
        [0.15,0.15,0.15],[0,0,0], False)
        
        num = random.randint(1,5)
        elements = list(range(1,6))
        elements.remove(num)
        num2 = choose_element(elements)
        texture_object(block_ref1, num)
        texture_object(block_ref2, num2)
        texture_object(block_ref3, num2)
        texture_object(block_ref4, num2)
        texture_object(block_ref5, num2)
                  
    return

# Creates residential buildings
def generate_residence(block, origin, size):
    
    if size == 4:
        quarter_x = abs(block[2]-block[0])/4
        quarter_y = abs(block[3]-block[1])/4
        origins = []
        origins.append((block[0]+quarter_x, block[1] + quarter_y, BLOCK_HEIGHT))
        origins.append((block[0]+quarter_x, block[1] + (quarter_y*3),BLOCK_HEIGHT))
        origins.append((block[0]+(quarter_x*3), block[1] + quarter_y, BLOCK_HEIGHT))
        origins.append((block[0]+(quarter_x*3), block[1] + (quarter_y*3), BLOCK_HEIGHT))
        
        for point in origins:
            block_ref1 = create_quad(point, [0.125,0.125,0.125],[-0.25,-0.25,-100], False)
            roof_height = block_ref1.dimensions.z
            block_ref2 = create_quad(point, [0.15,0.15,0.05],[-0.25,-0.25,roof_height], False)
            texture_object(block_ref1, random.randint(1,7))
            texture_object(block_ref2, random.randint(1,7))
            
            if random.randint(1,3) < 3:
                block_ref3 = create_quad(point, [0.125,0.125,0.125],[-0.25,0.25,-100], False)
                block_ref4 = create_quad(point, [0.15,0.15,0.05],[-0.25,0.25,roof_height], False)
                texture_object(block_ref3, random.randint(1,7))
                texture_object(block_ref4, random.randint(1,7))
                
            if random.randint(1,3) < 3:
                block_ref5 = create_quad(point, [0.125,0.125,0.125],[0.25,0.25,-100], False)
                block_ref6 = create_quad(point, [0.15,0.15,0.05],[0.25,0.25,roof_height], False)
                texture_object(block_ref5, random.randint(1,7))
                texture_object(block_ref6, random.randint(1,7))
                
            if random.randint(1,3) < 3:
                block_ref7 = create_quad(point, [0.125,0.125,0.125],[0.25,-0.25,-100], False)
                block_ref8 = create_quad(point, [0.15,0.15,0.05],[0.25,-0.25,roof_height], False)
                texture_object(block_ref7, random.randint(1,7))
                texture_object(block_ref8, random.randint(1,7))
                 
    elif size == 2:
        vertical = abs(block[2] - block[0])
        horizontal = abs(block[3]-block[1])
        
        if vertical > horizontal:
            
            quarter_x = abs(block[2]-block[0])/4
            half_y = abs(block[3]-block[1])/2
            origins = []
            origins.append((block[0]+quarter_x, block[1] + half_y, BLOCK_HEIGHT))
            origins.append((block[0]+(quarter_x*3), block[1] + half_y, BLOCK_HEIGHT))
            
            for point in origins:
                block_ref1 = create_quad(point, [0.125,0.125,0.125],[-0.25,-0.25,-100], False)
                roof_height = block_ref1.dimensions.z
                block_ref2 = create_quad(point, [0.15,0.15,0.05],[-0.25,-0.25,roof_height], False)
                texture_object(block_ref1, random.randint(1,7))
                texture_object(block_ref2, random.randint(1,7))
            
                if random.randint(1,3) < 3:
                    block_ref3 = create_quad(point, [0.125,0.125,0.125],[-0.25,0.25,-100], False)
                    block_ref4 = create_quad(point, [0.15,0.15,0.05],[-0.25,0.25,roof_height], False)
                    texture_object(block_ref3, random.randint(1,7))
                    texture_object(block_ref4, random.randint(1,7))
            
                if random.randint(1,3) < 3:
                    block_ref5 = create_quad(point, [0.125,0.125,0.125],[0.25,0.25,-100], False)
                    block_ref6 = create_quad(point, [0.15,0.15,0.05],[0.25,0.25,roof_height], False)
                    texture_object(block_ref5, random.randint(1,7))
                    texture_object(block_ref6, random.randint(1,7))
            
                if random.randint(1,3) < 3:
                    block_ref7 = create_quad(point, [0.125,0.125,0.125],[0.25,-0.25,-100], False)
                    block_ref8 = create_quad(point, [0.15,0.15,0.05],[0.25,-0.25,roof_height], False)
                    texture_object(block_ref7, random.randint(1,7))
                    texture_object(block_ref8, random.randint(1,7))
            
        else:
            half_x = abs(block[2]-block[0])/2
            quarter_y = abs(block[3]-block[1])/4
            origins = []
            origins.append((block[0]+half_x, block[1] + quarter_y, BLOCK_HEIGHT))
            origins.append((block[0]+half_x, block[1] + (quarter_y*3), BLOCK_HEIGHT))
            
            for point in origins:
                block_ref1 = create_quad(point, [0.125,0.125,0.125],[-0.25,-0.25,-100], False)
                roof_height = block_ref1.dimensions.z
                block_ref2 = create_quad(point, [0.15,0.15,0.05],[-0.25,-0.25,roof_height], False)
                texture_object(block_ref1, random.randint(1,7))
                texture_object(block_ref2, random.randint(1,7))
            
                if random.randint(1,3) < 3:
                    block_ref3 = create_quad(point, [0.125,0.125,0.125],[-0.25,0.25,-100], False)
                    block_ref4 = create_quad(point, [0.15,0.15,0.05],[-0.25,0.25,roof_height], False)
                    texture_object(block_ref3, random.randint(1,7))
                    texture_object(block_ref4, random.randint(1,7))
                    
                if random.randint(1,3) < 3:
                    block_ref5 = create_quad(point, [0.125,0.125,0.125],[0.25,0.25,-100], False)
                    block_ref6 = create_quad(point, [0.15,0.15,0.05],[0.25,0.25,roof_height], False)
                    texture_object(block_ref5, random.randint(1,7))
                    texture_object(block_ref6, random.randint(1,7)) 
                
                if random.randint(1,3) < 3:
                    block_ref7 = create_quad(point, [0.125,0.125,0.125],[0.25,-0.25,-100], False)
                    block_ref8 = create_quad(point, [0.15,0.15,0.05],[0.25,-0.25,roof_height], False)
                    texture_object(block_ref7, random.randint(1,7))
                    texture_object(block_ref8, random.randint(1,7))
        
    else:
        block_ref1 = create_quad(sub_origin, [0.125,0.125,0.125],[-0.25,-0.25,-100], False)
        roof_height = block_ref1.dimensions.z
        block_ref2 = create_quad(sub_origin, [0.15,0.15,0.05],[-0.25,-0.25,roof_height], False)
        texture_object(block_ref1, random.randint(1,7))
        texture_object(block_ref2, random.randint(1,7))
        
        if random.randint(1,3) < 3:
            block_ref3 = create_quad(sub_origin, [0.125,0.125,0.125],[-0.25,0.25,-100], False)
            block_ref4 = create_quad(sub_origin, [0.15,0.15,0.05],[-0.25,0.25,roof_height], False)
            texture_object(block_ref3, random.randint(1,7))
            texture_object(block_ref4, random.randint(1,7))
        
        if random.randint(1,3) < 3:
            block_ref5 = create_quad(sub_origin, [0.125,0.125,0.125],[0.25,0.25,-100], False)
            block_ref6 = create_quad(sub_origin, [0.15,0.15,0.05],[0.25,0.25,roof_height], False)
            texture_object(block_ref5, random.randint(1,7))
            texture_object(block_ref6, random.randint(1,7))
        
        if random.randint(1,3) < 3:
            block_ref7 = create_quad(sub_origin, [0.125,0.125,0.125],[0.25,-0.25,-100], False)
            block_ref8 = create_quad(sub_origin, [0.15,0.15,0.05],[0.25,-0.25,roof_height], False)
            texture_object(block_ref7, random.randint(1,7))
            texture_object(block_ref8, random.randint(1,7))
        
    return

# Utility method to save typing
def select_object(object):
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(object)
    return

# Creates a mesh from a given set of vertices and faces. Primarily used to create the city blocks
def create_block(name, origin, verts, faces):
    mesh = bpy.data.meshes.new(name+'Mesh')
    obj = bpy.data.objects.new(name, mesh)
    obj.location = origin
    
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.objects.active = obj
    obj.select = True

    mesh.from_pydata(verts, [], faces)
    #snap origin to itself here
    bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS')
    mesh.update()
    return obj

## Start of Execution ##
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

# Generates the city blocks and textures them
for i in range(0, PLANE_ROW):   
    for j in range(0, PLANE_COL):
        
        x = (i * GRID) + (i * STREET)
        y = (j * GRID) + (j * STREET)

        verts = [[x, y, 0],[x, y + GRID, 0], [x + GRID, y + GRID, 0], [x + GRID, y, 0],
                [x, y, BLOCK_HEIGHT],[x, y + GRID, BLOCK_HEIGHT], [x + GRID, y + GRID,
                BLOCK_HEIGHT], [x + GRID, y, BLOCK_HEIGHT]]
        faces = [[0,1,2,3], [0,4,5,1], [1,5,6,2], [2,6,7,3], [3,7,4,0], [4,5,6,7]]
        BLOCKS[i][j] = create_block('block' + str(i) + str(j), (0,0,0), verts, faces)  
        texture_object(BLOCKS[i][j], 5)

# Translates the blocks to be centred around the global origin
block_shift = (-((PLANE_ROW*GRID) + ((PLANE_ROW-1)*STREET))/2, -((PLANE_COL*GRID) + ((PLANE_COL-1)*STREET))/2, 0)
bpy.ops.transform.translate(value = block_shift)

calc_zone_thresh()     

# For each city block
for i in range(0, PLANE_ROW):
    for j in range(0, PLANE_COL):
        zone = int(max(abs(i - ZONE_FACTOR) , abs(j - ZONE_FACTOR)))
        
        SUB_BLOCKS = [[]]
        topleft = get_world_vert(0,i,j)
        botright = get_world_vert(2,i,j)
        
        #Coordinates for each potential sub-block
        bigl = [topleft.x, topleft.y, botright.x, botright.y - (GRID/2)]
        bigr = [topleft.x, topleft.y + (GRID/2), botright.x, botright.y]
        bigt = [topleft.x, topleft.y, botright.x - (GRID/2), botright.y]
        bigb = [topleft.x + (GRID/2), topleft.y, botright.x, botright.y]
        
        tl_box = [topleft.x, topleft.y, topleft.x + (GRID/2), topleft.y + (GRID/2)]
        tr_box = [topleft.x, topleft.y + (GRID/2), botright.x - (GRID/2), botright.y]
        bl_box = [topleft.x + (GRID/2), topleft.y, botright.x, botright.y - (GRID/2)]
        br_box = [topleft.x + (GRID/2), topleft.y + (GRID/2), botright.x, botright.y]
        
        # Determines which combination of sub_blocks a block will consist of
        cell_division = random.uniform(0,1)
        if cell_division > 0.7:
            SUB_BLOCKS = [[topleft.x,topleft.y,botright.x,botright.y]]
        elif cell_division > 0.4:
            if bool(random.getrandbits(1)):
                SUB_BLOCKS = [bigl,bigr]
            else:
                SUB_BLOCKS = [bigt,bigb]
        elif cell_division > 0.1:
            if bool(random.getrandbits(1)):
                if bool(random.getrandbits(1)):
                    SUB_BLOCKS = [bigl,tr_box,br_box]
                else:
                    SUB_BLOCKS = [tl_box,bigr,bl_box]
            else:
                if bool(random.getrandbits(1)):
                    SUB_BLOCKS = [bigt,br_box,bl_box]   
                else:
                    SUB_BLOCKS = [tl_box, tr_box, bigb]
            
        else:
            SUB_BLOCKS = [tl_box, tr_box, br_box, bl_box]
               
        # Parameters for randomisation, would have liked to tweak given more time        
        TOWER_STEP = zone
        BUSINESS_STEP = zone
        block_origin = BLOCKS[i][j].location
        tower_max_height = 10 - TOWER_STEP
        business_max_height = 7 - BUSINESS_STEP
        building = rbt_non_uniform(zone)
        
        # For each sub-block
        for k in range(0, len(SUB_BLOCKS)):
            sub_origin_x = SUB_BLOCKS[k][0] + (abs((SUB_BLOCKS[k][2] - SUB_BLOCKS[k][0]))/2)
            sub_origin_y = SUB_BLOCKS[k][1] + (abs((SUB_BLOCKS[k][3] - SUB_BLOCKS[k][1]))/2) 
            sub_origin = (sub_origin_x, sub_origin_y, BLOCK_HEIGHT)
            sub_size = int(abs(SUB_BLOCKS[k][2] - SUB_BLOCKS[k][0]) * 
            abs(SUB_BLOCKS[k][3] - SUB_BLOCKS[k][1]))
              
            if building == 1:
               generate_tower(SUB_BLOCKS[k], sub_origin, sub_size, tower_max_height)
               
            elif building == 0:
                generate_business(SUB_BLOCKS[k], sub_origin, sub_size, business_max_height)
            else:
                generate_residence(SUB_BLOCKS[k], sub_origin, sub_size)

#Creates a plane under the city and textures it to look like a road
verts = [get_world_vert(0,0,0), get_world_vert(1,0,PLANE_COL-1), get_world_vert(2, PLANE_ROW-1, PLANE_COL-1), get_world_vert(3, PLANE_ROW-1, 0)]
faces = [[0,1,2,3]]
road = create_block('road', (0,0,0), verts, faces)
texture_plane(road)

#Lamp Setup
lamp_data = bpy.data.lamps.new(name="SunData", type='SUN')
lamp_data.sky.use_sky = True
lamp_data.sky.sky_blend = 0.7
lamp_object = bpy.data.objects.new(name="Sun1", object_data=lamp_data)
bpy.context.scene.objects.link(lamp_object)
lamp_object.location = (PLANE_ROW+10, 0, 15)

#Define and position cameras
camera1 = bpy.ops.object.camera_add(location=(0,0,10*((PLANE_ROW+1)/2)))
bpy.ops.transform.rotate(value = (math.radians(-90)), axis = (0, 0, 1))

cam2_loc = 25 + (((PLANE_ROW-3)/2)*10)
camera2 =bpy.ops.object.camera_add(location=(cam2_loc,cam2_loc,cam2_loc))
bpy.ops.transform.rotate(value = math.radians(60), axis = (1, 0, 0))
bpy.ops.transform.rotate(value = (math.radians(135)), axis = (0, 0, 1))

camera3 = bpy.ops.object.camera_add(location=(0,-(41+((PLANE_COL-3)/2)),7))
bpy.ops.transform.rotate(value = math.radians(92), axis = (1, 0, 0))

# Takes pictures using the cameras. Code borrowed from Ashley Manson.
scene = bpy.context.scene
n = 0
for ob in scene.objects:
    if ob.type == 'CAMERA':
        bpy.context.scene.camera = ob
        file = bpy.path.abspath("//render%d.png" %n)
        n += 1
        bpy.context.scene.render.filepath = file
        bpy.ops.render.render( write_still=True )