import bpy, math, os
from mathutils import Quaternion, Vector
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(__file__), 'portrait_character.blend'))
rig=bpy.data.objects['CharacterRig']
rig.animation_data_clear()
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
def pose(name, axis, angle):
 p=rig.pose.bones[name];p.rotation_mode='QUATERNION'
 q=p.bone.matrix_local.to_quaternion()
 p.rotation_quaternion=q.inverted() @ Quaternion(Vector(axis),angle) @ q
def key(f):
 for p in rig.pose.bones:
  p.keyframe_insert('rotation_quaternion',frame=f)
  p.keyframe_insert('location',frame=f)
for name,frames in [('idle',61),('walk',25),('jump',25)]:
 rig.animation_data_create();rig.animation_data.action=bpy.data.actions.new(name)
 for f in range(1,frames+1,3):
  t=(f-1)/(frames-1)*math.tau
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.rotation_quaternion=(1,0,0,0);p.location=(0,0,0)
  for s,side in [(1,'Left'),(-1,'Right')]:
   pose(side+'Arm',(0,1,0),s*(1.35 if name!='jump' else .8))
   if name=='walk':
    pose(side+'UpLeg',(1,0,0),s*.55*math.sin(t))
    pose(side+'Leg',(1,0,0),max(0,-s*math.sin(t))*.6)
    # Small shoulder swing after lowering the arms.
    p=rig.pose.bones[side+'Arm'];q=p.bone.matrix_local.to_quaternion();p.rotation_quaternion=(q.inverted() @ Quaternion(Vector((1,0,0)),-s*.3*math.sin(t)) @ q) @ p.rotation_quaternion
   elif name=='jump':
    pose(side+'UpLeg',(1,0,0),-.3);pose(side+'Leg',(1,0,0),.6)
  if name=='idle':pose('Spine2',(1,0,0),.018*math.sin(t))
  key(f)
 for fc in rig.animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
rig.animation_data.action=bpy.data.actions.get('idle');bpy.context.scene.frame_set(1)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(os.path.dirname(__file__), '..', 'models', 'portrait_character.glb'),use_selection=True,export_animations=True,export_animation_mode='ACTIONS')
