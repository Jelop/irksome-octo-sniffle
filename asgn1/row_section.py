
import math
import random

import bpy, bmesh
from bpy import context as C

PLANE_ROW = 10
PLANE_COL = 10

bpy.ops.object.select_pattern()
bpy.ops.object.delete()

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
        #print(faces)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    return obj


# Start Execution #
print("start")
verts = [[-5,-5,0],[-5,5,0],[5,5,0],[5,-5,0]]
start_plane = create_block('plane', (0,0,0), verts)

#bpy.ops.object.editmode_toggle()
#bpy.ops.mesh.bisect(plane_co=(1.0, 1.0, 0.0), plane_no=(0.1, 0.0, 0.0))
#bisected = bpy.context.active_object
#bisected.data.update()
#for i in range (0, len(bisected.data.vertices)):
   # print(bisected.data.vertices[i].co)

#selected_verts = [v for v in bisected.data.vertices if v.select]
#for i in range(0, len(selected_verts)):
#    print(selected_verts[i].co)

#bpy.ops.mesh.separate(type='SELECTED')
#bpy.ops.object.editmode_toggle()    


bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(C.object.data) #context.object is the active object?

edges = []

ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(-4,0,0), plane_no=(1,0.2,0))
bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

'''for i in range(-10, 10, 2):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(i,0,0), plane_no=(-1,0,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

for i in range(-10, 10, 2):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,i,0), plane_no=(0,1,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])
'''

bmesh.update_edit_mesh(C.object.data)

bpy.ops.mesh.separate(type='LOOSE')



for i in range(0, len(bpy.data.objects)):
    print(i)
    
for ob in bpy.data.objects:
    print(ob.name)

#bpy.ops.object.mode_set(mode='OBJECT')

for i in range(0, len(bpy.data.objects)):
    ref = obtain_ref(bpy.data.objects[i])
    ref.location.z += 0.2 * i

#ref = obtain_ref(bpy.data.objects[0])
#ref.location.x += 0.2
bpy.ops.object.mode_set(mode='OBJECT')