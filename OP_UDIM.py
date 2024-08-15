import bpy
import os

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

# 이미지 중복 방지
def check_image_exist(image_name, size):
    if image_name in bpy.data.images:
        image = bpy.data.images[image_name]
        bpy.data.images.remove(image)

    image = bpy.data.images.new(image_name, width=size, height=size, tiled=True)

    return image


texture_size = 256
material_name = "UDIM"

# 이미지 텍스쳐 생성
image = check_image_exist(material_name, texture_size)

# 머티리얼 노드 트리 기본
material = check_material_exist(material_name)
node_tree = material.node_tree
nodes = node_tree.nodes
nodes.remove(nodes.get('Principled BSDF'))

# 노드 리스트

# # Material Output 노드
node_output = nodes.get('Material Output')
node_output.location = (1000, 0)

# # Images Texture 노드 1
node_TexImage_1 = nodes.new(type='ShaderNodeTexImage')
node_TexImage_1.location = (-70, 250)
node_TexImage_1.image = image

# # Principled BSDF 노드 1
node_BSDF_1 = nodes.new(type='ShaderNodeBsdfPrincipled')
node_BSDF_1.location = (230, 250)
node_BSDF_1.inputs[12].default_value = 0

# # Node link
node_tree.links.new(node_TexImage_1.outputs['Color'], node_BSDF_1.inputs['Base Color'])
node_tree.links.new(node_BSDF_1.outputs['BSDF'], node_output.inputs['Surface'])

selObjs = bpy.context.selected_objects
bpy.ops.object.select_all(action="DESELECT")

num = 1000

for obj in selObjs:
    bpy.context.view_layer.objects.active = obj
    obj.data.materials.clear()
    obj.data.materials.append(material)
    num += 1
    bpy.data.images['UDIM'].tiles.new(num, label=str(num))
