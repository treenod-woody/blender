bl_info = {
    "name": "Shader Library",
    "author": "Woody",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf",
    "description": "셰이더 라이브러리입니다.",
    "warning": "",
    "doc_url": "",
    "category": "Shader Lib",
}


import bpy
from bpy.types import Operator, Panel
        

class SHADER_PT_MainPanel(Panel):
    """Shader 머티리얼 생성"""
    bl_label = "Shader Library Panel"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Lib'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select a Shader")

        row = layout.row()
        row.operator(SHADER_OT_TwoSideTex.bl_idname, text=SHADER_OT_TwoSideTex.bl_label)

class SHADER_OT_TwoSideTex(Operator):
    bl_label = "TwoSideTex"
    bl_idname = 'shader.twosidetex_operator'

    def execute(self, context):

        # material_name 존재여부 체크 : True / False
        def check_material_exist(material_name):
            return material_name in bpy.data.materials

        # group_name 존재여부 체크 : True / False
        def check_node_group_exist(group_name):
            return group_name in bpy.data.node_groups

        # 선택한 오브젝트의 머티리얼 슬롯을 모두 제거
        obj = bpy.context.object
        obj.data.materials.clear()

        material = None

        # 존재 여부 체크 후 동일한 이름의 머티리얼이 있다면 제거
        if check_material_exist(obj.name):
            material = bpy.data.materials[obj.name]
            bpy.data.materials.remove(material)

        # 신규 머티리얼 생성 후 노드 활성화
        material = bpy.data.materials.new(name=obj.name)
        material.use_nodes = True
        
        # 머티리얼의 모든 노드 리스트를 받아와서 'Prinscipled BSDF' 노드만 제거
        node_tree = material.node_tree
        nodes = node_tree.nodes
        nodes.remove(nodes.get('Principled BSDF'))

        # Material Output 노드
        material_output = nodes.get('Material Output')
        material_output.location = (100, 0)

        # 노드 그룹 데이터 블록을 가져옵니다.
        two_side_tex_group = bpy.data.node_groups.get("TwoSideTexGroup")

        # 노드 그룹 데이터 블록이 존재한다면 제거합니다.
        if two_side_tex_group is not None:
            bpy.data.node_groups.remove(two_side_tex_group)
            
        # 'TwoSideTexGroup' 노드 그룹 데이터 블록 생성
        bpy.data.node_groups.new('TwoSideTexGroup', 'ShaderNodeTree')
        node_group = nodes.new(type='ShaderNodeGroup')
        node_group.node_tree = bpy.data.node_groups['TwoSideTexGroup']
        node_group.location = (-100, 0)
        group = node_group.node_tree

        # Group Input 노드
        group_in = group.nodes.new(type='NodeGroupInput')
        group_in.location = (-600, 0)

        # Group Output 노드
        group_out = group.nodes.new(type='NodeGroupOutput')
        group_out.location = (1000, 0)

        # Group Input / Output 소켓 추가
        group.interface.new_socket(name="Face Color", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Back Color", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')

# 노드 리스트 ===================================
        
        # Images Texture 노드 1
        node_TexImage_1 = group.nodes.new(type='ShaderNodeTexImage')
        node_TexImage_1.location = (-600, 300)

        # Images Texture 노드 2
        node_TexImage_2 = group.nodes.new(type='ShaderNodeTexImage')
        node_TexImage_2.location = (-600, -300)

        # Math 노드 1
        node_Math_1 = group.nodes.new(type='ShaderNodeMath')
        node_Math_1.location = (-250, 200)
        node_Math_1.operation = 'MULTIPLY'

        # Mix Color 노드 2
        node_Math_2 = group.nodes.new(type='ShaderNodeMath')
        node_Math_2.location = (-250, -200)
        node_Math_2.operation = 'MULTIPLY'

        # Principled BSDF 노드 1
        node_BSDF_1 = group.nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_1.location = (230, 250)
        node_BSDF_1.inputs[12].default_value = 0

        # Principled BSDF 노드 2
        node_BSDF_2 = group.nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_2.location = (230, -250)
        node_BSDF_2.inputs[12].default_value = 0

        # Mix Shader 노드
        node_MixShader = group.nodes.new(type='ShaderNodeMixShader')
        node_MixShader.location = (730, 0)

        # Geometry 노드
        node_Geometry = group.nodes.new(type='ShaderNodeNewGeometry')
        node_Geometry.location = (0, 90)

        # 노드 링크
        group.links.new(node_TexImage_1.outputs[0], node_Math_1.inputs[0])
        group.links.new(node_TexImage_2.outputs[0], node_Math_2.inputs[0])
        group.links.new(node_TexImage_1.outputs[1], node_BSDF_1.inputs[4])
        group.links.new(node_TexImage_2.outputs[1], node_BSDF_2.inputs[4])
        group.links.new(group_in.outputs[0], node_Math_1.inputs[1])
        group.links.new(group_in.outputs[1], node_Math_2.inputs[1])
        group.links.new(node_Math_1.outputs[0], node_BSDF_1.inputs[0])
        group.links.new(node_Math_2.outputs[0], node_BSDF_2.inputs[0])
        group.links.new(node_Geometry.outputs[6], node_MixShader.inputs[0])
        group.links.new(node_BSDF_1.outputs[0], node_MixShader.inputs[1])
        group.links.new(node_BSDF_2.outputs[0], node_MixShader.inputs[2])
        group.links.new(node_MixShader.outputs[0], group_out.inputs[0])

        # Material Output 노드에 Node Group 적용
        material.node_tree.links.new(node_group.outputs[0], material_output.inputs[0])

        # 머티리얼 할당
        obj.data.materials.append(material)

        return {'FINISHED'}



classes = [
    SHADER_PT_MainPanel,
    SHADER_OT_TwoSideTex
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()