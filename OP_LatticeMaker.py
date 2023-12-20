import bpy

# Lattice Resolution --------------------------

resolution_x = 0
resolution_y = 0
resolution_z = 0

# ---------------------------------------------

selObj = bpy.context.selected_objects

# Desellect All
bpy.ops.object.select_all(action='DESELECT')

for obj in selObj:
    
    obj_loc = bpy.data.objects[obj.name].location
    
    # Create Lattice : select obj's location & Scale
    bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=obj_loc, scale=(1, 1, 1))
    curObj = bpy.context.selected_objects[0]
    curObj.name = obj.name + "_Lattice"
    latticeName = curObj.name
    curObj.data.name = latticeName
    size = obj.dimensions
    curObj.scale = (size[0] + 0.1, size[1] + 0.1, size[2] + 0.1)
    
    # Lattice Resolution
    latticeObj = bpy.context.selected_objects[0]
    latticeObj.data.points_u = 2 + resolution_x
    latticeObj.data.points_v = 2 + resolution_y
    latticeObj.data.points_w = 2 + resolution_z
    
    bpy.ops.object.select_all(action='DESELECT')
    
    # "Lattice" Modifier & Apply "Lattice" Object
    obj.select_set(True)
    selObj = bpy.context.selected_objects[0]
    selObj.modifiers.new(name='Lattice', type='LATTICE')
    selObj.modifiers["Lattice"].object = bpy.data.objects[latticeName]
    
    bpy.ops.object.select_all(action='DESELECT')