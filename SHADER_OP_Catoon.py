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


# 그룹 노드 존재한다면 제거
def check_group_node_exists(group_node_name):
    group_node_name = group_node_name
    group_node = bpy.data.node_groups.get(group_node_name)

    if group_node is not None:
        bpy.data.node_groups.remove(group_node)

    # 'CatoonGroup' 노드 그룹 데이터 블록 생성
    bpy.data.node_groups.new(group_node_name, 'ShaderNodeTree')
    node_group = nodes.new(type='ShaderNodeGroup')

    return node_group


# 선택한 오브젝트에 머티리얼 할당
obj = bpy.context.object
obj.data.materials.clear()
material = check_material_exist(obj.name)
obj.data.materials.append(material)

# 노드 트리 기본 세팅
node_tree = material.node_tree
nodes = node_tree.nodes
nodes.remove(nodes.get('Principled BSDF'))

# 노드 리스트 =============================================

# Material Output 노드
material_output = nodes.get('Material Output')
material_output.location = (100, 0)

# Images Texture 노드 1
node_TexImage = nodes.new(type='ShaderNodeTexImage')
node_TexImage.location = (-400, 0)


group_node_name = "CatoonGroup"
node_group = check_group_node_exists(group_node_name)
node_group.node_tree = bpy.data.node_groups[group_node_name]
node_group.location = (-100, 0)
group = node_group.node_tree

# Group Input 노드
group_in = group.nodes.new(type='NodeGroupInput')
group_in.location = (500, -300)

# Group Output 노드
group_out = group.nodes.new(type='NodeGroupOutput')
group_out.location = (1900, 0)

# Group Input / Output 소켓 추가
group.interface.new_socket(name="Base Color", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Shadow Color", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Key Light Color", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Fill Light Color", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Back Light Color", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type='NodeSocketColor')

# Diffuse BSDF 노드
node_BSDF = group.nodes.new(type='ShaderNodeBsdfDiffuse')
node_BSDF.location = (-400, 0)

# ShaderToRGB 노드
node_ShaderToRGB = group.nodes.new(type='ShaderNodeShaderToRGB')
node_BSDF.location = (-200, 0)

# SeperateColor 노드
node_SeperateColor = group.nodes.new(type='ShaderNodeSeparateColor')
node_SeperateColor.location = (200, 0)

# Frame 노드 : Outline
# frame_Outline = group.nodes.new(type='NodeFrame')
# frame_Outline.label = "Outline"
# frame_Outline.location = (400, 200)

# Math : Multiply 노드
node_Math = group.nodes.new(type='ShaderNodeMath')
node_Math.operation = 'MULTIPLY'
node_Math.inputs[1].default_value = 26
node_Math.location = (400, 200)

# LayerWeight 노드
node_LayerWeight = group.nodes.new(type='ShaderNodeLayerWeight')
node_LayerWeight.location = (400, 400)

# Math : Power 노드
node_Power = group.nodes.new(type='ShaderNodeMath')
node_Power.operation = 'POWER'
node_Power.location = (600, 300)

# ColorRamp_1 노드
node_ColorRamp_1 = group.nodes.new(type='ShaderNodeValToRGB')
node_ColorRamp_1.color_ramp.elements[0].position = 0.15
node_ColorRamp_1.color_ramp.elements[0].color = (0, 0, 0, 1)
node_ColorRamp_1.color_ramp.elements[1].position = 0.2
node_ColorRamp_1.color_ramp.elements[1].color = (1, 1, 1, 1)
node_ColorRamp_1.location = (800, 300)
node_ColorRamp_1.hide = True

# ColorRamp_2 노드
node_ColorRamp_2 = group.nodes.new(type='ShaderNodeValToRGB')
node_ColorRamp_2.location = (400, 0)
node_ColorRamp_2.hide = True

# ColorRamp_3 노드
node_ColorRamp_3 = group.nodes.new(type='ShaderNodeValToRGB')
node_ColorRamp_3.location = (400, -50)
node_ColorRamp_3.hide = True

# ColorRamp_4 노드
node_ColorRamp_4 = group.nodes.new(type='ShaderNodeValToRGB')
node_ColorRamp_4.location = (400, -100)
node_ColorRamp_4.hide = True

# Mix Color 노드 1
node_MixColor_1 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_1.location = (700, -150)
node_MixColor_1.data_type = 'RGBA'
node_MixColor_1.blend_type = 'MULTIPLY'
node_MixColor_1.inputs['Factor'].default_value = 1.0
node_MixColor_1.hide = True

# Mix Color 노드 2
node_MixColor_2 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_2.location = (700, -200)
node_MixColor_2.data_type = 'RGBA'
node_MixColor_2.blend_type = 'MULTIPLY'
node_MixColor_2.inputs['Factor'].default_value = 1.0
node_MixColor_2.hide = True

