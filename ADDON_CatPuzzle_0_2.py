# MissionIcon Maker 수정

bl_info = {
    "name": "CatPuzzle",
    "author": "Woody",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "description": "캐주얼G팀 CAT Puzzle 블럭 제작에 필요한 애드온입니다.",
    "doc_url": "https://treenod.atlassian.net/wiki/spaces/CGP/pages/71737541370/CAT",
    "category": "3D View",
}


import bpy, os, math
from bpy.props import IntProperty, FloatProperty, EnumProperty


    # 메시 체크 & 제거 (중복 방지)
def check_mesh_exist(mesh_name):
    if mesh_name in bpy.data.meshes:
        mesh = bpy.data.meshes[mesh_name]
        bpy.data.meshes.remove(mesh)

def check_collection_exist(collection_name):
    if collection_name not in bpy.data.collections:
        # 'Collision' 컬렉션 생성
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)

# Class 리스트 =======================================

    # 애드온 Operation 메뉴 설정
class CatPuzzleMenu(bpy.types.Menu):
    """CAT 블럭 제작을 위한 기능들"""
    bl_idname = "OBJECT_MT_cat_puzzle_menu"
    bl_label = "Cat"

    def draw(self, context):
        layout = self.layout
            # MatchName & BlockSort
        layout.operator(MatchName.bl_idname, text=MatchName.bl_label, icon='SORTALPHA') # Match Name
        layout.operator(BlockSort.bl_idname, text=BlockSort.bl_label, icon="SNAP_VERTEX") # Block Sort
        layout.separator()
            # Export UV / OBJ / FBX
        layout.operator(ExportUV.bl_idname, text=ExportUV.bl_label, icon="TEXTURE") # Export UV
        layout.operator(ExportOBJ.bl_idname, text=ExportOBJ.bl_label, icon='EXPORT') # Export OBJ
        layout.operator(ExportFBX.bl_idname, text=ExportFBX.bl_label, icon='EXPORT') # Export FBX
        layout.separator()
            # Colission / Picking
        layout.operator(CollisionMaker.bl_idname, text=CollisionMaker.bl_label, icon='CUBE') # Collision Maker
        layout.operator(PickingMaker.bl_idname, text=PickingMaker.bl_label, icon='MESH_CUBE') # Picking Maker
        layout.separator()
            # Clean Setting / Rotation Info / Mission Icon
        layout.operator(CleanSetting.bl_idname, text=CleanSetting.bl_label, icon='BRUSH_DATA') # Clean Setting
        layout.operator(BlockRotationInfo.bl_idname, text=BlockRotationInfo.bl_label, icon='INFO') # Block Rotation Info
        layout.operator(MissionIconMaker.bl_idname, text=MissionIconMaker.bl_label, icon='OUTLINER_OB_CAMERA') # Mission Icon Maker
        layout.separator()


    # 데이터 이름을 오브젝트 이름으로 변경
class MatchName(bpy.types.Operator):
    """데이터 이름을 오브젝트 이름으로 변경합니다."""
    bl_idname = "object.match_name"
    bl_label = "Match name"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        num = 0
            # 전체 메쉬의 임시 이름을 지정 (중복 방지)
        for mesh in bpy.data.meshes:
            mesh.name = str(num)
            num += 1
            # 실제 사용될 이름으로 변경
        for obj in bpy.data.objects:
            obj.data.name = obj.name
                            
        return {'FINISHED'}

    # 블럭을 그리드 간격으로 정렬
class BlockSort(bpy.types.Operator):
    """선택된 블럭들을 그리드 단위로 정렬시킵니다."""
    bl_idname = "object.block_sort"
    bl_label = "Block sort"
    bl_options = {'REGISTER', 'UNDO'}

    column: IntProperty(name="열 개수 :", default=10, min=1, max=100) # type: ignore
    
    def execute(self, context):
            # 정렬 시작 포인트
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
        # 충돌 메시의 크기 가중치
    scale: FloatProperty(name="Scale", default=0.1, min=0.01, max=0.2) # type: ignore
    
    def execute(self, context):
        scale = self.scale
            # 선택된 오브젝트 리스트
        selected_objects = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        # 동일한 이름의 'Collision' 컬렉션이 존재 여부
        check_collection_exist('Collision')
        target_collection = bpy.data.collections.get('Collision')
        
        objs = []

        for obj in selected_objects:
            if (obj.name.endswith('Collision')) or (obj.name.endswith('Picking')):
                continue
            else:
                objs.append(obj)

        for obj in objs:

            collision_name = obj.name + "_Collision"
            # 동일한 이름의 Collision 메쉬가 존재하는지 체크 후 제거
            check_mesh_exist(collision_name)
            cube_size = obj.dimensions
            # 오브젝트 위치에 Collision Cube 생성 후 WIRE 모드로 변환
            bpy.ops.mesh.primitive_cube_add(size=1.0)
            collision_object = bpy.context.active_object
            collision_object.location = obj.location
            collision_object.scale = (cube_size[0] + scale, cube_size[1] + scale, cube_size[2] + scale)
            collision_object.name = collision_name
            collision_object.data.name = collision_name
            bpy.context.object.display_type = 'WIRE'
            
            # Applay Scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.select_all(action='DESELECT')

            # 컬렉션 이동
            collision_object.users_collection[0].objects.unlink(collision_object)
            target_collection.objects.link(collision_object)

        return {'FINISHED'}

    # Picking Collision 메쉬 생성
