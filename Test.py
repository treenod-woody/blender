from typing import Set
import bpy
from bpy.types import Context, Panel, Operator
from bpy.props import FloatProperty

class OBJECT_PT_Woody_Tools(Panel):
    bl_idname = "OBJECT_PT_Woody_Tools"
    bl_label = "Woody Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Woody Tools"

    def draw(self, context):
        layout = self.layout
        
        selected_object = bpy.context.object

        # 선택한 오브젝트의 프라퍼티를 사용
        layout.label(text="Transform :")
        layout.prop(selected_object, "location", text="")
        layout.prop(selected_object, "rotation_euler", text="")
        layout.prop(selected_object, "scale", text="")



classes = [
    OBJECT_PT_Woody_Tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()