bl_info = {
    "name": "editor-switch-buffer",
    "author": "+-",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "description": "Search popup for switching between open files in the text editor. Some of the logic was taken from CoDEmanX addon Run Script in PyConsole.",
    "location": "Bind `wm.editor_switch_buffer', preferrably under Text > Text Generic",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"}

import bpy

def get_visible(context):
    l = []
    for area in context.screen.areas:
        if area.type == 'TEXT_EDITOR':
            text = area.spaces[0].text
            if text is not None and text not in l:
                l.append(text)
    return [t.name for t in l]

def get_buffer_enum(self, context):
    l = []
    visible = get_visible(context)
    for i, text in enumerate(bpy.data.texts):
        if text.name in visible:
            l.append((text.name, text.name + " (visible)", str(i)))
        else:
            l.append((text.name, text.name, str(i)))
    return l

class EditorSwitchBuffer(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "wm.editor_switch_buffer"
	bl_label = "Editor switch buffer"
	bl_property = "buffers_enum"
	buffers_enum = bpy.props.EnumProperty(items=get_buffer_enum)

	@classmethod
	def poll(cls, context):
		return context.area.type == 'TEXT_EDITOR'

	def execute(self, context):
            context.space_data.text = bpy.data.texts[self.buffers_enum]
            return {'FINISHED'}

	def invoke(self, context, event):
            wm = context.window_manager
            wm.invoke_search_popup(self)
            return {'FINISHED'}

def register():
	bpy.utils.register_class(EditorSwitchBuffer)

def unregister():
	bpy.utils.unregister_class(EditorSwitchBuffer)

if __name__ == "__main__":
	register()
