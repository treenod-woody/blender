import bpy

selObj = bpy.context.selected_objects

bpy.ops.object.select_all(action='DESELECT')

# Create Picking Collider
for obj in selObj:
    
    if (obj.name.endswith('Collision')):
        
        newObjName = obj.name.replace("Collision", "Picking") 
        
        # Copy Object
        newObj = obj.copy()
        newObj.data = obj.data.copy()
        
        # Changing Name & Location of newObj
        newObj.name = newObjName
        newObj.data.name = newObjName
        newObj.location = obj.location
        
        # Insert main collection
        bpy.context.collection.objects.link(newObj)
        
        # add 'Displace' modifier & value setting
        mod = newObj.modifiers.new('Displace', type='DISPLACE')
        mod.strength = 0.25
        bpy.ops.object.modifier_apply(modifier="Displace")
        
        # Desellect All
        bpy.ops.object.select_all(action='DESELECT')