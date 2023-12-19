import bpy

# 데이터 기록
def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("Test : %s" % use_some_setting)
    f.close()

    return {'FINISHED'}

# ExportHelper는 helper 클래스로서 파일 이름을 정의하고 파일 선택기를 호출
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export.some_data"  # important since its how bpy.ops.import.some_data is constructed
    bl_label = "Export Data"

    # ExportHelper mix-in class uses this.
    filename_ext = ".txt"

    # 파일 선택기로부터 받을 파일명
    filter_glob: StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # TXT파일에 입력될 정보
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# 동적 메뉴를 추가하고자 할때만 필요 : 파일 선택기에서 Export Data 버튼
def menu_func_export(self, context):
    self.layout.operator(ExportData.bl_idname, text="Text Export Operator")


def register():
    bpy.utils.register_class(ExportData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export.some_data('INVOKE_DEFAULT')
