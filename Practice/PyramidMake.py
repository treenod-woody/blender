import bpy

# 메쉬 이름이 존재할 경우 제거
def check_mesh_exist(mesh_name):
    if mesh_name in bpy.data.meshes:
        mesh = bpy.data.meshes[mesh_name]
        bpy.data.meshes.remove(mesh)

verts = [
    (-1, -1, -1),
    (-1, 1, -1),
    (1, 1, -1),
    (1, -1, -1),
    (0, 0, 1)
]

faces = [
    (0, 1, 2, 3),
    (4, 1, 0),
    (4, 0, 3),
    (4, 3, 2),
    (4, 2, 1)
]

edges = []

mesh_name = "pyramid"

check_mesh_exist(mesh_name)

# mesh 데이터 블록 생성
mesh_data = bpy.data.meshes.new(mesh_name)
mesh_data.from_pydata(verts, edges, faces)

# object 데이터 블록 생성
mesh_obj = bpy.data.objects.new(mesh_name, mesh_data)

# collection에 obj 링크
bpy.context.collection.objects.link(mesh_obj)
