import math
import random

import bpy, bmesh

PLANE_ROW = 10
PLANE_COL = 10
STREET_WIDTH = 0.2

bpy.ops.object.select_pattern()
bpy.ops.object.delete()

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
print("start\n")
verts = [[-5,-5,0],[-5,5,0],[5,5,0],[5,-5,0]]
start_plane = create_block('plane', (0,0,0), verts)

bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(bpy.context.scene.objects[0].data) 

edges = []

ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(-4,0,0), plane_no=(1,0.08,0))
bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])


#bmesh.ops.translate(bm, vec=(STREET_WIDTH,0,0), verts=bm.verts)
bmesh.update_edit_mesh(bpy.context.scene.objects[0].data)
bpy.ops.mesh.separate(type='LOOSE')


bpy.context.active_object.location.x += 1
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.scene.objects.active = bpy.context.scene.objects[0]


bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(bpy.context.scene.objects[0].data)
print(bpy.context.scene.objects[0].name)

edges = []

ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(-4.5,-4,0), plane_no=(0,1,0))
bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])


bmesh.ops.translate(bm, vec=(STREET_WIDTH,0,0), verts=bm.verts)
bmesh.update_edit_mesh(bpy.context.scene.objects[0].data)

bpy.ops.mesh.separate(type='LOOSE')

bpy.ops.object.mode_set(mode='OBJECT')

for i in range(0, len(bpy.context.scene.objects)):
    print(bpy.context.scene.objects[i].name)