import bpy

selObj = bpy.context.selected_objects
scale = 0.1

# Desellect All
bpy.ops.object.select_all(action='TOGGLE')

for obj in selObj:
    # Create Cube : select obj's location
    selObj_loc = bpy.data.objects[obj.name].location
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=selObj_loc)
    bpy.context.object.display_type = 'WIRE'
    
    # Set collision name & scale
    curObj = bpy.context.selected_objects[0]
    curObj.name = obj.name + "_Collision"
    curObj.data.name = obj.name + "_Collision"
    size = obj.dimensions
    curObj.scale = (size[0] + scale, size[1] + scale, size[2] + scale)
        
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)