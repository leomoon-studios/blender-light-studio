import bpy
import os
from . common import getLightMesh
from . auto_load import force_register

@force_register
class LLS_PT_Studio(bpy.types.Panel):
    bl_idname = "LLS_PT_studio"
    bl_label = "Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        if not context.scene.LLStudio.initialized: col.operator('scene.create_leomoon_light_studio')
        if context.scene.LLStudio.initialized: col.operator('scene.delete_leomoon_light_studio')
        col.separator()
        col.operator('light_studio.control_panel', icon='MENU_PANEL')
        col.operator('scene.set_light_studio_background')

@force_register
class LLS_PT_Lights(bpy.types.Panel):
    bl_idname = "LLS_PT_lights"
    bl_label = "Lights"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and len(context.scene.LLStudio.profile_list)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        
        props = context.scene.LLStudio

        row = layout.row()
        col = row.column()
        col.template_list("LLS_UL_LightList", "Light_List", props, "light_list", props, "light_list_index", rows=5)

        col = row.column(align=True)
        col.operator('scene.add_leomoon_studio_light', icon='PLUS', text="")
        col.operator('scene.delete_leomoon_studio_light', icon='TRASH', text="")


@force_register
class LLS_PT_Selected(bpy.types.Panel):
    bl_idname = "LLS_PT_selected"
    bl_label = "Selected Light"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'

    def draw(self, context):
        if context.active_object and (context.active_object.name.startswith('LLS_CONTROLLER') or context.active_object.name.startswith('LLS_LIGHT_MESH')):
            layout = self.layout
            wm = context.window_manager

            col = layout.column(align=True)
            col.operator('lls.light_brush', text="3D Edit", icon='PIVOT_CURSOR')

            box = layout.box()
            col = box.column()
            col.template_icon_view(wm, "lls_tex_previews", show_labels=True)
            col.label(text=os.path.splitext(wm.lls_tex_previews)[0])

            layout.separator()
            try:
                lls_inputs = getLightMesh().active_material.node_tree.nodes["Group"].inputs
                for input in lls_inputs[2:]:
                    if input.type == "RGBA":
                        layout.prop(input, 'default_value', text=input.name)
                        col = layout.column(align=True)
                    else:
                        col.prop(input, 'default_value', text=input.name)
            except:
                col.label(text="LLS_light material is not valid.")
                #import traceback
                #traceback.print_exc()
            col.prop(getLightMesh(), 'location', index=0) #light radius

@force_register
class LLS_PT_ProfileList(bpy.types.Panel):
    bl_idname = "LLS_PT_profile_list"
    bl_label = "Profiles"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.LLStudio.initialized

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        props = scene.LLStudio

        row = layout.row()
        col = row.column()
        col.template_list("UI_UL_list", "Profile_List", props, "profile_list", props, "list_index", rows=5)

        col = row.column(align=True)
        col.operator('lls_list.new_profile', icon='PLUS', text="")
        col.operator('lls_list.delete_profile', icon='TRASH', text="")
        col.operator('lls_list.copy_profile_menu', icon='DUPLICATE', text="")

        col.separator()
        col.operator('lls_list.move_profile', text='', icon="TRIA_UP").direction = 'UP'
        col.operator('lls_list.move_profile', text='', icon="TRIA_DOWN").direction = 'DOWN'

@force_register
class LLS_PT_ProfileImportExport(bpy.types.Panel):
    bl_idname = "LLS_PT_profile_import_export"
    bl_label = "Import/Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.LLStudio.initialized

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.operator('lls_list.export_profiles', text="Export Selected Profile")
        col.operator('lls_list.export_profiles', text="Export All Profiles").all=True
        col.operator('lls_list.import_profiles')

from . import bl_info
@force_register
class LLS_PT_Misc(bpy.types.Panel):
    bl_idname = "LLS_PT_misc"
    bl_label = "Misc"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' #and context.scene.LLStudio.initialized

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        props = scene.LLStudio

        col = layout.column(align=True)
        col.operator('lls.find_missing_textures')
        col.operator('lls.open_textures_folder')
        col.operator('lls.lls_keyingset')
        if context.scene.keying_sets.active and context.scene.keying_sets.active.bl_idname == "BUILTIN_KSI_LightStudio":
            box = col.box()
            box.label(text="Keying Set is active")

class LLSKeyingSet(bpy.types.Operator):
    bl_idname = "lls.lls_keyingset"
    bl_description = "Activate LightStudio Keying Set to animate lights"
    bl_label = "LightStudio Keying Set"
    bl_options = {"INTERNAL", "UNDO"}
    @classmethod
    def poll(self, context):
        """ Enable if there's something in the list """
        return len(context.scene.LLStudio.profile_list)

    def execute(self, context):
        context.scene.keying_sets.active = [k for k in context.scene.keying_sets_all if k.bl_idname == "BUILTIN_KSI_LightStudio"][0]
        return {"FINISHED"}

@force_register
class LLS_PT_Hotkeys(bpy.types.Panel):
    bl_idname = "LLS_PT_hotkeys"
    bl_label = "Hotkeys"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LightStudio"
    #bl_options = {'DEFAULT_CLOSED'}

    #@classmethod
    #def poll(cls, context):
    #    return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' #and context.scene.LLStudio.initialized

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        props = scene.LLStudio

        box = layout.box()

        box.label(text="Move light", icon='MOUSE_LMB')
        row = box.row(align=True)

        row.label(text="Scale light", icon='EVENT_S')
        row = box.row(align=True)

        row.label(text="Rotate light", icon='EVENT_R')
        row = box.row(align=True)

        row.label(text="Precision mode", icon='EVENT_SHIFT')
        row = box.row(align=True)

        box.label(text="Mute light", icon='MOUSE_LMB_DRAG')

        box.label(text="Isolate light", icon='MOUSE_RMB')
        row = box.row(align=True)

        row.label(text="", icon='EVENT_CTRL')
        row.label(text="Loop overlapping lights", icon='MOUSE_LMB')
        row = box.row(align=True)

        box.label(text="(numpad) Icon scale up", icon='ADD')

        box.label(text="(numpad) Icon scale down", icon='REMOVE')
