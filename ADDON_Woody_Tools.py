bl_info = {
    "name": "Woody Tools Add-on",
    "author": "Woody",
    "version": (0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Woody Tools Tab",
    "description": "CAT 블럭 모델링에 유용한 도구 모음",
    "warning": "",
    "wiki_url": "",
    "category": "Woody Tools",
}

from typing import Set
import bpy
import bmesh
from bpy.types import Panel, Operator

# Main Panel : 사이드바 메인 메뉴 UI 세팅
class OBJECT_PT_WoodyTool(Panel):
    bl_label = "Woody Tools"
    bl_idname = "OBJECT_PT_woodytool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Woody"
    
    def draw(self, context):
        layout = self.layout

        # Transform
        selected_object = bpy.context.object

        # 선택한 오브젝트의 Properties 사용
        layout.label(text="Transform :", icon="OUTLINER_DATA_EMPTY")
        layout.prop(selected_object, "location", text="")
        layout.prop(selected_object, "rotation_euler", text="")
        layout.prop(selected_object, "scale", text="")

        layout.separator(factor=1)

        # Cylinder
        layout.label(text="Cyliner :", icon= 'MESH_CYLINDER')
        row = layout.row()
        row.operator(Add_Cylinder_6.bl_idname, text= Add_Cylinder_6.bl_label) # 버튼 : 8각형
        row.operator(Add_Cylinder_8.bl_idname, text= Add_Cylinder_8.bl_label) # 버튼 : 8각형
        row.operator(Add_Cylinder_10.bl_idname, text= Add_Cylinder_10.bl_label) # 버튼 : 10각형
        row.operator(Add_Cylinder_12.bl_idname, text= Add_Cylinder_12.bl_label) # 버튼 : 12각형

        layout.separator(factor=1)

        # Material & Text
        row = layout.row()
        row.operator(Add_Material.bl_idname, text= Add_Material.bl_label, icon= 'NODE_MATERIAL')
        row.operator(Add_Text.bl_idname, text= Add_Text.bl_label, icon= 'OUTLINER_OB_FONT')

        layout.separator(factor=1)

        # Modifyers
        layout.label(text="Modifyer :", icon= 'MODIFIER_DATA')
        layout.operator(Add_Lattice.bl_idname, text= Add_Lattice.bl_label, icon= 'MOD_LATTICE')
        row = layout.row()
        # Mirror 모디파이어 추가 버튼
        row.operator(Add_Mirror_X_Modifier.bl_idname, text=Add_Mirror_X_Modifier.bl_label, icon="MOD_MIRROR")
        row.operator(Add_Mirror_Y_Modifier.bl_idname, text=Add_Mirror_Y_Modifier.bl_label, icon="MOD_MIRROR")
        row.operator(Add_Mirror_Z_Modifier.bl_idname, text=Add_Mirror_Z_Modifier.bl_label, icon="MOD_MIRROR")

# Text Panel : 텍스트 생성 후 텍스트 Spacing 옵션 ----------------------------------------

class OBJECT_PT_Spacing(Panel):
    bl_label = "Text Spacing"
    bl_idname = "OBJECT_PT_spacing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Woody"
    bl_parentid = "OBJECT_PT_woodytool"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        text = context.object.data

        row = layout.row()
        row.label(text= "텍스트 Spacing 옵션 설정")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Character:")
        row.prop(text, "space_character", text= "")

        row = layout.split(factor= 0.45)
        row.label(text= "Word:")
        row.prop(text, "space_word", text= "")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Line:")
        row.prop(text, "space_line", text= "")

class OBJECT_PT_Mirror_Modifier(Panel):
    bl_label = "Mirror Axis"
    bl_idname = "OBJECT_PT_Mirror_Modifier"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Woody"
    bl_parentid = "OBJECT_PT_woodytool"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        selected_object = context.object
        mirror_modifier = None

        # 선택한 오브젝트의 Mirror 모디파이어
        for modifier in selected_object.modifiers:
            if modifier.type == 'MIRROR':
                mirror_modifier = modifier
                break

        # Mirror Modifier가 존재하는 경우에만 UI를 그립니다.
        if mirror_modifier:
            # Mirror Axis 축 변경 toggle 버튼
            layout.prop(mirror_modifier, "use_axis", toggle=True)
        else:
            layout.label(text="Mirror Modifier를 찾을 수 없습니다.")

# Cylinder Operator -----------------------------------------------------------------------------

class Add_Cylinder_6(Operator):
    bl_label = "6"
    bl_idname = "wm.add_cylinder_6"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.5, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1,1,1))
        return {'FINISHED'}

class Add_Cylinder_8(Operator):
    bl_label = "8"
    bl_idname = "wm.add_cylinder_8"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.5, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1,1,1))
        return {'FINISHED'}

class Add_Cylinder_10(Operator):
    bl_label = "10"
    bl_idname = "wm.add_cylinder_10"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.5, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1,1,1))
        return {'FINISHED'}

