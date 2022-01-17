bl_info = {
    "name": "Mirror Separate",
    "author": "Takeshi Chō",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Edit Tab / Edit Mode Context Menu",
    "warning": "",
    "description": "separate mesh and set origin mirroredly",
    "doc_url": "",
    "category": "Mesh",
}

import bpy
from bpy.types import (Operator,Menu)

# ---------- Main function ---------- 

class Channel():
    x = 0
    y = 1
    z = 2

def Mirror_Separate(channel):

    cursor = bpy.context.scene.cursor
    cursor_original_location = cursor.location.xyz


    obj = bpy.context.selected_objects[0]
    obj_original_location = obj.location.xyz
    obj_name = obj.name_full

    bpy.ops.object.editmode_toggle()

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    obj_median_loction = obj.location.xyz

    obj_target_location = obj_original_location.xyz
    obj_target_location[channel] += ((obj_median_loction[channel]- obj_original_location[channel])*2)

    cursor.location = obj_target_location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.editmode_toggle()

    #separated_obj_name = bpy.context.selected_objects[1].name_full

    cursor.location = obj_original_location.xyz
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=obj_name)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    #bpy.ops.object.select_pattern(pattern=separated_obj_name)

    cursor.location = cursor_original_location.xyz
    bpy.ops.object.editmode_toggle()

# ---------- Operator ---------- 

class Separate_Along_X(Operator):
    """separate mesh mirroredly along X"""
    bl_idname = "mesh.separate_along_x"
    bl_label = "Separate Along X"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        Mirror_Separate(Channel.x)
        return {'FINISHED'}

class Separate_Along_Y(Operator):
    """separate mesh mirroredly along Y"""
    bl_idname = "mesh.separate_along_y"
    bl_label = "Separate Along Y"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        Mirror_Separate(Channel.y)
        return {'FINISHED'}

class Separate_Along_Z(Operator):
    """separate mesh mirroredly along Z"""
    bl_idname = "mesh.separate_along_z"
    bl_label = "Separate Along Z"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        Mirror_Separate(Channel.z)
        return {'FINISHED'}    

# ---------- GUI and registration ---------- 

class VIEW3D_MT_edit_mesh_Mirror_Separate(Menu):
    bl_label = "Mirror Separate"

    def draw(self, context):
        layout = self.layout
        layout.operator(Separate_Along_X.bl_idname, text=Separate_Along_X.bl_label)
        layout.operator(Separate_Along_Y.bl_idname, text=Separate_Along_Y.bl_label)
        layout.operator(Separate_Along_Z.bl_idname, text=Separate_Along_Z.bl_label)
        
    
def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_Mirror_Separate")
    self.layout.separator()
    
classes = (
    VIEW3D_MT_edit_mesh_Mirror_Separate,
    Separate_Along_X,
    Separate_Along_Y,
    Separate_Along_Z,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(menu_func)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()