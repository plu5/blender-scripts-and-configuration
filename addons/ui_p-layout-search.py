bl_info = {
    "name": "p/layout-search",
    "author": "+-",
    "version": (1, 2),
    "blender": (2, 78, 0),
    "description": "Search popup for switching between layouts.",
	"location": "Bind `wm.layout_search', preferably under Screen > Screen (Global)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"}

import bpy

def get_layouts(self, context):
    l = []
    for i, screenlayout in enumerate(bpy.data.screens):
        l.append((screenlayout.name, screenlayout.name, str(i)))
    return l

class LayoutSearch(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "wm.layout_search"
	bl_label = "Layout Search"
	bl_property = "layouts_enum"
	layouts_enum = bpy.props.EnumProperty(items=get_layouts)

	def execute(self, context):
            self.report({'INFO'}, "Screen layout: %s" % self.layouts_enum)
            bpy.context.window.screen = bpy.data.screens[self.layouts_enum]
            return {'FINISHED'}

	def invoke(self, context, event):
            wm = context.window_manager
            wm.invoke_search_popup(self)
            return {'FINISHED'}

def register():
	bpy.utils.register_class(LayoutSearch)

def unregister():
	bpy.utils.unregister_class(LayoutSearch)

if __name__ == "__main__":
	register()
