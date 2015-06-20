bl_info = {
    "name": "pin-button",
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

def main(context):
    clean = False
    frame = bpy.context.scene.frame_current
    for obj in bpy.context.selected_objects:
        try:
            if obj['pinned'] == True:
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
                clean = True
            else:
                obj['pinned'] = True
                obj['original_name'] = obj.name
                obj.name += ' (pinned)'
                obj.show_name = True
                obj.show_bounds = True
                obj.keyframe_insert(data_path = 'location', frame = frame)
                obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)
                obj.keyframe_insert(data_path = 'scale', frame = frame)
        except:
            obj['pinned'] = True
            obj['original_name'] = obj.name
            obj.name += ' (pinned)'
            obj.show_name = True
            obj.show_bounds = True
            obj.keyframe_insert(data_path = 'location', frame = frame)
            obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)
            obj.keyframe_insert(data_path = 'scale', frame = frame)
    if clean :
        original_type = bpy.context.area.type
        bpy.context.area.type = "DOPESHEET_EDITOR"      
        bpy.ops.action.clean()
        bpy.context.area.type = original_type

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
    bpy.utils.register_class(PinPanel)
    bpy.utils.register_class(pin_it_operator)

def unregister():
    bpy.utils.unregister_class(PinPanel)
    bpy.utils.unregister_class(pin_it_operator)

if __name__ == "__main__":
    register()
