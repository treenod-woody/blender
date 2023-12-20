import bpy
import os
import math

listName = []
listVal = []
cntObj = len(bpy.data.objects)
data = ''

# (블렌더파일명)_Rotation.txt
save_path = bpy.data.filepath.replace('.blend', '_Rotation.txt')

for obj in bpy.data.objects:
    listName.append(obj.name)
    rotation = obj.rotation_euler
    x = int(math.degrees(rotation.x))
    y = int(math.degrees(rotation.y))
    z = int(math.degrees(rotation.z))
    listVal.append((x,y,z))

for i in range(1, cntObj + 1):
    data += f'{listName[i-1]},{listVal[i-1]},\n'
    
if __name__ == "__main__":
    f = open(save_path, 'w')
    f.write(data)
    f.close()