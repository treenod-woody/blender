import bpy
import math
import os

# 사용할 렌더링 엔진 설정 및 카메라 렌더링 배경 투명도 True
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.resolution_x = 256
bpy.context.scene.render.resolution_y = 256

# Save Directiry
file_path = bpy.data.filepath
export_dir = os.path.dirname(file_path) + "/MissionIcon/"

# Check directory
if not os.path.exists(export_dir):
    os.makedirs(export_dir)
    print("Create folder")
else:
    print("Exist folder:", export_dir)

# Camera 변수
cam_name = "RenderCamera"
cam_location = (0, -8.2668, 0)
cam_rotation = (90, 0, 0)

# LightA 변수
lit_A_name = "LightA"
lit_A_location = (0, -5.59733, -3.39775)
lit_A_rotation = (121.58, 0, 0)

# LightB 변수
lit_B_name = "LightB"
lit_B_location = (0, 0, 8.65)
lit_B_rotation = (2.9658, 0, 0)

# 씬에 카메라 추가(location & rotation setting)
def add_camera_to_scene(name, location, rotation):
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.name = name
    bpy.context.scene.camera = camera
    camera.rotation_euler = [math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2])]
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 1.0

# 씬에 Area타입의 조명 추가
def add_area_light_to_scene(name, location, rotation):
    bpy.ops.object.light_add(type='AREA', location=(location))
    light = bpy.context.object
    light.name = name
    light.data.energy = 1256.6
    light.data.shape = 'ELLIPSE'
    light.data.size = 20.3
    light.data.size_y = 12.7
    light.rotation_euler = [math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2])]

# 카메라와 조명 제거 함수
#def remove_camera_and_lights():
#    # 모든 객체 순회
#    for obj in bpy.context.scene.objects:
#        # 객체가 카메라 또는 조명인 경우
#        if obj.type == 'CAMERA' or obj.type == 'LIGHT':
#            # 해당 객체 제거
#            bpy.context.collection.objects.unlink(obj)


# 카메라와 라이트 생성
add_camera_to_scene(cam_name, cam_location, cam_rotation)
add_area_light_to_scene(lit_A_name, lit_A_location, lit_A_rotation)
add_area_light_to_scene(lit_B_name, lit_B_location, lit_B_rotation)


# -------------- mission icon make ----------------


objList = []

# except 'Camera' and 'Light' in objList
for obj in bpy.data.objects:
    if (obj.name == cam_name) or (obj.name == lit_A_name) or (obj.name == lit_B_name):
        print("Camera or Light")
    else :
        objList.append(obj)
        obj.location = (10, 0, 0)
        
# 미션 아이콘 이미지 렌더링
for obj in objList:
    obj.hide_set(False, view_layer=None)
    obj.location = (0, 0, 0)
    bpy.context.scene.render.filepath = export_dir + obj.name + '_Icon.png'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    obj.location = (10, 0, 0)
    

# 블럭 재정렬
xPos, yPos, zPos = 0.5, 0.5, 0.5
column = 10

#objs = bpy.context.selected_objects
objList.sort(key = lambda o: o.name)

for obj in objList:
    obj.location = (xPos, yPos, zPos)
    if xPos < (column - 1):
        xPos += 1.0
    elif xPos > (column - 1):
        xPos = 0.5
        yPos -= 1.0
        zPos -= 1.0

# 카메라와 라이트 제거
for cam in bpy.data.cameras:
    bpy.data.cameras.remove(cam)
    
for lit in bpy.data.lights:
    bpy.data.lights.remove(lit)