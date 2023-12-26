import bpy, math, pprint

# 메시 체크 & 제거 (중복 방지)
def check_mesh_exist(mesh_name):
    if mesh_name in bpy.data.materials:
        mesh = bpy.data.materials[mesh_name]
        bpy.data.materials.remove(mesh)

# 선택한 오브젝트
origin_obj = bpy.context.active_object
origin_obj.location = (0,0,0)

segment = 16
angle_step = math.tau / segment
radius = 4

vert_coordinates = list()

delete_obj_name = ""

for i in range(segment):

    current_angle_step = i * angle_step

    x = radius * math.sin(current_angle_step)
    y = radius * math.cos(current_angle_step)

    # 선택한 오브젝트를 복제한 후 원래의 오브젝트에 데이터 링크
    copy_obj = origin_obj.copy()
    # copy_obj.data = origin_obj.data.copy()
    copy_obj.location = (x, y, 0)
    copy_obj_name = copy_obj.name

    # 메인 컬렉션에 복제된 오브젝트 링크
    bpy.context.collection.objects.link(copy_obj)

    # 데이터 링크
    copy_obj.select_set(True)
    origin_obj.select_set(True)
    bpy.context.view_layer.objects.active = origin_obj
    bpy.ops.object.make_links_data(type='OBDATA')
    bpy.ops.object.select_all(action='DESELECT')
    
    # 미사용 메시는 제거
    check_mesh_exist(copy_obj_name)
    
    vert_coordinates.append((x, y, 0))

pprint.pprint(vert_coordinates)