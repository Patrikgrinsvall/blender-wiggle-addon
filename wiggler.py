import bpy
import random

bl_info = {
    "name": "Wiggle",
    "author": "William Landgren",
    "version": (1, 2),
    "blender": (3, 0, 0),
}

################################
# Helpers
################################
def has_keyframe(ob, attr):
    anim = ob.animation_data
    if anim is not None and anim.action is not None:
        for fcu in anim.action.fcurves:  
            if fcu.data_path == attr:
                return len(fcu.keyframe_points) > 0
    return False 

def find_modifier(fcu, type):   
    for modifier in fcu.modifiers:  
        if modifier.type == type:
            return modifier
    return None

def wiggle(ob, context):
    scene = context.scene
    mytool = scene.wiggler_addon
    if has_keyframe(ob, "rotation_euler") == False:
        ob.keyframe_insert("rotation_euler") 

    action = ob.animation_data.action

    for fcu in action.fcurves:
        if fcu.data_path == "rotation_euler":
            random_num_sc = random.uniform(0.01, 1)
            random_num_st = random.uniform(25, 60)
            random_num_ph = random.uniform(1000, 2000 )
            mod = find_modifier(fcu, "NOISE")
            if mod == None: 
                mod = fcu.modifiers.new("NOISE")
            mod.scale = scene.wiggler_addon.speed_vector
            mod.strength = scene.wiggler_addon.strength_vector
            mod.phase = scene.wiggler_addon.rand_vector + random_num_ph
            mod.use_influence = True
            mod.influence = scene.wiggler_addon.influence_vector
    bpy.ops.transform.rotate(value = 0)

def wiggle_selected_objects(context):
    for ob in context.selected_objects:
        wiggle(ob, context)
        
def update_when_changed(self, context):
    wiggle_selected_objects(context)

################################
# Classes
################################
class Wiggler_properties(bpy.types.PropertyGroup):
    speed_vector : bpy.props.FloatProperty(name= "Speed", update=update_when_changed, soft_min= 0, soft_max= 1000, default= 50)
    strength_vector : bpy.props.FloatProperty(name= "Strength ", update=update_when_changed, soft_min= 0, soft_max= 1000, default= 0.2)
    rand_vector : bpy.props.FloatProperty(name= "Randomize", update=update_when_changed, soft_min= -1000, soft_max= 1000, default= 1)
    influence_vector : bpy.props.FloatProperty(name= "Influence", update=update_when_changed, subtype= "FACTOR", soft_min= 0, soft_max= 1, default= 1.0)
 
################################
class Wiggler_panel(bpy.types.Panel):
    bl_label = "Wiggle"
    bl_idname = "Wiggler_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator("wiggler_addon.wiggler_operator")
        layout.prop(scene.wiggler_addon, "speed_vector")
        layout.prop(scene.wiggler_addon, "strength_vector")
        layout.prop(scene.wiggler_addon, "rand_vector")
        layout.prop(scene.wiggler_addon, "influence_vector")

################################
class Wiggler_operator(bpy.types.Operator):
    bl_label = "Wiggle it!"
    bl_idname = "wiggler_addon.wiggler_operator"

    def execute(self, context):    
        wiggle_selected_objects(context)
        return {'FINISHED'}

################################
# Main entrypoint
################################
classes = [Wiggler_properties, Wiggler_panel, Wiggler_operator]
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.wiggler_addon = bpy.props.PointerProperty(type=Wiggler_properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        try:
            del bpy.types.Scene.wiggler_addon
        except:
            print("Got exception when trying to unregister")

 
 
if __name__ == "__main__":
    register()
