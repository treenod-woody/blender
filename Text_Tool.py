bl_info = {
    "name": "Text Tool",
    "author": "Darkfall",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Text Tool Tab",
    "description": "Adds a new Text Object with user defined properties",
    "warning": "",
    "wiki_url": "",
    "category": "Add Text",
}

import bpy

# VIEW_3D 사이드바 ---------------------------------------

class OBJECT_PT_TextTool(bpy.types.Panel):
    bl_label = "Text Tool"
    bl_idname = "OBJECT_PT_texttool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text= "Text Popup:")
        row.operator("wm.textopbasic", text= "Add Text...", icon= 'OUTLINER_OB_FONT')
        


# 텍스트 생성 후 텍스트 Spacing 옵션 ----------------------------------------

class OBJECT_PT_Spacing(bpy.types.Panel):
    bl_label = "Spacing"
    bl_idname = "OBJECT_PT_spacing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    bl_parentid = "OBJECT_PT_texttool"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        text = context.object.data

        row = layout.row()
        row.label(text= "텍스트 Spacing 옵션 설정")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Character:")
        row.prop(text, "space_character", text= "")

        row = layout.split(factor= 0.45)
        row.label(text= "Word:")
        row.prop(text, "space_word", text= "")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Line:")
        row.prop(text, "space_line", text= "")
        

# Operation 옵션 ---------------------------------------------------------------

class WM_OT_textOpBasic(bpy.types.Operator):
    """Open the Text Tool Dialog Box"""
    bl_idname = "wm.textopbasic"
    bl_label = "Text Tool Operator"
    
    text : bpy.props.StringProperty(name="Enter Text", default="")
    scale : bpy.props.FloatProperty(name= "Scale", default= 1)
    rotation : bpy.props.BoolProperty(name= "Z up", default= False)
    center : bpy.props.BoolProperty(name= "Center Origin", default= False)
    extrude : bpy.props.BoolProperty(name= "Extrude", default= False)
    extrude_amount : bpy.props.FloatProperty(name= "Extrude Amount", default= 0.06)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        
        layout = self.layout
        
        layout.prop(self, "text")
        layout.prop(self, "scale")
        
        layout.separator(factor= 1)
        
        box = layout.box()
        
        row = box.row()
        row.prop(self, "rotation")
        if self.rotation == True:
            row.label(text= "Orientation: Z up", icon= 'EMPTY_SINGLE_ARROW')
        elif self.rotation == False:
            row.label(text= "Orientation: Default", icon= 'ARROW_LEFTRIGHT')
            
        
        row = box.row()
        row.prop(self, "center")
        if self.center == True:
            row.label(text= "Align: Center", icon= 'ALIGN_CENTER')
        elif self.center == False:
            row.label(text= "Align: Left", icon= 'ALIGN_LEFT')
        
        row = box.row()
        row.prop(self, "extrude")
        if self.extrude == True:
            row.prop(self, "extrude_amount")
        
    def execute(self, context):
        
        text = self.text
        scale = self.scale
        center = self.center
        extrude = self.extrude
        extrude_amount = self.extrude_amount
        rotation = self.rotation
        
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text= text)
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.size = scale

        if rotation == True:
            bpy.context.object.rotation_euler[0] = 1.5708
                    
        if extrude == True:
            bpy.context.object.data.extrude = extrude_amount
        
        if center == True:
            bpy.context.object.data.align_x = 'CENTER'
            bpy.context.object.data.align_y = 'CENTER'


        return {'FINISHED'}

# Registration -------------------------------------------------------------------

classes= {
    OBJECT_PT_TextTool,
    OBJECT_PT_Spacing,
    WM_OT_textOpBasic
}

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()