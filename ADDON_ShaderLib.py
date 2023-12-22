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

        row = layout.row()
        row.operator(SHADER_OT_Blend2Tex.bl_idname, text=SHADER_OT_Blend2Tex.bl_label)
        row.operator(SHADER_OT_Blend3Tex.bl_idname, text=SHADER_OT_Blend3Tex.bl_label)
        row.operator(SHADER_OT_Blend4Tex.bl_idname, text=SHADER_OT_Blend4Tex.bl_label)

        layout.separator(factor=1)

        layout.operator(SHADER_OT_TwoSideTex.bl_idname, text=SHADER_OT_TwoSideTex.bl_label)

class SHADER_OT_Blend2Tex(Operator):
    bl_label = "2Tex"
    bl_idname = 'shader.blend2tex_operator'

    def execute(self, context):

        # material_name 존재여부 체크 : True / False
        def check_material_exist(material_name):
            return material_name in bpy.data.materials

        # 선택한 오브젝트의 머티리얼 슬롯을 모두 제거
        obj = bpy.context.object
        obj.data.materials.clear()

        material = None

        # 존재 여부 체크 후 머티리얼 할당
        if check_material_exist(obj.name):
            material = bpy.data.materials[obj.name]
            bpy.data.materials.remove(material)

        material = bpy.data.materials.new(name=obj.name)
        material.use_nodes = True
        node_tree = material.node_tree
        nodes = node_tree.nodes
        nodes.remove(nodes.get('Principled BSDF'))

        # Material Output 노드
        node_output = nodes.get('Material Output')
        node_output.location = (1000, 0)

        # Texture Coordinate 노드
        node_TexCoord = nodes.new(type='ShaderNodeTexCoord')
        node_TexCoord.location = (-600, 0)

        # Mapping 노드 1
        node_Mapping_1 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_1.location = (-370, 250)
        node_Mapping_1.inputs[3].default_value[0] = 2
        node_Mapping_1.inputs[3].default_value[1] = 2

        # Mapping 노드 2
        node_Mapping_2 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_2.location = (-370, -250)
        node_Mapping_2.inputs[3].default_value[0] = 2
        node_Mapping_2.inputs[3].default_value[1] = 2

        # Images Texture 노드 1
        node_TexImage_1 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_1.location = (-70, 250)

        # Images Texture 노드 2
        node_TexImage_2 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_2.location = (-70, -250)

        # Principled BSDF 노드 1
        node_BSDF_1 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_1.location = (230, 250)
        node_BSDF_1.inputs[12].default_value = 0

        # Principled BSDF 노드 2
        node_BSDF_2 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_2.location = (230, -250)
        node_BSDF_2.inputs[12].default_value = 0

        # Mix Shader 노드
        node_MixShader = nodes.new(type='ShaderNodeMixShader')
        node_MixShader.location = (730, 0)

        # Attribute 노드
        node_Attribute = nodes.new(type='ShaderNodeAttribute')
        node_Attribute.location = (230, 500)
        node_Attribute.attribute_name = "Col"


        # Node link
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_1.inputs[0])
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_2.inputs[0])
        node_tree.links.new(node_Mapping_1.outputs[0], node_TexImage_1.inputs[0])
        node_tree.links.new(node_Mapping_2.outputs[0], node_TexImage_2.inputs[0])
        node_tree.links.new(node_TexImage_1.outputs[0], node_BSDF_1.inputs[0])
        node_tree.links.new(node_TexImage_2.outputs[0], node_BSDF_2.inputs[0])
        node_tree.links.new(node_Attribute.outputs[0], node_MixShader.inputs[0])
        node_tree.links.new(node_BSDF_1.outputs[0], node_MixShader.inputs[1])
        node_tree.links.new(node_BSDF_2.outputs[0], node_MixShader.inputs[2])
        node_tree.links.new(node_MixShader.outputs[0], node_output.inputs[0])

        # 머티리얼 할당
        obj.data.materials.append(material)

        return {'FINISHED'}


