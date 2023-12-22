bl_info = {
    "name": "CatPuzzle",
    "author": "Woody",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "캐주얼G팀 CAT Puzzle 블럭 제작에 필요한 애드온입니다.",
    "doc_url": "https://treenod.atlassian.net/wiki/spaces/CGP/pages/71737541370/CAT",
    "category": "3D View",
}


import bpy
import os
import math

# 애드온 Operation 메뉴 설정
class CatPuzzleMenu(bpy.types.Menu):
    """CAT 블럭 제작을 위한 기능들"""
    bl_idname = "OBJECT_MT_cat_puzzle_menu"
    bl_label = "Cat"

    def draw(self, context):
        layout = self.layout
        
        layout.operator(MatchName.bl_idname, text=MatchName.bl_label) # Match Name
        layout.operator(BlockSort.bl_idname, text=BlockSort.bl_label) # Block Sort
        
        layout.separator()
        
        layout.operator(ExportUV.bl_idname, text=ExportUV.bl_label) # Export UV
        layout.operator(ExportOBJ.bl_idname, text=ExportOBJ.bl_label) # Export OBJ
        layout.operator(ExportFBX.bl_idname, text=ExportFBX.bl_label) # Export FBX
        
        layout.separator()
        
        layout.operator(CollisionMaker.bl_idname, text=CollisionMaker.bl_label) # Collision Maker
        layout.operator(PickingMaker.bl_idname, text=PickingMaker.bl_label) # Picking Maker
        
        layout.separator()
        
        layout.operator(CleanSetting.bl_idname, text=CleanSetting.bl_label) # Clean Setting
        layout.operator(BlockRotationInfo.bl_idname, text=BlockRotationInfo.bl_label) # Block Rotation Info
        layout.operator(MissionIconMaker.bl_idname, text=MissionIconMaker.bl_label) # Mission Icon Maker
        
        layout.separator()


# 데이터 이름을 오브젝트 이름으로 변경
class MatchName(bpy.types.Operator):
    """데이터 이름을 오브젝트 이름으로 변경합니다."""
    bl_idname = "object.match_name"
    bl_label = "Match name"
    
    def execute(self, context):
        
        num = 0

        for mesh in bpy.data.meshes:
            mesh.name = str(num)
            num += 1
            
        for obj in bpy.data.objects:
            obj.data.name = obj.name
                            
        return {'FINISHED'}

# 블럭을 그리드 간격으로 정렬
class BlockSort(bpy.types.Operator):
    """선택된 블럭들을 그리드 단위로 정렬시킵니다."""
    bl_idname = "object.block_sort"
    bl_label = "Block sort"
    bl_options = {'REGISTER', 'UNDO'}

    column: bpy.props.IntProperty(name="열 개수(min 5 ~ max 50)", default=10, min=1, max=100)
    
    def execute(self, context):

        xPos, yPos, zPos = 0.5, 0.5, 0.5

        objs = context.selected_objects
        objs.sort(key = lambda o: o.name)

        for obj in objs:
            obj.location = (xPos, yPos, zPos)
            if xPos < (self.column - 1):
                xPos += 1.0
            elif xPos > (self.column - 1):
                xPos = 0.5
                yPos -= 1.0
                zPos -= 1.0

        return {'FINISHED'}

# 충돌 메쉬용 큐브 생성
class CollisionMaker(bpy.types.Operator):
    """Collision Cube를 오브젝트 크기에 맞게 생성합니다."""
    bl_idname = "object.collision_maker"
    bl_label = "Collision maker"
    bl_options = {'REGISTER', 'UNDO'}
    
    scale: bpy.props.FloatProperty(name="Scale", default=0.1, min=0.01, max=0.2)
    
    def execute(self, context):
        selObj = bpy.context.selected_objects

        # Desellect All
        bpy.ops.object.select_all(action='TOGGLE')

        for obj in selObj:
            # Create Cube : select obj's location
            selObj_loc = bpy.data.objects[obj.name].location
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=selObj_loc)
            bpy.context.object.display_type = 'WIRE'
            
            # Set collision name & scale
            curObj = bpy.context.selected_objects[0]
            curObj.name = obj.name + "_Collision"
            curObj.data.name = obj.name + "_Collision"
            size = obj.dimensions
            curObj.scale = (size[0] + self.scale, size[1] + self.scale, size[2] + self.scale)
              
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
        return {'FINISHED'}