class Add_Cylinder_12(Operator):
    bl_label = "12"
    bl_idname = "wm.add_cylinder_12"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.5, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1,1,1))
        return {'FINISHED'}


# Add Material --------------------------------------------------------------------
    
class Add_Material(Operator):
    """선택한 오브젝트의 머티리얼을 오브젝트 이름으로 생성"""
    bl_label = "Material"
    bl_idname = "wm.add_material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        selObjs = bpy.context.selected_objects
        matList = bpy.data.materials

        # material_name 존재여부 체크 : True / False
        def check_material_exist(material_name):
            return material_name in bpy.data.materials

        for obj in selObjs:
            name = obj.name

            obj.data.materials.clear()

            # 존재 여부 체크 후 머티리얼 할당
            if check_material_exist(name):
                mat = bpy.data.materials[name]
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                bsdf.inputs[12].default_value = 0    # Specular = '0'
                obj.data.materials.append(mat)
            else: 
                mat = bpy.data.materials.new(name)
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                bsdf.inputs[12].default_value = 0    # Specular = '0'
                obj.data.materials.append(mat)

        return {'FINISHED'}

# Add Lattice --------------------------------------------------------------------

class Add_Lattice(Operator):
    """선택한 오브젝트를 기준으로 Lattice를 생성합니다."""
    bl_label = "Lattice"
    bl_idname = "wm.add_lattice"
    bl_options = {'REGISTER', 'UNDO'}

    lattice_resolution: bpy.props.IntProperty(name="Resolution", default=0, min=0, max=10)
    
    def execute(self, context):
        # Lattice Resolution --------------------------

        resolution = self.lattice_resolution

        # ---------------------------------------------

        selObj = bpy.context.selected_objects

        # Desellect All
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selObj:
            
            obj_loc = bpy.data.objects[obj.name].location
            
            # Create Lattice : select obj's location & Scale
            bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=obj_loc, scale=(1, 1, 1))
            curObj = bpy.context.selected_objects[0]
            curObj.name = obj.name + "_Lattice"
            latticeName = curObj.name
            curObj.data.name = latticeName
            size = obj.dimensions
            curObj.scale = (size[0] + 0.1, size[1] + 0.1, size[2] + 0.1)
            
            # Lattice Resolution
            latticeObj = bpy.context.selected_objects[0]
            latticeObj.data.points_u = 2 + resolution
            latticeObj.data.points_v = 2 + resolution
            latticeObj.data.points_w = 2 + resolution
            
            bpy.ops.object.select_all(action='DESELECT')
            
            # "Lattice" Modifier & Apply "Lattice" Object
            obj.select_set(True)
            selObj = bpy.context.selected_objects[0]
            selObj.modifiers.new(name='Lattice', type='LATTICE')
            selObj.modifiers["Lattice"].object = bpy.data.objects[latticeName]
            
            bpy.ops.object.select_all(action='DESELECT')
            
        return {'FINISHED'}


# Add Text Operator -----------------------------------------------------------------

class Add_Text(Operator):
    """Open the Text Tool Dialog Box"""
    bl_label = "Text"
    bl_idname = "wm.add_text"
    bl_options = {'REGISTER', 'UNDO'}
    
    text : bpy.props.StringProperty(name="Enter Text", default="")
    scale : bpy.props.FloatProperty(name= "Scale", default= 1)
    rotation : bpy.props.BoolProperty(name= "Z up", default= False)
    center : bpy.props.BoolProperty(name= "Center Origin", default= False)
    extrude : bpy.props.BoolProperty(name= "Extrude", default= False)
    extrude_amount : bpy.props.FloatProperty(name= "Extrude Amount", default= 0.06)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        
        layout = self.layout
        
        layout.prop(self, "text")
        layout.prop(self, "scale")
        
        layout.separator(factor= 1)
        
        box = layout.box()
        
        row = box.row()
        row.prop(self, "rotation")
        if self.rotation == True:
            row.label(text= "Orientation: Z up", icon= 'EMPTY_SINGLE_ARROW')
        elif self.rotation == False:
            row.label(text= "Orientation: Default", icon= 'ARROW_LEFTRIGHT')
            
        
        row = box.row()
        row.prop(self, "center")
        if self.center == True:
            row.label(text= "Align: Center", icon= 'ALIGN_CENTER')
        elif self.center == False:
            row.label(text= "Align: Left", icon= 'ALIGN_LEFT')
        
        row = box.row()
        row.prop(self, "extrude")
        if self.extrude == True:
            row.prop(self, "extrude_amount")
        
    def execute(self, context):
        
        text = self.text
        scale = self.scale
        center = self.center
        extrude = self.extrude
        extrude_amount = self.extrude_amount
        rotation = self.rotation
        
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text= text)
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.size = scale

        if rotation == True:
            bpy.context.object.rotation_euler[0] = 1.5708
                    
        if extrude == True:
            bpy.context.object.data.extrude = extrude_amount
        
        if center == True:
            bpy.context.object.data.align_x = 'CENTER'
            bpy.context.object.data.align_y = 'CENTER'


        return {'FINISHED'}