class SHADER_OT_Blend3Tex(Operator):
    bl_label = "3Tex"
    bl_idname = 'shader.blend3tex_operator'

    def execute(self, context):

        # material_name 존재여부 체크 : True / False
        def check_material_exist(material_name):
            return material_name in bpy.data.materials

        # 선택한 오브젝트의 머티리얼 슬롯을 모두 제거
        obj = bpy.context.object
        obj.data.materials.clear()

        material = None

        # 존재 여부 체크 후 머티리얼 할당
        if check_material_exist(obj.name):
            material = bpy.data.materials[obj.name]
            bpy.data.materials.remove(material)

        material = bpy.data.materials.new(name=obj.name)
        material.use_nodes = True
        node_tree = material.node_tree
        nodes = node_tree.nodes
        nodes.remove(nodes.get('Principled BSDF'))

        # Material Output 노드
        node_output = nodes.get('Material Output')
        node_output.location = (1700, -250)

        # Texture Coordinate 노드
        node_TexCoord = nodes.new(type='ShaderNodeTexCoord')
        node_TexCoord.location = (-600, 0)

        # Mapping 노드 1
        node_Mapping_1 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_1.location = (-370, 250)
        node_Mapping_1.inputs[3].default_value[0] = 2
        node_Mapping_1.inputs[3].default_value[1] = 2

        # Mapping 노드 2
        node_Mapping_2 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_2.location = (-370, -250)
        node_Mapping_2.inputs[3].default_value[0] = 2
        node_Mapping_2.inputs[3].default_value[1] = 2

        # Mapping 노드 3
        node_Mapping_3 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_3.location = (-370, -750)
        node_Mapping_3.inputs[3].default_value[0] = 2
        node_Mapping_3.inputs[3].default_value[1] = 2

        # Images Texture 노드 1
        node_TexImage_1 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_1.location = (-70, 250)

        # Images Texture 노드 2
        node_TexImage_2 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_2.location = (-70, -250)

        # Images Texture 노드 3
        node_TexImage_3 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_3.location = (-70, -750)

        # Principled BSDF 노드 1
        node_BSDF_1 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_1.location = (230, 250)
        node_BSDF_1.inputs[12].default_value = 0

        # Principled BSDF 노드 2
        node_BSDF_2 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_2.location = (230, -250)
        node_BSDF_2.inputs[12].default_value = 0

        # Principled BSDF 노드 3
        node_BSDF_3 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_3.location = (230, -750)
        node_BSDF_3.inputs[12].default_value = 0

        # Mix Shader 노드 1
        node_MixShader_1 = nodes.new(type='ShaderNodeMixShader')
        node_MixShader_1.location = (730, 0)

        # Mix Shader 노드 2
        node_MixShader_2 = nodes.new(type='ShaderNodeMixShader')
        node_MixShader_2.location = (1230, -250)

        # Color Attribute 노드
        node_ColorAttribute = nodes.new(type='ShaderNodeVertexColor')
        node_ColorAttribute.location = (0, 500)

        # Separate Color 노드
        node_SeparateColor = nodes.new(type='ShaderNodeSeparateColor')
        node_SeparateColor.location = (300, 500)


        # Node link
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_1.inputs[0])
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_2.inputs[0])
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_3.inputs[0])
        node_tree.links.new(node_Mapping_1.outputs[0], node_TexImage_1.inputs[0])
        node_tree.links.new(node_Mapping_2.outputs[0], node_TexImage_2.inputs[0])
        node_tree.links.new(node_Mapping_3.outputs[0], node_TexImage_3.inputs[0])
        node_tree.links.new(node_TexImage_1.outputs[0], node_BSDF_1.inputs[0])
        node_tree.links.new(node_TexImage_2.outputs[0], node_BSDF_2.inputs[0])
        node_tree.links.new(node_TexImage_3.outputs[0], node_BSDF_3.inputs[0])
        node_tree.links.new(node_ColorAttribute.outputs[0], node_SeparateColor.inputs[0])
        node_tree.links.new(node_SeparateColor.outputs[0], node_MixShader_1.inputs[0])
        node_tree.links.new(node_SeparateColor.outputs[1], node_MixShader_2.inputs[0])
        node_tree.links.new(node_BSDF_1.outputs[0], node_MixShader_1.inputs[1])
        node_tree.links.new(node_BSDF_2.outputs[0], node_MixShader_1.inputs[2])
        node_tree.links.new(node_BSDF_3.outputs[0], node_MixShader_2.inputs[2])
        node_tree.links.new(node_MixShader_1.outputs[0], node_MixShader_2.inputs[1])
        node_tree.links.new(node_MixShader_2.outputs[0], node_output.inputs[0])

        # 머티리얼 할당
        obj.data.materials.append(material)

        return {'FINISHED'}