# 선택 메쉬 생성
class PickingMaker(bpy.types.Operator):
    """Picking Collision을 생성합니다."""
    bl_idname = "object.picking"
    bl_label = "Picking maker"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selObj = bpy.context.selected_objects

        bpy.ops.object.select_all(action='DESELECT')

        # Create Picking Collider
        for obj in selObj:
            
            if (obj.name.endswith('Collision')):
                
                newObjName = obj.name.replace("Collision", "Picking") 
                
                # Copy Object
                newObj = obj.copy()
                newObj.data = obj.data.copy()
                
                # Changing Name & Location of newObj
                newObj.name = newObjName
                newObj.data.name = newObjName
                newObj.location = obj.location
                
                # Insert main collection
                bpy.context.collection.objects.link(newObj)
                
                # add 'Displace' modifier & value setting
                mod = newObj.modifiers.new('Displace', type='DISPLACE')
                mod.strength = 0.25
                bpy.ops.object.modifier_apply(modifier="Displace")
                
                # Desellect All
                bpy.ops.object.select_all(action='DESELECT')
                    
        return {'FINISHED'}

# 선택한 오브젝트들의 UV를 Texture 폴더에 추출
class ExportUV(bpy.types.Operator):
    """선택된 오브젝트들의 UV를 한꺼번에 추출합니다."""
    bl_idname = "object.exportuv"
    bl_label = "Export UV"
    bl_options = {'REGISTER', 'UNDO'}
    
    texure_size: bpy.props.IntProperty(name="TextureSize", default=256, min=128, max=2048)
    
    # Export UV
    def execute(self, context):
        # Change Texture Size : N x N pixel
        texture_size = self.texure_size

        # Save directory
        file_path = bpy.data.filepath
        file_dir, file_name = os.path.split(file_path)
        export_dir = os.path.join(file_dir, 'Texture')

        # Check directory
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            print("Create folder")
        else:
            print("Exist folder:", export_dir)


        # Select Object List
        selObj = bpy.context.selected_objects

        # Desellect All
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selObj:
            # Save File Name
            export_path = os.path.join(export_dir, obj.name + '.png')

            # Export UV
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.export_layout(filepath = export_path, export_all = False, modified = False, mode = 'PNG', size = (texture_size, texture_size),opacity = 1.0)
            bpy.ops.object.mode_set(mode="OBJECT")
        
        return {'FINISHED'}

# 선택한 오브젝트들의 OBJ파일을 Obj 폴더에 추출
class ExportOBJ(bpy.types.Operator):
    """Obj파일을 한꺼번에 추출합니다."""
    bl_idname = "object.export_obj"
    bl_label = "Export OBJ"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Save directory
        file_path = bpy.data.filepath
        file_dir, file_name = os.path.split(file_path)
        export_dir = os.path.join(file_dir, 'Obj')

        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        else:
            print("폴더가 이미 존재합니다:", export_dir)

        # Select Object List
        selObj = bpy.context.selected_objects

        # Desellect All
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selObj:
            # Save File Name
            export_path = os.path.join(export_dir, obj.name + '.obj')
            print(export_path)
            # Export Obj
            obj.select_set(True)
            bpy.ops.wm.obj_export(filepath=export_path, export_selected_objects=True)
            bpy.ops.object.select_all(action='DESELECT')
            
        return {'FINISHED'}

