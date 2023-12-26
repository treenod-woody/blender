import bpy, math
from typing import Set
from bpy.types import Context, Panel, Operator
from bpy.props import StringProperty, FloatProperty, BoolProperty, IntProperty

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
    if mesh_name in bpy.data.meshes:
        mesh = bpy.data.meshes[mesh_name]
        bpy.data.meshes.remove(mesh)


# Main Panel : 사이드바 메인 메뉴 UI 세팅
class OBJECT_PT_TestTool(Panel):
    bl_label = "Test"
    bl_idname = "OBJECT_PT_woodytool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test"

    def draw(self, context):
        layout = self.layout

        # Circle Array Button
        layout.operator(CircleArray.bl_idname, text=CircleArray.bl_label, icon="OUTLINER_DATA_POINTCLOUD")


class CircleArray(Operator):
    bl_label = "Circle Array"
    bl_idname = "object.circle_array"
    bl_options = {'REGISTER', 'UNDO'}
    
    segment : IntProperty(name="Segment", default=6, min=3)
    radius : IntProperty(name="Radius", default=2, min=1)

    def execute(self, context):

        segment = self.segment
        angle_step = math.tau / segment
        radius = self.radius

        # 선택한 오브젝트
        origin_obj = bpy.context.active_object
        origin_obj.location = (0,0,0)


        for i in range(segment):

            current_angle_step = i * angle_step

            x = radius * math.sin(current_angle_step)
            y = radius * math.cos(current_angle_step)

            # 선택한 오브젝트를 복제한 후 원래의 오브젝트에 데이터 링크
            copy_obj = origin_obj.copy()
            # copy_obj.data = origin_obj.data.copy()
            copy_obj.location = (x, y, 0)
            copy_obj_name = copy_obj.name
            print(copy_obj_name)


            # 메인 컬렉션에 복제된 오브젝트 링크
            bpy.context.collection.objects.link(copy_obj)

            # 데이터 링크
            copy_obj.select_set(True)
            origin_obj.select_set(True)
            bpy.context.view_layer.objects.active = origin_obj
            bpy.ops.object.make_links_data(type='OBDATA')
            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
    
classes = [
    OBJECT_PT_TestTool,
    CircleArray
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()