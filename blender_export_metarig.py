"""Blender metarig landmark exporter for PROFILE Motion Engine.
Run from Blender Scripting with a selected armature. This script contains
original interoperability code; it does not import or redistribute Rigify code.
"""
import bpy
import json
from mathutils import Vector
from pathlib import Path

arm = bpy.context.active_object
if arm is None or arm.type != 'ARMATURE':
    raise RuntimeError('Select an armature object (e.g. Rigify metarig), then run.')
mesh_objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not mesh_objects:
    raise RuntimeError('Scene requires a mesh to establish proportional bounds.')
verts = []
for o in mesh_objects:
    verts.extend(arm.matrix_world.inverted() @ (o.matrix_world @ v.co) for v in o.data.vertices)
if not verts:
    raise RuntimeError('No mesh vertices')
mins = [min(v[i] for v in verts) for i in range(3)]
maxs = [max(v[i] for v in verts) for i in range(3)]
# Blender and glTF use Z-up vs Y-up conventions: (x,y,z)_Blender => (x,z,-y)_glTF.
def cv(v):
    return [float(v[0]),float(v[2]),float(-v[1])]
source = [{'name': b.name, 'parent': b.parent.name if b.parent else None, 'head': cv(b.head_local), 'tail': cv(b.tail_local)} for b in arm.data.bones]
# Convert all 8 corners to account for coordinate-system sign changes.
coords = [cv(Vector((x,y,z))) for x in (mins[0],maxs[0]) for y in (mins[1],maxs[1]) for z in (mins[2],maxs[2])]
bounds = {'min': [min(p[i] for p in coords) for i in range(3)], 'max':[max(p[i] for p in coords) for i in range(3)]}
out = {'format':'PROFILE-metarig-1','axis':'Y_UP','source':'Blender armature landmarks','bounds':bounds,'bones':source}
path = Path(bpy.path.abspath('//profile-metarig-guide.json'))
path.write_text(json.dumps(out,indent=2),encoding='utf-8')
print('Saved PROFILE guide:', path)
