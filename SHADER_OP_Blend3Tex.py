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
        row.operator(SHADER_OT_Blend3Tex.bl_idname, text=SHADER_OT_Blend3Tex.bl_label)

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



classes = [
    SHADER_PT_MainPanel,
    SHADER_OT_Blend3Tex
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()