class SHADER_OT_Blend4Tex(Operator):
    bl_label = "4Tex"
    bl_idname = 'shader.blend4tex_operator'

    def execute(self, context):

        # material_name 존재여부 체크 : True / False
        def check_material_exist(material_name):
            return material_name in bpy.data.materials

        # 선택한 오브젝트의 머티리얼 슬롯을 모두 제거
        obj = bpy.context.object
        obj.data.materials.clear()

        material = None

        # 존재 여부 체크 후 머티리얼 할당
        if check_material_exist(obj.name):
            material = bpy.data.materials[obj.name]
            bpy.data.materials.remove(material)

        material = bpy.data.materials.new(name=obj.name)
        material.use_nodes = True
        node_tree = material.node_tree
        nodes = node_tree.nodes
        nodes.remove(nodes.get('Principled BSDF'))

        # Material Output 노드
        node_output = nodes.get('Material Output')
        node_output.location = (2200, -250)

        # Texture Coordinate 노드
        node_TexCoord = nodes.new(type='ShaderNodeTexCoord')
        node_TexCoord.location = (-600, 0)

        # Mapping 노드 1
        node_Mapping_1 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_1.location = (-370, 250)
        node_Mapping_1.inputs[3].default_value[0] = 2
        node_Mapping_1.inputs[3].default_value[1] = 2

        # Mapping 노드 2
        node_Mapping_2 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_2.location = (-370, -250)
        node_Mapping_2.inputs[3].default_value[0] = 2
        node_Mapping_2.inputs[3].default_value[1] = 2

        # Mapping 노드 3
        node_Mapping_3 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_3.location = (-370, -750)
        node_Mapping_3.inputs[3].default_value[0] = 2
        node_Mapping_3.inputs[3].default_value[1] = 2

        # Mapping 노드 4
        node_Mapping_4 = nodes.new(type='ShaderNodeMapping')
        node_Mapping_4.location = (-370, -1250)
        node_Mapping_4.inputs[3].default_value[0] = 2
        node_Mapping_4.inputs[3].default_value[1] = 2

        # Images Texture 노드 1
        node_TexImage_1 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_1.location = (-70, 250)

        # Images Texture 노드 2
        node_TexImage_2 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_2.location = (-70, -250)

        # Images Texture 노드 3
        node_TexImage_3 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_3.location = (-70, -750)

        # Images Texture 노드 4
        node_TexImage_4 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_4.location = (-70, -1250)

        # Principled BSDF 노드 1
        node_BSDF_1 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_1.location = (230, 250)
        node_BSDF_1.inputs[12].default_value = 0

        # Principled BSDF 노드 2
        node_BSDF_2 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_2.location = (230, -250)
        node_BSDF_2.inputs[12].default_value = 0

        # Principled BSDF 노드 3
        node_BSDF_3 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_3.location = (230, -750)
        node_BSDF_3.inputs[12].default_value = 0

        # Principled BSDF 노드 4
        node_BSDF_4 = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_BSDF_4.location = (230, -1250)
        node_BSDF_4.inputs[12].default_value = 0

        # Mix Shader 노드 1
        node_MixShader_1 = nodes.new(type='ShaderNodeMixShader')
        node_MixShader_1.location = (730, 0)

        # Mix Shader 노드 2
        node_MixShader_2 = nodes.new(type='ShaderNodeMixShader')
        node_MixShader_2.location = (1230, -250)

        # Mix Shader 노드 3
        node_MixShader_3 = nodes.new(type='ShaderNodeMixShader')
        node_MixShader_3.location = (1730, -500)

        # Color Attribute 노드
        node_ColorAttribute = nodes.new(type='ShaderNodeVertexColor')
        node_ColorAttribute.location = (0, 500)

        # Separate Color 노드
        node_SeparateColor = nodes.new(type='ShaderNodeSeparateColor')
        node_SeparateColor.location = (300, 500)


        # Node link
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_1.inputs[0])
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_2.inputs[0])
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_3.inputs[0])
        node_tree.links.new(node_TexCoord.outputs[2], node_Mapping_4.inputs[0])
        node_tree.links.new(node_Mapping_1.outputs[0], node_TexImage_1.inputs[0])
        node_tree.links.new(node_Mapping_2.outputs[0], node_TexImage_2.inputs[0])
        node_tree.links.new(node_Mapping_3.outputs[0], node_TexImage_3.inputs[0])
        node_tree.links.new(node_Mapping_4.outputs[0], node_TexImage_4.inputs[0])
        node_tree.links.new(node_TexImage_1.outputs[0], node_BSDF_1.inputs[0])
        node_tree.links.new(node_TexImage_2.outputs[0], node_BSDF_2.inputs[0])
        node_tree.links.new(node_TexImage_3.outputs[0], node_BSDF_3.inputs[0])
        node_tree.links.new(node_TexImage_4.outputs[0], node_BSDF_4.inputs[0])
        node_tree.links.new(node_ColorAttribute.outputs[0], node_SeparateColor.inputs[0])
        node_tree.links.new(node_SeparateColor.outputs[0], node_MixShader_1.inputs[0])
        node_tree.links.new(node_SeparateColor.outputs[1], node_MixShader_2.inputs[0])
        node_tree.links.new(node_SeparateColor.outputs[2], node_MixShader_3.inputs[0])
        node_tree.links.new(node_BSDF_1.outputs[0], node_MixShader_1.inputs[1])
        node_tree.links.new(node_BSDF_2.outputs[0], node_MixShader_1.inputs[2])
        node_tree.links.new(node_BSDF_3.outputs[0], node_MixShader_2.inputs[2])
        node_tree.links.new(node_BSDF_4.outputs[0], node_MixShader_3.inputs[2])
        node_tree.links.new(node_MixShader_1.outputs[0], node_MixShader_2.inputs[1])
        node_tree.links.new(node_MixShader_2.outputs[0], node_MixShader_3.inputs[1])
        node_tree.links.new(node_MixShader_3.outputs[0], node_output.inputs[0])

        # 머티리얼 할당
        obj.data.materials.append(material)

        return {'FINISHED'}