# Mix Color 노드 3
node_MixColor_3 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_3.location = (700, -250)
node_MixColor_3.data_type = 'RGBA'
node_MixColor_3.blend_type = 'MULTIPLY'
node_MixColor_3.inputs['Factor'].default_value = 1.0
node_MixColor_3.hide = True

# Mix Color 노드 4
node_MixColor_4 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_4.location = (900, -300)
node_MixColor_4.data_type = 'RGBA'
node_MixColor_4.blend_type = 'LIGHTEN'
node_MixColor_4.inputs['Factor'].default_value = 1.0
node_MixColor_4.hide = True

# Mix Color 노드 5
node_MixColor_5 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_5.location = (1100, -250)
node_MixColor_5.data_type = 'RGBA'
node_MixColor_5.blend_type = 'MULTIPLY'
node_MixColor_5.inputs['Factor'].default_value = 1.0
node_MixColor_5.hide = True

# Mix Color 노드 6
node_MixColor_6 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_6.location = (1300, -200)
node_MixColor_6.data_type = 'RGBA'
node_MixColor_6.blend_type = 'ADD'
node_MixColor_6.inputs['Factor'].default_value = 1.0
node_MixColor_6.hide = True

# Mix Color 노드 7
node_MixColor_7 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_7.location = (1500, -150)
node_MixColor_7.data_type = 'RGBA'
node_MixColor_7.blend_type = 'ADD'
node_MixColor_7.inputs['Factor'].default_value = 1.0
node_MixColor_7.hide = True

# Mix Color 노드 8
node_MixColor_8 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_8.location = (1700, -100)
node_MixColor_8.data_type = 'RGBA'
node_MixColor_8.blend_type = 'MIX'
node_MixColor_8.inputs['A'].default_value = (0.0, 0.0, 0.0, 1.0)
node_MixColor_8.hide = True

# 노드 내부 링크 ==========================================================
group.links.new(node_BSDF.outputs['BSDF'], node_ShaderToRGB.inputs['Shader'])
group.links.new(node_ShaderToRGB.outputs['Color'], node_SeperateColor.inputs['Color'])
group.links.new(node_SeperateColor.outputs['Red'], node_Math.inputs[0])
group.links.new(node_LayerWeight.outputs['Fresnel'], node_Power.inputs[0])
group.links.new(node_Math.outputs['Value'], node_Power.inputs[1])
group.links.new(node_Power.outputs[0], node_ColorRamp_1.inputs[0])
group.links.new(node_SeperateColor.outputs['Red'], node_ColorRamp_2.inputs[0])
group.links.new(node_SeperateColor.outputs['Green'], node_ColorRamp_3.inputs[0])
group.links.new(node_SeperateColor.outputs['Blue'], node_ColorRamp_4.inputs[0])
group.links.new(node_ColorRamp_2.outputs['Color'], node_MixColor_1.inputs['A'])
group.links.new(node_ColorRamp_3.outputs['Color'], node_MixColor_2.inputs['A'])
group.links.new(node_ColorRamp_4.outputs['Color'], node_MixColor_3.inputs['A'])
group.links.new(group_in.outputs['Key Light Color'], node_MixColor_1.inputs['B'])
group.links.new(group_in.outputs['Fill Light Color'], node_MixColor_2.inputs['B'])
group.links.new(group_in.outputs['Back Light Color'], node_MixColor_3.inputs['B'])
group.links.new(node_MixColor_1.outputs['Result'], node_MixColor_4.inputs['A'])
group.links.new(group_in.outputs['Shadow Color'], node_MixColor_4.inputs['B'])
group.links.new(node_MixColor_4.outputs['Result'], node_MixColor_5.inputs['A'])
group.links.new(group_in.outputs['Base Color'], node_MixColor_5.inputs['B'])
group.links.new(node_MixColor_5.outputs['Result'], node_MixColor_6.inputs['A'])
group.links.new(node_MixColor_2.outputs['Result'], node_MixColor_6.inputs['B'])
group.links.new(node_MixColor_6.outputs['Result'], node_MixColor_7.inputs['A'])
group.links.new(node_MixColor_3.outputs['Result'], node_MixColor_7.inputs['B'])
group.links.new(node_ColorRamp_1.outputs['Color'], node_MixColor_8.inputs['Factor'])
group.links.new(node_MixColor_7.outputs['Result'], node_MixColor_8.inputs['B'])
group.links.new(node_MixColor_8.outputs['Result'], group_out.inputs['Color'])


# 노드 외부 링크 ==========================================================
# material.node_tree.links.new(node_TexImage.outputs['Color'], node_group.inputs['Color'])
material.node_tree.links.new(node_group.outputs['Color'], material_output.inputs['Surface'])