# Mirror 모디파이어
class Add_Mirror_X_Modifier(Operator):
    bl_idname = "wm.add_mirror_x_modifier"
    bl_label = "X"

    def execute(self, context):
        # 선택한 오브젝트 가져오기
        obj = bpy.context.object

        # Edit 모드로 전환
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # BMesh 생성
        bm = bmesh.from_edit_mesh(obj.data)

        # 0 < x < 0.01 사이의 vertex는 모두 0으로
        for vertex in bm.verts:
            if vertex.co.x > 0 and vertex.co.x < 0.01:
                vertex.co.x = 0

        # x > 0인 버텍스 모두 선택
        for vertex in bm.verts:
            # 버텍스의 좌표를 기반으로 선택 여부 판단
            if vertex.co.x > 0.0 :
                vertex.select = True
            else:
                vertex.select = False

        # 선택된 버텍스 제거
        bmesh.ops.delete(
            bm,
            geom=[v for v in bm.verts if v.select],
            context='VERTS'
        )

        # BMesh 데이터를 오브젝트에 적용
        bmesh.update_edit_mesh(obj.data)

        #Object 모드로 전환
        bpy.ops.object.mode_set(mode='OBJECT')

        # Mirror 모디파이어 추가
        mirror_modifier = obj.modifiers.new("Mirror", 'MIRROR')
        mirror_modifier.use_axis[0] = True
        mirror_modifier.use_axis[1] = False
        mirror_modifier.use_axis[2] = False

        return {'FINISHED'}
    
# Mirror 모디파이어
class Add_Mirror_Y_Modifier(Operator):
    bl_idname = "wm.add_mirror_y_modifier"
    bl_label = "Y"

    def execute(self, context):
        # 선택한 오브젝트 가져오기
        obj = bpy.context.object

        # Edit 모드로 전환
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # BMesh 생성
        bm = bmesh.from_edit_mesh(obj.data)

        # 0 < x < 0.01 사이의 vertex는 모두 0으로
        for vertex in bm.verts:
            if vertex.co.y > 0 and vertex.co.y < 0.01:
                vertex.co.y = 0

        # x > 0인 버텍스 모두 선택
        for vertex in bm.verts:
            # 버텍스의 좌표를 기반으로 선택 여부 판단
            if vertex.co.y > 0.0 :
                vertex.select = True
            else:
                vertex.select = False

        # 선택된 버텍스 제거
        bmesh.ops.delete(
            bm,
            geom=[v for v in bm.verts if v.select],
            context='VERTS'
        )

        # BMesh 데이터를 오브젝트에 적용
        bmesh.update_edit_mesh(obj.data)

        #Object 모드로 전환
        bpy.ops.object.mode_set(mode='OBJECT')

        # Mirror 모디파이어 추가
        mirror_modifier = obj.modifiers.new("Mirror", 'MIRROR')
        mirror_modifier.use_axis[0] = False
        mirror_modifier.use_axis[1] = True
        mirror_modifier.use_axis[2] = False

        return {'FINISHED'}

# Mirror 모디파이어
class Add_Mirror_Z_Modifier(Operator):
    bl_idname = "wm.add_mirror_z_modifier"
    bl_label = "Z"

    def execute(self, context):
        # 선택한 오브젝트 가져오기
        obj = bpy.context.object

        # Edit 모드로 전환
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # BMesh 생성
        bm = bmesh.from_edit_mesh(obj.data)

        # 0 < x < 0.01 사이의 vertex는 모두 0으로
        for vertex in bm.verts:
            if vertex.co.z > 0 and vertex.co.z < 0.01:
                vertex.co.z = 0

        # x > 0인 버텍스 모두 선택
        for vertex in bm.verts:
            # 버텍스의 좌표를 기반으로 선택 여부 판단
            if vertex.co.z > 0.0 :
                vertex.select = True
            else:
                vertex.select = False

        # 선택된 버텍스 제거
        bmesh.ops.delete(
            bm,
            geom=[v for v in bm.verts if v.select],
            context='VERTS'
        )

        # BMesh 데이터를 오브젝트에 적용
        bmesh.update_edit_mesh(obj.data)

        #Object 모드로 전환
        bpy.ops.object.mode_set(mode='OBJECT')

        # Mirror 모디파이어 추가
        mirror_modifier = obj.modifiers.new("Mirror", 'MIRROR')
        mirror_modifier.use_axis[0] = False
        mirror_modifier.use_axis[1] = False
        mirror_modifier.use_axis[2] = True

        return {'FINISHED'}


classes = [
    OBJECT_PT_WoodyTool,
    OBJECT_PT_Spacing,
    OBJECT_PT_Mirror_Modifier,
    Add_Cylinder_6,
    Add_Cylinder_8,
    Add_Cylinder_10,
    Add_Cylinder_12,
    Add_Material,
    Add_Lattice,
    Add_Mirror_X_Modifier,
    Add_Mirror_Y_Modifier,
    Add_Mirror_Z_Modifier,
    Add_Text
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()