class SHADER_OT_TwoSideTex(Operator):
    bl_label = "TwoSideTex"
    bl_idname = 'shader.twosidetex_operator'

    def execute(self, context):

        # material_name 존재여부 체크 : True / False
        def check_material_exist(material_name):
            return material_name in bpy.data.materials

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

# 외부 노드 리스트

        # Material Output 노드
        material_output = nodes.get('Material Output')
        material_output.location = (100, 0)

        # Images Texture 노드 1
        node_TexImage_1 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_1.location = (-600, 200)

        # Images Texture 노드 2
        node_TexImage_2 = nodes.new(type='ShaderNodeTexImage')
        node_TexImage_2.location = (-600, -200)

# 노드 그룹 관련 ========================================
        
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

        

# 노드 그룹 내부 노드 리스트 ===================================

        # Group Input 노드
        group_in = group.nodes.new(type='NodeGroupInput')
        group_in.location = (-600, 0)

        # Group Output 노드
        group_out = group.nodes.new(type='NodeGroupOutput')
        group_out.location = (1000, 0)

    # Group Input / Output 소켓 추가 ===================================
        group.interface.new_socket(name="Fornt Image", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Face Tint", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Face Alpha", in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket(name="Back Image", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Back Tint", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Back Alpha", in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')

        # 소켓 디폴트값 설정
        node_group.inputs.get('Face Tint').default_value = (1.0, 1.0, 1.0, 1.0)
        node_group.inputs.get('Back Tint').default_value = (1.0, 1.0, 1.0, 1.0)

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
        group.links.new(group_in.outputs[0], node_Math_1.inputs[0]) # image 1
        group.links.new(group_in.outputs[1], node_Math_1.inputs[1]) # Tint 1
        group.links.new(group_in.outputs[2], node_BSDF_1.inputs[4]) # Alpha 1

        group.links.new(group_in.outputs[3], node_Math_2.inputs[0]) # image 2
        group.links.new(group_in.outputs[4], node_Math_2.inputs[1]) # Tint 2
        group.links.new(group_in.outputs[5], node_BSDF_2.inputs[4]) # Alpha 2

        group.links.new(node_Math_1.outputs[0], node_BSDF_1.inputs[0])
        group.links.new(node_Math_2.outputs[0], node_BSDF_2.inputs[0])
        group.links.new(node_Geometry.outputs[6], node_MixShader.inputs[0])
        group.links.new(node_BSDF_1.outputs[0], node_MixShader.inputs[1])
        group.links.new(node_BSDF_2.outputs[0], node_MixShader.inputs[2])
        group.links.new(node_MixShader.outputs[0], group_out.inputs[0])

        # Material Output 노드에 Node Group 적용
        material.node_tree.links.new(node_TexImage_1.outputs[0], node_group.inputs[0]) # Image 1
        material.node_tree.links.new(node_TexImage_1.outputs[1], node_group.inputs[2]) # Alpha 1
        material.node_tree.links.new(node_TexImage_2.outputs[0], node_group.inputs[3]) # Image 2
        material.node_tree.links.new(node_TexImage_2.outputs[0], node_group.inputs[5]) # Alpha 2
        material.node_tree.links.new(node_group.outputs[0], material_output.inputs[0])

        # 머티리얼 할당
        obj.data.materials.append(material)

        return {'FINISHED'}

classes = [
    SHADER_PT_MainPanel,
    SHADER_OT_Blend2Tex,
    SHADER_OT_Blend3Tex,
    SHADER_OT_Blend4Tex,
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