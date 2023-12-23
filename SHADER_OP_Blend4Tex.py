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

# Material Output 노드
node_output = nodes.get('Material Output')
node_output.location = (2200, -250)

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
node_VertexColor = nodes.new(type='ShaderNodeVertexColor')
node_VertexColor.location = (0, 500)

# Separate Color 노드
node_SeparateColor = nodes.new(type='ShaderNodeSeparateColor')
node_SeparateColor.location = (300, 500)


# Node link
node_tree.links.new(node_TexCoord.outputs['UV'], node_Mapping_1.inputs['Vector'])
node_tree.links.new(node_TexCoord.outputs['UV'], node_Mapping_2.inputs['Vector'])
node_tree.links.new(node_TexCoord.outputs['UV'], node_Mapping_3.inputs['Vector'])
node_tree.links.new(node_TexCoord.outputs['UV'], node_Mapping_4.inputs['Vector'])
node_tree.links.new(node_Mapping_1.outputs['Vector'], node_TexImage_1.inputs['Vector'])
node_tree.links.new(node_Mapping_2.outputs['Vector'], node_TexImage_2.inputs['Vector'])
node_tree.links.new(node_Mapping_3.outputs['Vector'], node_TexImage_3.inputs['Vector'])
node_tree.links.new(node_Mapping_4.outputs['Vector'], node_TexImage_4.inputs['Vector'])
node_tree.links.new(node_TexImage_1.outputs['Color'], node_BSDF_1.inputs['Base Color'])
node_tree.links.new(node_TexImage_2.outputs['Color'], node_BSDF_2.inputs['Base Color'])
node_tree.links.new(node_TexImage_3.outputs['Color'], node_BSDF_3.inputs['Base Color'])
node_tree.links.new(node_TexImage_4.outputs['Color'], node_BSDF_4.inputs['Base Color'])
node_tree.links.new(node_VertexColor.outputs['Color'], node_SeparateColor.inputs['Color'])
node_tree.links.new(node_SeparateColor.outputs['Red'], node_MixShader_1.inputs['Fac'])
node_tree.links.new(node_SeparateColor.outputs['Green'], node_MixShader_2.inputs['Fac'])
node_tree.links.new(node_SeparateColor.outputs['Blue'], node_MixShader_3.inputs['Fac'])
node_tree.links.new(node_BSDF_1.outputs[0], node_MixShader_1.inputs[1])
node_tree.links.new(node_BSDF_2.outputs[0], node_MixShader_1.inputs[2])
node_tree.links.new(node_BSDF_3.outputs[0], node_MixShader_2.inputs[2])
node_tree.links.new(node_BSDF_4.outputs[0], node_MixShader_3.inputs[2])
node_tree.links.new(node_MixShader_1.outputs[0], node_MixShader_2.inputs[1])
node_tree.links.new(node_MixShader_2.outputs[0], node_MixShader_3.inputs[1])
node_tree.links.new(node_MixShader_3.outputs[0], node_output.inputs['Surface'])

# 머티리얼 할당
obj.data.materials.append(material)