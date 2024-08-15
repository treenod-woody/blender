from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, FloatVectorProperty, EnumProperty
import bpy

class MyProperties(PropertyGroup):

    my_string : StringProperty(name="Enter Text") # type: ignore
    my_float_vector : FloatVectorProperty(name="Location", default=(1,1,1)) # type: ignore
    my_enum : EnumProperty(
        name="Enumerator / Dropdown",
        description="sample text",
        items=[('OP1', "Add Cube", ""),
               ('OP2', "Add Sphere", ""),
               ('OP3', "Add Suzanne", "")],
        default='OP1'
    ) # type: ignore