class PickingMaker(bpy.types.Operator):
    """Picking Collision을 생성합니다."""
    bl_idname = "object.picking"
    bl_label = "Picking maker"
    bl_options = {'REGISTER', 'UNDO'}

    strength : FloatProperty(name="Scale", default=0.25, min=0, max=0.5) # type: ignore
    
    def execute(self, context):
        strength = self.strength
            # 선택된 오브젝트 리스트
        selected_objects = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        # 동일한 이름의 'Picking' 컬렉션이 존재 여부
        check_collection_exist('Picking')
        target_collection = bpy.data.collections.get('Picking')

        # 이름에 'Collision'이 포함된 것만 추출
        col_objs = []
        for obj in selected_objects:
            if (obj.name.endswith('Collision')):
                col_objs.append(obj)

            # Picking Collision 메쉬 생성
        for obj in col_objs:
                # Picking 메쉬 중복 체크 후 제거
            picking_object_name = obj.name.replace("Collision", "Picking")
            check_mesh_exist(picking_object_name)

                # Picking 오브젝트 신규 생성 및 설정
            picking_object = obj.copy()
            picking_object.data = obj.data.copy()
            picking_object.name = picking_object_name
            picking_object.data.name = picking_object_name
            picking_object.location = obj.location
            
                # 생성된 Picking 오브젝트를 컬렉션에 링크
            bpy.context.collection.objects.link(picking_object)
            
                # Displace 모디파이어 설정
            mod = picking_object.modifiers.new('Displace', type='DISPLACE')
            mod.strength = strength
            bpy.ops.object.modifier_apply(modifier="Displace")
            bpy.ops.object.select_all(action='DESELECT')

            # 컬렉션 이동
            picking_object.users_collection[0].objects.unlink(picking_object)
            target_collection.objects.link(picking_object)
                    
        return {'FINISHED'}

    # 선택한 오브젝트들의 UV를 Texture 폴더에 추출
class ExportUV(bpy.types.Operator):
    """선택된 오브젝트들의 UV를 한꺼번에 추출합니다."""
    bl_idname = "object.exportuv"
    bl_label = "Export UV"
    bl_options = {'REGISTER', 'UNDO'}
    
    # texure_size: IntProperty(name="TextureSize", default=256, min=128, max=2048)
    texure_size: EnumProperty(
        name="Texture Size", 
        description="텍스쳐 크기를 지정합니다.",
        items=[('OP1', "256", ""),
               ('OP2', "512", ""),
               ('OP3', "1024", ""),
               ('OP4', "2048", ""),
               ('OP5', "4096", "")],
        default='OP1') # type: ignore
    opacity : FloatProperty(name="Opacity", default=1.0, min=0.0, max=1.0) # type: ignore
    
    # Export UV
    def execute(self, context):
        # Change Texture Size : N x N pixel
        texture_size = self.texure_size
        opacity = self.opacity
        tex_size = 0

        if texture_size == 'OP1':
            tex_size = 256
        elif texture_size == 'OP2':
            tex_size = 512
        elif texture_size == 'OP3':
            tex_size = 1024
        elif texture_size == 'OP4':
            tex_size = 2048
        elif texture_size == 'OP5':
            tex_size = 4096

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
        selected_objects = bpy.context.selected_objects

        # Desellect All
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selected_objects:
            # Save File Name
            export_path = os.path.join(export_dir, obj.name + '_UV.png')

            # Export UV
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.export_layout(filepath = export_path, export_all = False, modified = False, mode = 'PNG', size = (tex_size, tex_size),opacity = opacity)
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

            if ('Collision' not in obj.name) and ('Picking' not in obj.name):
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

        # 씬에 카메라 추가(location & rotation setting)
        def add_camera_to_scene(name, location, rotation):
            bpy.ops.object.camera_add(location=location)
            camera = bpy.context.object
            camera.name = name
            bpy.context.scene.camera = camera
            camera.rotation_euler = [math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2])]
            camera.data.type = 'ORTHO'
            camera.data.ortho_scale = 1.0


        # 카메라와 생성
        add_camera_to_scene(cam_name, cam_location, cam_rotation)

        # 3D 뷰포트 영역 활성화
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'

        # 오버레이 숨기기
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.overlay.show_overlays = False


        # -------------- mission icon make ----------------


        objList = []

        # except 'Camera' in objList
        for obj in bpy.data.objects:
            if (obj.name == cam_name):
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
            bpy.ops.render.opengl(write_still=True)
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

        # 카메라 제거
        for cam in bpy.data.cameras:
            bpy.data.cameras.remove(cam)
            
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