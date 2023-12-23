import bpy

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

# 선택한 오브젝트의 머티리얼 슬롯을 모두 제거
obj = bpy.context.object
obj.data.materials.clear()

# 머티리얼 노드 트리 기본
material = check_material_exist(obj.name)
node_tree = material.node_tree
nodes = node_tree.nodes
nodes.remove(nodes.get('Principled BSDF'))

# 노드 리스트

# Material Output 노드
node_output = nodes.get('Material Output')
node_output.location = (1000, 0)

# Texture Coordinate 노드
node_TexCoord = nodes.new(type='ShaderNodeTexCoord')
node_TexCoord.location = (-600, 0)
node_TexCoord.object = obj

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

# VertexColor 노드
node_VertexColor = nodes.new(type='ShaderNodeVertexColor')
node_VertexColor.location = (230, 500)


# Node link
node_tree.links.new(node_TexCoord.outputs['UV'], node_Mapping_1.inputs['Vector'])
node_tree.links.new(node_TexCoord.outputs['UV'], node_Mapping_2.inputs['Vector'])
node_tree.links.new(node_Mapping_1.outputs['Vector'], node_TexImage_1.inputs['Vector'])
node_tree.links.new(node_Mapping_2.outputs['Vector'], node_TexImage_2.inputs['Vector'])
node_tree.links.new(node_TexImage_1.outputs['Color'], node_BSDF_1.inputs['Base Color'])
node_tree.links.new(node_TexImage_2.outputs['Color'], node_BSDF_2.inputs['Base Color'])
node_tree.links.new(node_VertexColor.outputs['Color'], node_MixShader.inputs['Fac'])
node_tree.links.new(node_BSDF_1.outputs['BSDF'], node_MixShader.inputs[1])
node_tree.links.new(node_BSDF_2.outputs['BSDF'], node_MixShader.inputs[2])
node_tree.links.new(node_MixShader.outputs[0], node_output.inputs['Surface'])

# 머티리얼 할당
obj.data.materials.append(material)