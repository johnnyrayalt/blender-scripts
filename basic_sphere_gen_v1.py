import bpy
import bmesh
import math
from random import random, randint
from mathutils import Vector

def rand_int():
    return randint(0, 99)
        
def check_index_duplicate(index1, index2):
    if index1 == index2:
        index3 = rand_int()
        print('oops, original index:', index1, ', duplicated index:', index2, ', trying again with:', index3)
        return check_index_duplicate(index1, index3)
    else:
        return index2
    
def add_bezier(v0, v1):
    o = (v1 + v0) / 2
    
    curve = bpy.data.curves.new('Curve', 'CURVE')
    spline = curve.splines.new('BEZIER')
    bp0 = spline.bezier_points[0]
    bp0.co = v0 - o
    bp0.handle_left_type = bp0.handle_right_type = 'AUTO'

    spline.bezier_points.add(count=1)
    bp1 = spline.bezier_points[1]
    bp1.co = v1 - o
    bp1.handle_left_type = bp1.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new('Curve', curve)
    ob.matrix_world.translation = o
    return ob

# delete existing objects
delete = bpy.context.scene.objects.keys()
if len(delete) > 0:
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global = False)


# generate vectors
ranges = {
    'x': { 'min': -4, 'max': 4 },
    'y': { 'min': -4, 'max': 4 },
    'z': { 'min': -4, 'max': 4 }
}

size = 100
spheres = []

randLocInRange = lambda axis: ranges[axis]['min'] + random() * ( ranges[axis]['max'] - ranges[axis]['min'] )

loopIterations = 0
maxIterations = 100
while len(spheres) < size:
    loc = Vector([ randLocInRange(axis) for axis in ranges.keys() ])
    
    if len(spheres) > 0:
        overlappingPoints = [ p for p in spheres if (p - loc).length < 0.1 ]
        
        if overlappingPoints: continue
    
    spheres.append(loc)


# create new objects
x = 0
while x < 100:
    # create mesh + object
    mesh = bpy.data.meshes.new('Basic_Sphere')
    sphere = bpy.data.objects.new('Basic_Sphere', mesh)
    
    # add object to the scene
    bpy.context.collection.objects.link(sphere)
    
    # select new object
    bpy.context.view_layer.objects.active = sphere
    sphere.select_set(True)
    
    # construct bmesh sphere and add it to blender mesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments = 32, v_segments = 16, diameter = random())
    bm.to_mesh(mesh)
    
    # translate sphere
    print(spheres[x])
    bpy.ops.transform.translate(value = spheres[x])
    
    x += 1
 
 


objects = bpy.context.scene.objects.keys()
scene = bpy.context.scene
for index, start in enumerate(spheres):
    print(start)
    bpy.ops.object.mode_set(mode = 'EDIT')
    sphere2 = rand_int()
    dest = check_index_duplicate(index, sphere2)
    
    line = add_bezier(start, spheres[dest])
    curve = line.data    
    curve.dimensions = '3D'
    curve.bevel_depth = 0.010
    curve.bevel_resolution = 3
    scene.collection.objects.link(line)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
print('finished')
