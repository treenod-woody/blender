import bpy

bl_info = {
    "name": "woody Tool",
    "author": "woody",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > WoodyTool Tab",
    "description": "신규 도형을 추가합니다.",
    "warning": "",
    "wiki_url": "",
    "category": "Add Primitive",
}

# VIEW_3D 사이드바 ---------------------------------------

class OBJECT_PT_WoodyTool(bpy.types.Panel):
    bl_label = "Woody Tool"
    bl_idname = "OBJECT_PT_woodytool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Woody Tool"
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("wm.add_cube", text= "Add Cube...", icon= 'MESH_CUBE') # Button : Add Cube

# Cube 생성
class AddCube(bpy.types.Operator):
    """Cube 추가용 대화상자"""
    bl_label = "Add Cube"
    bl_idname = "wm.add_cube"

    text: bpy.props.StringProperty(name= "Name", default= "Cube")
    scale: bpy.props.FloatProperty(name= "Scale", default= 1)
    origin: bpy.props.EnumProperty(
        name= "",
        description= "",
        items= [
            ('OP1', "Bottom", "Origin to Bottom"),
            ('OP2', "Center", "Origin to Center")
        ],
        default= 'OP2'
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "text")
        row.prop(self, "scale")
        
        layout.separator(factor= 1)

        row = layout.row()
        row.prop(self, "origin")
        if self.origin == 'OP1':
            row.label(text= "Origin: Bottom", icon= 'ANCHOR_BOTTOM')
        elif self.origin == 'OP2':
            row.label(text= "Origin: Center", icon= 'ANCHOR_CENTER')

        layout.separator(factor= 1)

    def execute(self, context):
        
        text = self.text
        scale = self.scale
        origin = self.origin

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object

        # Cube Name
        obj.name = text

        # Cube Scale
        obj.scale[0] = scale
        obj.scale[1] = scale
        obj.scale[2] = scale

        # Cube Origin
        if self.origin == 'OP1':
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.object.pivotobottom()
        elif self.origin == 'OP2':
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')



        return {'FINISHED'}

class AddCylinder(bpy.types.Operator):
    """Cylinder 추가용 대화상자"""
    bl_label = "Add Cylinder"
    bl_idname = "wm.add_cylinder"

    text: bpy.props.StringProperty(name= "Name", default= "Cylinder")
    radius: bpy.props.FloatProperty(name= "Radius", default= 1)
    depth: bpy.props.FloatProperty(name= "Depth", default= 2)
    scale: bpy.props.FloatProperty(name= "Scale", default= 0.5)
    
    vertices: bpy.props.EnumProperty(
        name= "",
        description= "",
        items= [
            ('OP1', "6", "6각형"),
            ('OP2', "8", "8각형"),
            ('OP3', "10", "10각형"),
            ('OP4', "12", "12각형"),
        ],
        default= 'OP2'
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout

        row.prop(self, "text")

        row = layout.row()
        row.prop(self, "scale")
        row.prop(self, "vertices")
        if self.vertices == 'OP1':
            row.label(text= "6각형")
        elif self.vertices == 'OP2':
            row.label(text= "8각형")
        elif self.vertices == 'OP3':
            row.label(text= "10각형")
        elif self.vertices == 'OP4':
            row.label(text= "12각형")
        
        layout.separator(factor= 1)

        row = layout.row()
        row.prop(self, "radius")
        row.prop(self, "depth")
        
        layout.separator(factor= 1)

    def execute(self, context):
        
        text = self.text
        scale = self.scale
        origin = self.origin

        bpy.ops.mesh.primitive_cylinder_add()
        obj = bpy.context.active_object

        # Cylinder Name
        obj.name = text

        # Cylinder Scale
        obj.scale[0] = scale
        obj.scale[1] = scale
        obj.scale[2] = scale

        # Cylinder Vertices
        if self.vertices == 'OP1':
            bpy.ops.object.vertices(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.object.pivotobottom()
        elif self.vertices == 'OP2':
            bpy.ops.object.vertices(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')



        return {'FINISHED'}

classes = [
    OBJECT_PT_WoodyTool,
    AddCube
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
