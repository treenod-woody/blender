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
material.blend_method = 'CLIP'
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
group.interface.new_socket(name="Face Image", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Face Tint", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Face Alpha", in_out='INPUT', socket_type='NodeSocketFloat')
group.interface.new_socket(name="Back Image", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Back Tint", in_out='INPUT', socket_type='NodeSocketColor')
group.interface.new_socket(name="Back Alpha", in_out='INPUT', socket_type='NodeSocketFloat')
group.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')

# 소켓 디폴트값 설정
node_group.inputs.get('Face Tint').default_value = (1.0, 1.0, 1.0, 1.0)
node_group.inputs.get('Back Tint').default_value = (1.0, 1.0, 1.0, 1.0)

# Mix Color 노드 1
node_MixColor_1 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_1.location = (-250, 200)
node_MixColor_1.data_type = 'RGBA'
node_MixColor_1.blend_type = 'MULTIPLY'

# Mix Color 노드 2
node_MixColor_2 = group.nodes.new(type='ShaderNodeMix')
node_MixColor_2.location = (-250, -200)
node_MixColor_2.data_type = 'RGBA'
node_MixColor_2.blend_type = 'MULTIPLY'

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

# 노드 링크 ===============================================================================
group.links.new(group_in.outputs['Face Image'], node_MixColor_1.inputs['A'])
group.links.new(group_in.outputs['Face Tint'], node_MixColor_1.inputs['B'])
group.links.new(group_in.outputs['Face Alpha'], node_BSDF_1.inputs['Alpha'])

group.links.new(group_in.outputs['Back Image'], node_MixColor_2.inputs['A'])
group.links.new(group_in.outputs['Back Tint'], node_MixColor_2.inputs['B'])
group.links.new(group_in.outputs['Back Alpha'], node_BSDF_2.inputs['Alpha'])

group.links.new(node_MixColor_1.outputs['Result'], node_BSDF_1.inputs['Base Color'])  # BSDF 1
group.links.new(node_MixColor_2.outputs['Result'], node_BSDF_2.inputs['Base Color'])  # BSDF 2
group.links.new(node_Geometry.outputs['Backfacing'], node_MixShader.inputs['Fac']) # Geometry
group.links.new(node_BSDF_1.outputs['BSDF'], node_MixShader.inputs[1])   # Mix Shader
group.links.new(node_BSDF_2.outputs['BSDF'], node_MixShader.inputs[2])   # Mix Shader
group.links.new(node_MixShader.outputs[0], group_out.inputs[0])     # Group Output

# Material Output 노드에 Node Group 적용
material.node_tree.links.new(node_TexImage_1.outputs['Color'], node_group.inputs['Face Image']) # Image 1
material.node_tree.links.new(node_TexImage_1.outputs['Alpha'], node_group.inputs['Face Alpha']) # Alpha 1
material.node_tree.links.new(node_TexImage_2.outputs['Color'], node_group.inputs['Back Image']) # Image 2
material.node_tree.links.new(node_TexImage_2.outputs['Alpha'], node_group.inputs['Back Alpha']) # Alpha 2
material.node_tree.links.new(node_group.outputs[0], material_output.inputs[0]) # Material Output

# 머티리얼 할당
obj.data.materials.append(material)