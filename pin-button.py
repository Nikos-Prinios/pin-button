bl_info = {
    "name": "pin button",
    "author": "Nicolas Priniotakis (Nikos)",
    "version": (0,0,0,1),
    "blender": (2, 7, 4, 0),
    "api": 44539,
    "category": "3D View",
    "location": "3D View -> Header",
    "description": "Similar to Adobe Edge Animate's pin button",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",}


import bpy
from bpy.app.handlers import persistent

bpy.types.Scene.pin = bpy.props.BoolProperty(name="Pin",description="In the process of pinning",default = False)
global obj, pinned
pinned = False

def pos_marker(frame,marker):
    for k, m in bpy.context.screen.scene.timeline_markers.items():
        if m.name == marker:
            m.frame = frame
            return
@persistent
def update_marker(self):
    print('change')
    if bpy.context.scene.pin == True:
        frame = bpy.context.scene.frame_current
        pos_marker(frame,'unpin')

def marker_exist(name):
    for k, m in bpy.context.screen.scene.timeline_markers.items():
        if m.name == name: return True
    return False

def add_marker(name):
    if not marker_exist(name):
        original_type = bpy.context.area.type
        bpy.context.area.type = "TIMELINE" 
        bpy.ops.marker.add()
        bpy.ops.marker.rename(name=name)
        bpy.context.area.type = original_type

def is_pinned():
    for obj in bpy.context.scene.objects:
        try:
            if obj['pinned']:
                return True
        except: pass
    return False

def delete_markers():
    original_type = bpy.context.area.type
    bpy.context.area.type = "TIMELINE"
    for k, m in bpy.context.screen.scene.timeline_markers.items():
        if m.name == 'pin' or m.name == 'unpin' :
            m.select = True
        else: m.select = False
    bpy.ops.marker.delete()
    bpy.context.area.type = original_type

def pin(obj):
    frame = bpy.context.scene.frame_current
    obj['pinned'] = True
    obj['original_name'] = obj.name
    obj.name += ' (pinned)'
    obj.show_name = True
    obj.show_bounds = True
    obj.keyframe_insert(data_path = 'location', frame = frame)
    obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)
    obj.keyframe_insert(data_path = 'scale', frame = frame)
    add_marker("pin")
    bpy.context.scene.frame_current += 1
    add_marker("unpin")
    bpy.context.scene.pin = True

def unpin(obj):
    frame = bpy.context.scene.frame_current
    obj['pinned'] = False
    obj.show_bounds = False
    obj.name = obj['original_name']
    obj.show_name = False
    original_type = bpy.context.area.type
    bpy.context.area.type = "DOPESHEET_EDITOR"
    obj.keyframe_insert(data_path = 'location', frame = frame)
    obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)
    obj.keyframe_insert(data_path = 'scale', frame = frame)
    bpy.context.area.type = original_type
    bpy.context.scene.pin = False

def main(context):
    if is_pinned():
        for obj in bpy.context.selected_objects:
            try : 
                if obj['pinned'] == True : unpin(obj)
            except : pass
    else :
        for obj in bpy.context.selected_objects:
            pin(obj)
            

    if not is_pinned() :
        original_type = bpy.context.area.type
        bpy.context.area.type = "DOPESHEET_EDITOR"      
        bpy.ops.action.clean()
        bpy.context.area.type = original_type
        delete_markers()

class pin_it_operator(bpy.types.Operator):
    bl_idname = "object.pin"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode =='OBJECT'

    def execute(self, context):
        main(context)
        return {'FINISHED'}

class PinPanel(bpy.types.Header):
    bl_label = "Pin Panel"
    bl_idname = "OBJECT_PT_PIN"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
            
    def draw(self, context):
        icn = "UNPINNED"
        obj = context.active_object
        try:
            if obj['pinned'] == True :
                icn = "PINNED"
            else: icn = "UNPINNED"
        except: icn = "UNPINNED"
        layout = self.layout
        row=layout.row()
        layout.separator()
        row.operator("object.pin", icon=icn)

def register():
    bpy.app.handlers.frame_change_pre.append(update_marker)
    bpy.utils.register_class(PinPanel)
    bpy.utils.register_class(pin_it_operator)
    

def unregister():
    bpy.app.handlers.frame_change_pre.remove(update_marker)
    bpy.utils.unregister_class(PinPanel)
    bpy.utils.unregister_class(pin_it_operator)
    

if __name__ == "__main__":
    register()
