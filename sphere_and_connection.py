import bpy
import bmesh
import math
from random import random, randint
from mathutils import Vector

class Spheres:
    
    spheres = []
    sphere = None
    size = 100
    ranges = {
        'x': { 'min': -20, 'max': 20 },
        'y': { 'min': -20, 'max': 20 },
        'z': { 'min': -20, 'max': 20 }
    }
    
    def generate_vectors(self):
        randLocInRange = lambda axis: self.ranges[axis]['min'] + random() * ( self.ranges[axis]['max'] - self.ranges[axis]['min'] )

        while len(self.spheres) < self.size:
            loc = Vector([ randLocInRange(axis) for axis in self.ranges.keys() ])
            
            if len(self.spheres) > 0:
                overlappingPoints = [ p for p in self.spheres if (p - loc).length < 0.1 ]
                
                if overlappingPoints: continue
            
            self.spheres.append(loc)
            
    def create_objects(self):
        x = 0
        while x < 100:
            # create mesh + object
            mesh = bpy.data.meshes.new('Basic_Sphere')
            self.sphere = bpy.data.objects.new('Basic_Sphere', mesh)
            
            # add object to the scene
            bpy.context.collection.objects.link(self.sphere)
            
            # select new object
            bpy.context.view_layer.objects.active = self.sphere
            self.sphere.select_set(True)
            
            # construct bmesh sphere and add it to blender mesh
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments = 32, v_segments = 16, radius = 1)
            bm.to_mesh(mesh)

            x += 1
            
    def populate_sphere_location(self):
        for s in self.spheres[1:]:
            d = self.sphere.copy()
            d.location = s
            bpy.context.collection.objects.link(d)

class Connections:
    
    @staticmethod
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
    
    @staticmethod
    def populate_connections(spheres):
        objects = bpy.context.scene.objects.keys()
        scene = bpy.context.scene
        for index, start in enumerate(spheres):
            print(start)
            bpy.ops.object.mode_set(mode = 'EDIT')
            sphere2 = Utils().rand_int()
            dest = Utils().check_index_duplicate(index, sphere2)
            
            line = Connections().add_bezier(start, spheres[dest])
            curve = line.data    
            curve.dimensions = '3D'
            curve.bevel_depth = 0.010
            curve.bevel_resolution = 3
            scene.collection.objects.link(line)
            bpy.ops.object.mode_set(mode = 'OBJECT')

class Utils:

    @staticmethod
    def rand_int():
        return randint(0, 99)

    @staticmethod
    def check_index_duplicate(index1, index2):
        if index1 == index2:
            index3 = Utils().rand_int()
            print('oops, original index:', index1, ', duplicated index:', index2, ', trying again with:', index3)
            return Utils().check_index_duplicate(index1, index3)
        else:
            return index2
    
    @staticmethod
    def clear_board():
        if len(bpy.context.scene.objects.keys()) > 0:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action = 'SELECT')
            bpy.ops.object.delete(use_global = False)


Utils().clear_board()

print("[1]..generating spheres")
spheres = Spheres()
print(".....spheres completed")

print("[2]..generating vectors")
spheres.generate_vectors()
print(".....vectors completed")

print("[3]..adding objects to context")
spheres.create_objects()
print(".....objects added")

print("[4]..add objects to scene")
spheres.populate_sphere_location()
print(".....objects added")

print("[5]..poppulate connections")
Connections().populate_connections(spheres.spheres)
print(".....connections added")

print('finished!')