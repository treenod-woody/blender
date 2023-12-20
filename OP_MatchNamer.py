import bpy

num = 0

for mesh in bpy.data.meshes:
    mesh.name = str(num)
    num += 1

for obj in bpy.data.objects:
    obj.data.name = obj.name