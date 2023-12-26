import bpy
import bmesh
from typing import Set
from bpy.types import Context, Panel, Operator
from bpy.props import StringProperty, FloatProperty, BoolProperty

# 머티리얼 체크 & 생성 & 리턴 (중복 방지)
def check_material_exist(material_name):
    if material_name in bpy.data.materials:
        material = bpy.data.materials[material_name]
        bpy.data.materials.remove(material)

    material = bpy.data.materials.new(material_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[12].default_value = 0    # Specular = '0'

    return material

# 메시 체크 & 제거 (중복 방지)
def check_mesh_exist(mesh_name):
    if mesh_name in bpy.data.materials:
        mesh = bpy.data.materials[mesh_name]
        bpy.data.materials.remove(mesh)


# Main Panel : 사이드바 메인 메뉴 UI 세팅
class OBJECT_PT_TestTool(Panel):
    bl_label = "Test"
    bl_idname = "OBJECT_PT_woodytool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test"

    def draw(self, context):
        layout = self.layout

        # 선택한 오브젝트의 Properties 사용
        layout.label(text="Object Array :", icon="OUTLINER_DATA_EMPTY")

class ARRAY_OT_myop(Operator):
    bl_idname = ""
    bl_label = ""
    
    def execute(self, context):

        

        return {'FINISHED'}
    

classes = [
    OBJECT_PT_TestTool,
    ARRAY_OT_myop
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()