# 선택한 오브젝트들의 FBX파일을 FBX 폴더에 추출
class ExportFBX(bpy.types.Operator):
    """FBX파일을 한꺼번에 추출합니다."""
    bl_idname = "object.export_fbx"
    bl_label = "Export FBX"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        # Save directory
        file_path = bpy.data.filepath
        file_dir, file_name = os.path.split(file_path)
        export_dir = os.path.join(file_dir, 'FBX')

        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        else:
            print("폴더가 이미 존재합니다:", export_dir)

        # Select Object List
        selObj = bpy.context.selected_objects

        # Desellect All
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selObj:
            # Save File Name
            export_path = os.path.join(export_dir, obj.name + '.fbx')
            print(export_path)
            # Export Obj
            obj.select_set(True)
        #    bpy.ops.wm.obj_export(filepath=export_path, export_selected_objects=True)
            
            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                object_types={'MESH'},  # 내보낼 오브젝트 타입 설정
                use_mesh_modifiers=True,
                mesh_smooth_type='FACE',
                bake_anim=False
            )
            
            bpy.ops.object.select_all(action='DESELECT')
        
        return {'FINISHED'}

# 머티리얼 및 이미지를 모두 재설정
class CleanSetting(bpy.types.Operator):
    """불필요한 Image와 Material을 제거하고 새로 생성합니다."""
    bl_idname = "object.clean_settings"
    bl_label = "Clean Setting"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        imgDir = os.path.dirname(bpy.data.filepath) + "/Texture/"

        # 모든 머티리얼 데이터 제거
        for mat in bpy.data.materials:
            bpy.data.materials.remove(mat)
            
        # 모든 이미지 데이터 제거
        for img in bpy.data.images:
            bpy.data.images.remove(img)
        
        for obj in bpy.data.objects:

            if (obj.name[-1] == 'Collision') or (obj.name[-1] == 'Picking'):
                continue
            
            name = obj.name    # 오브젝트 이름
            
            # Clear all material slot of object
            obj.data.materials.clear()
            
            # Assign material
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            texImage.image = bpy.data.images.load(imgDir + name + ".png")
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
            mat.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 0    # Specular value = '0'
            
            obj.data.materials.append(mat)    # Assign material to material slot
            
        return {'FINISHED'}

# 블럭 회전값 정보를 TXT 파일로 추출
class BlockRotationInfo(bpy.types.Operator):
    """블럭의 Rotation 정보를 txt 파일로 추출"""
    bl_idname = "object.block_rotation_info"
    bl_label = "Block Rotation Info"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        listName = []
        listVal = []
        cntObj = len(bpy.data.objects)
        data = ''

        # (블렌더파일명)_Rotation.txt
        save_path = bpy.data.filepath.replace('.blend', '_Rotation.txt')
        print(save_path)

        for obj in bpy.data.objects:
            listName.append(obj.name)
            rotation = obj.rotation_euler
            x = int(math.degrees(rotation.x))
            y = int(math.degrees(rotation.y))
            z = int(math.degrees(rotation.z))
            listVal.append((x,y,z))

        for i in range(1, cntObj + 1):
            data += f'{listName[i-1]},{listVal[i-1]},\n'
            
        f = open(save_path, 'w')
        f.write(data)
        f.close()
            
        return {'FINISHED'}

# 미션 아이콘 렌더링 이미지를 MissionIcon 폴더에 추출
class MissionIconMaker(bpy.types.Operator):
    """미션 아이콘을 생성합니다."""
    bl_idname = "object.mission_icon_maker"
    bl_label = "Mission Icon Maker"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
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
            
        return {'FINISHED'}
 


classes = [
    CatPuzzleMenu, 
    BlockSort,
    MatchName,
    ExportUV,
    ExportOBJ,
    ExportFBX,
    CollisionMaker,
    PickingMaker,
    CleanSetting,
    BlockRotationInfo,
    MissionIconMaker
]     


# Menu Space --------------------------------------------------------------------

def menu_func(self, context):
    self.layout.menu(CatPuzzleMenu.bl_idname, text=CatPuzzleMenu.bl_label)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.VIEW3D_MT_editor_menus.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    bpy.types.VIEW3D_MT_editor_menus.remove(menu_func)


if __name__ == "__main__":
    register()