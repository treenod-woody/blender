import bpy
from bpy.types import Operator, Panel

palette_name = "RGB Palette"

for palette in bpy.data.palettes:
    if palette.name == palette_name:
        bpy.data.palettes.remove(palette)

# 신규 팔레트 생성 및 컬러 등록
palette = bpy.data.palettes.new(palette_name)
palette.colors.new().color = (1.0, 0.0, 0.0) # R
palette.colors.new().color = (0.0, 1.0, 0.0) # G
palette.colors.new().color = (0.0, 0.0, 1.0) # B
palette.colors.new().color = (0.0, 0.0, 0.0) # Black
palette.colors.new().color = (1.0, 1.0, 1.0) # White

# 객체의 모드를 'VERTEX_PAINT'로 변경합니다.
bpy.ops.object.mode_set(mode='VERTEX_PAINT')
