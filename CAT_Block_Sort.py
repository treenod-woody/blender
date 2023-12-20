import bpy

xPos, yPos, zPos = 0.5, 0.5, 0.5
column = 0

objs = bpy.context.selected_objects
objs.sort(key = lambda o: o.name)

for obj in objs:
    obj.location = (xPos, yPos, zPos)
    if xPos < (column - 1):
        xPos += 1.0
    elif xPos > (column - 1):
        xPos = 0.5
        yPos -= 1.0
        zPos -= 1.0