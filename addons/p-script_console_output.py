bl_info = {
    "name": "script-console-output",
    "author": "+-",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "description": "Run script from text editor and display the output in console present in the layout. Some of the logic was taken from CoDEmanX addon Run Script in PyConsole.",
    "location": "Bind `text.script_console_output', preferrably under Text > Text Generic",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"}

import bpy
                
def main(self, context, text):
    text = bpy.data.texts.get(text.name)
    if text is not None:
        text = "exec(compile(" + repr(text) + ".as_string(), '" + \
                                    text.name + "', 'exec'))"
        for area in context.screen.areas:
            if area.type == 'CONSOLE':
                override = bpy.context.copy()
                override['area'] = area
                space_data = area.spaces.active
                # the proper way that should work but doesnt:
#                bpy.ops.console.clear_line(override)
#                bpy.ops.console.insert(override, text=text)
#                bpy.ops.console.execute(override)  # error
                
                # so instead:
                # switch to console and run our script
                old_type = bpy.context.area.type
                bpy.context.area.type = 'CONSOLE'
                bpy.ops.console.clear()
                bpy.ops.console.insert(text=text)
                bpy.ops.console.execute()
                # copy the output
                scrollback = bpy.context.area.spaces.active.scrollback
                # switch back
                bpy.context.area.type = old_type
                # paste the output where we want it
                for line in scrollback:
                    bpy.ops.console.scrollback_append(override, 
                                                      text=line.body,   
                                                      type=line.type)
                break

class CONSOLE_OT_script_console_output(bpy.types.Operator):
    """Run a text datablock in PyConsole"""
    bl_idname = "text.script_console_output"
    bl_label = "Run script in pyconsole"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'TEXT_EDITOR'

    def execute(self, context):
        text = context.space_data.text
        main(self, context, text)
        return {'FINISHED'}
    
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
