import bpy
import bmesh

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

# Object 모드로 전환
bpy.ops.object.mode_set(mode='OBJECT')

# 모디파이어 리스트
modifiers = obj.modifiers

for modifier in modifiers:
    if modifier.type == 'MIRROR':
        modifiers.remove(modifier)

# Mirror 모디파이어 추가
mirror_modifier = obj.modifiers.new("Mirror", 'MIRROR')
mirror_modifier.use_axis[0] = True
mirror_modifier.use_axis[1] = False
mirror_modifier.use_axis[2] = False