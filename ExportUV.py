import bpy
import os

# Change Texture Size : N x N pixel
texture_size = 256

# Save directory
file_path = bpy.data.filepath
file_dir, file_name = os.path.split(file_path)
export_dir = os.path.join(file_dir, 'Texture')

# Check directory
if not os.path.exists(export_dir):
    os.makedirs(export_dir)
    print("Create folder")
else:
    print("Exist folder:", export_dir)

# Select Object List
selObj = bpy.context.selected_objects

# Desellect All
bpy.ops.object.select_all(action='DESELECT')

for obj in selObj:
    # Save File Name
    export_path = os.path.join(export_dir, obj.name + '.png')

    # Export UV
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.export_layout(filepath = export_path, export_all = False, modified = False, mode = 'PNG', size = (texture_size, texture_size),opacity = 1.0)
    bpy.ops.object.mode_set(mode="OBJECT")