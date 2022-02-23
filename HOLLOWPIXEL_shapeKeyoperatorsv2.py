bl_info = {
    "name": "HOLLOWPIXEL SHAPEKEY OPERATORS",
    "author": "Chris mcfall based onwork by Ott, Jan, Eduardo Teixeira, sambler",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "description": "Adds operators: 'Zero all shapekeys','add52facialshapekeys', 'XYZ Shapekeys', 'Split Shapekeys', 'Apply Modifiers and Keep Shapekeys' and 'Apply Selected Shapekey as Basis'",
    "warning": "",
    "wiki_url": "https://blenderartists.org/t/addon-shapekey-helpers/1131849",
    "category": "'Mesh",
}

import bpy
from inspect import currentframe, getframeinfo


#__________________________________________________________________________
#__________________________________________________________________________


def SetActiveShapeKey (name):
    bpy.context.object.active_shape_key_index = bpy.context.object.data.shape_keys.key_blocks.keys().index(name)
    
#__________________________________________________________________________
#__________________________________________________________________________

O = bpy.ops
#__________________________________________________________________________
#__________________________________________________________________________

class ANIM_OT_add52facialkeys(bpy.types.Operator):
    """Creates 52 named but blank shapekeys ready for facial mocap systems"""
    bl_idname = "anim.add52facialkeys"
    bl_label = "add52facialkeys"
    
    def execute(self, context):
        keynames = [
        "browInnerUp",
        "browDown_L",
        "browDown_R",
        "browOuterUp_L",
        "browOuterUp_R",
        "eyeLookUp_L",
        "eyeLookUp_R",
        "eyeLookDown_L",
        "eyeLookDown_R",
        "eyeLookIn_L",
        "eyeLookIn_R",
        "eyeLookOut_L",
        "eyeLookOut_R",
        "eyeBlink_L",
        "eyeBlink_R",
        "eyeSquint_L",
        "eyeSquint_R",
        "eyeWide_L",
        "eyeWide_R",
        "cheekPuff",
        "cheekSquint_L",
        "cheekSquint_R",
        "noseSneer_L",
        "noseSneer_R",
        "jawOpen",
        "jawForward",
        "jawLeft",
        "jawRight",
        "mouthFunnel",
        "mouthPucker",
        "mouthLeft",
        "mouthRight",
        "mouthRollUpper",
        "mouthRollLower",
        "mouthShrugUpper",
        "mouthShrugLower",
        "mouthClose",
        "mouthSmile_L",
        "mouthSmile_R",
        "mouthFrown_L",
        "mouthFrown_R",
        "mouthDimple_L",
        "mouthDimple_R",
        "mouthUpperUp_L",
        "mouthUpperUp_R",
        "mouthLowerDown_L",
        "mouthLowerDown_R",
        "mouthPress_L",
        "mouthPress_R",
        "mouthStretch_L",
        "mouthStretch_R",
        "tongueOut",
            ]

        shape_keys = bpy.context.object.data.shape_keys.key_blocks
        for n in keynames:
            bpy.ops.object.shape_key_add(from_mix=False)
            shape_keys[-1].name = n
            
        self.report({'INFO'},"52 KEYS ADDED!")
        
        return{'FINISHED'}
    
class ANIM_OT_shapekeyxyz(bpy.types.Operator):
    """Creates 3 shapekeys based on selected shapekey but splits into X,Y and Z"""
    bl_idname = "anim.shapekeyxyz"
    bl_label = "shapeKeyXYZ"
    
    
    
    @classmethod
    def poll(cls, context):
            return context.active_object.active_shape_key is not None
    
    def execute(self, context):
        context = bpy.context
        scene = context.scene
        obj = context.object
        shape_name = obj.active_shape_key.name

        ## enable shapekey before copying
        skey_value = obj.active_shape_key.value
        obj.active_shape_key.value = obj.active_shape_key.slider_max

        obj.shape_key_add(name=str(shape_name) + "_X", from_mix=True)
        xshape_idx = len(obj.data.shape_keys.key_blocks)-1
        obj.shape_key_add(name=str(shape_name) + "_Y", from_mix=True)
        yshape_idx = len(obj.data.shape_keys.key_blocks)-1
        obj.shape_key_add(name=str(shape_name) + "_Z", from_mix=True)
        zshape_idx = len(obj.data.shape_keys.key_blocks)-1

        ## reset shapekey
        obj.active_shape_key.value = skey_value
        

        for vert in obj.data.vertices: #Isolate the translation on the X axis
            obj.data.shape_keys.key_blocks[xshape_idx].data[vert.index].co.y = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.y
            obj.data.shape_keys.key_blocks[xshape_idx].data[vert.index].co.z = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.z
                
        for vert in obj.data.vertices: #Isolate the translation on the Y axis
            obj.data.shape_keys.key_blocks[yshape_idx].data[vert.index].co.x = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.x
            obj.data.shape_keys.key_blocks[yshape_idx].data[vert.index].co.z = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.z
        
        for vert in obj.data.vertices: #Isolate the translation on the Z axis
            obj.data.shape_keys.key_blocks[zshape_idx].data[vert.index].co.x = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.x
            obj.data.shape_keys.key_blocks[zshape_idx].data[vert.index].co.y = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.y
        ##have to run z twice to fix bug
        for vert in obj.data.vertices: #Isolate the translation on the Z axis
            obj.data.shape_keys.key_blocks[zshape_idx].data[vert.index].co.x = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.x
            obj.data.shape_keys.key_blocks[zshape_idx].data[vert.index].co.y = obj.data.shape_keys.key_blocks['Basis'].data[vert.index].co.y
                
            self.report({'INFO'},"XYZ KEYS ADDED!")
                
            return{'FINISHED'}
#__________________________________________________________________________
#__________________________________________________________________________
class ShapeKeySplitter(bpy.types.Operator):
    """Creates a new object with the shapekeys split based on two vertex groups, named 'left' and 'right', that you must create manually"""
    bl_idname = "object.shape_key_splitter"
    bl_label = "Split Shapekeys"

    def execute(self, context):
        
        O.object.select_all(action='DESELECT')
        bpy.context.active_object.select_set(True)
        #____________________________
        #Generate copy of object
        #____________________________
        originalName = bpy.context.object.name
        O.object.duplicate_move()
        bpy.context.object.name = originalName + "_SplitShapeKeys"


        listOfKeys = []

        index = 0

        #__________________________________________________

        for s_key in bpy.context.object.data.shape_keys.key_blocks:
            
            if(index == 0):
                index = index + 1
                continue 
            
            if s_key.name.endswith('.L') or s_key.name.endswith('.R') or s_key.name.endswith('.B'):
                continue
            
            
            listOfKeys.append(s_key.name)

        #__________________________________________________

        for name in listOfKeys:
            
            SetActiveShapeKey(name)
            
            savedName = name
            savedShapeKey = bpy.context.object.active_shape_key
            
            
            #Create left version
            
            O.object.shape_key_clear()
            
            SetActiveShapeKey(savedName)
            savedShapeKey.vertex_group = 'left'
            savedShapeKey.value = 1.0
            
            O.object.shape_key_add(from_mix=True)
            bpy.context.object.active_shape_key.name = savedName + ".L"

            
            #Create right version
            
            O.object.shape_key_clear()
            
            SetActiveShapeKey(savedName)
            savedShapeKey.vertex_group = 'right'
            savedShapeKey.value = 1.0
            
            O.object.shape_key_add(from_mix=True)
            bpy.context.object.active_shape_key.name = savedName + ".R"
            
            
        for name in listOfKeys:
            
            #Set index to target shapekey
            SetActiveShapeKey(name)
            #Remove
            O.object.shape_key_remove(all=False)
                
        self.report({'INFO'},"SPLIT DONE.")        
        return {'FINISHED'}
    

class ShapeKeyPreserver(bpy.types.Operator):
    """Creates a new object with all modifiers applied and all shape keys preserved"""
    """NOTE: Blender can only combine objects with a matching number of vertices. """ 
    """As a result, you need to make sure that your shape keys don't change the number of vertices of the mesh. """
    """Modifiers like 'Subdivision Surface' can always be applied without any problems, other modifiers like 'Bevel' or 'Edgesplit' may not."""

    bl_idname = "object.shape_key_preserver"
    bl_label = "Apply Modifiers and Keep Shapekeys"
    
    def execute(self, context):
    
        oldName = bpy.context.active_object.name
        
        #Change context to 'VIEW_3D' and store old context
        oldContext = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'

        #selection setup
        originalObject = bpy.context.active_object

        originalObject.select_set(True)

        listOfShapeInstances = []
        listOfShapeKeyValues = []

        #_______________________________________________________________

        #Deactivate any armature modifiers
        for mod in originalObject.modifiers:
            if mod.type == 'ARMATURE':
                originalObject.modifiers[mod.name].show_viewport = False

        index = 0
        for shapekey in originalObject.data.shape_keys.key_blocks:
            if(index == 0):
                index = index + 1
                continue
            listOfShapeKeyValues.append(shapekey.value)

        index = 0
        for shapekey in originalObject.data.shape_keys.key_blocks:
            
            if(index == 0):
                index = index + 1
                continue
            
            bpy.ops.object.select_all(action='DESELECT')
            originalObject.select_set(True)

            bpy.context.view_layer.objects.active = originalObject
            
            bpy.ops.object.shape_key_clear()
            
            shapekey.value = 1.0
            
            #save name
            #____________________________
            shapekeyname = shapekey.name
            
            #create new object from shapekey and add it to list
            #____________________________
            bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
            bpy.ops.object.convert(target='MESH')
            listOfShapeInstances.append(bpy.context.active_object)
            
            #rename new object
            #____________________________
            bpy.context.object.name = shapekeyname
            
            bpy.ops.object.select_all(action='DESELECT')
            originalObject.select_set(True)

            bpy.context.view_layer.objects.active = originalObject

        #_____________________________________________________________
        #Prepare final empty container model for all those shape keys:
        #_____________________________________________________________
        
        bpy.context.view_layer.objects.active = originalObject
        bpy.ops.object.shape_key_clear()

        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        newObject = bpy.context.active_object

        bpy.ops.object.shape_key_clear()
        bpy.ops.object.shape_key_remove(all=True)

        newObject.name = oldName + "_Applied"

        for mod in newObject.modifiers:
            # Not actually sure why this is necessary, but blender crashes without it. :| - Stel
            bpy.ops.object.mode_set(mode = 'EDIT')            
            bpy.ops.object.mode_set(mode = 'OBJECT')            
            if mod.type != 'ARMATURE':
                if (2, 90, 0) > bpy.app.version:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
                else:
                    bpy.ops.object.modifier_apply(modifier=mod.name)

        errorDuringShapeJoining = False
            
        for object in listOfShapeInstances:
            
            bpy.ops.object.select_all(action='DESELECT')
            newObject.select_set(True)
            object.select_set(True)

            bpy.context.view_layer.objects.active = newObject
      
            self.report({'INFO'},"Trying to join shapes!")
            print("Trying to join shapes.")
            
            result = bpy.ops.object.join_shapes()
            
            if(result != {'FINISHED'}):
                self.report({'ERROR'},"Could not add " + object.name + " as shape key.")
                print ("Could not add " + object.name + " as shape key.")
                errorDuringShapeJoining = True

        if(errorDuringShapeJoining == False):
            self.report({'INFO'},"SUCCESS!")
            print("Success!")
            #Reset old shape key values on new object
            index = 0
            for shapekey in newObject.data.shape_keys.key_blocks:
                if(index == 0):
                    index = index + 1
                    continue
                shapekey.value = listOfShapeKeyValues[index-1]
                index = index + 1

        #Reset old shape key values on original object
        index = 0
        for shapekey in originalObject.data.shape_keys.key_blocks:
            if(index == 0):
                index = index + 1
                continue
            shapekey.value = listOfShapeKeyValues[index-1]
            index = index + 1
            
            
        #Select and delete all temporal shapekey objects       
        bpy.ops.object.select_all(action='DESELECT')

        for object in listOfShapeInstances:
            object.select_set(True)
            
        bpy.ops.object.delete(use_global=False)
        
        
        #Reactivate armature modifiers on old and new object
    
        for mod in originalObject.modifiers:
            if mod.type == 'ARMATURE':
                originalObject.modifiers[mod.name].show_viewport = True

        for mod in newObject.modifiers:
            if mod.type == 'ARMATURE':
                newObject.modifiers[mod.name].show_viewport = True
                
        bpy.context.area.type = oldContext
        
        self.report({'INFO'},"APPLIED MODIFIERS")
        return {'FINISHED'}
    
    
    
class ShapeKeyApplier(bpy.types.Operator):
    """Replace the 'Basis' shape key with the currently selected shape key"""
    bl_idname = "object.shape_key_applier"
    bl_label = "Apply Selected Shapekey as Basis"
    
    def execute(self, context):
        
        O.object.select_all(action='DESELECT')
        bpy.context.object.select_set(True)

        #____________________________
        #Generate copy of object
        #____________________________
        originalName = bpy.context.object.name
        O.object.duplicate_move()
        bpy.context.object.name = originalName + "_Applied_Shape_Key"

        shapeKeyToBeApplied_name = bpy.context.object.active_shape_key.name

        listOfKeys = []

        #__________________________________________________
        #Store all shape keys in a list 
        #__________________________________________________

        for s_key in bpy.context.object.data.shape_keys.key_blocks:
            
            if s_key.name == shapeKeyToBeApplied_name:
                continue
            
            listOfKeys.append(s_key.name)

        #__________________________________________________

        for name in listOfKeys:
            
            SetActiveShapeKey(name)
            currentShapeKey = bpy.context.object.active_shape_key
            
            SetActiveShapeKey(shapeKeyToBeApplied_name)
            applyShapeKey = bpy.context.object.active_shape_key
            
            #Add new shapekey from mix
            O.object.shape_key_clear()
            
            currentShapeKey.value = 1.0
            applyShapeKey.value = 1.0
            
            O.object.shape_key_add(from_mix=True)
            bpy.context.object.active_shape_key.name = currentShapeKey.name + "_"
            
            
        for name in listOfKeys:
            
            #Set index to target shapekey
            SetActiveShapeKey(name)
            #Remove
            O.object.shape_key_remove(all=False)
            
            
        SetActiveShapeKey(shapeKeyToBeApplied_name)
        O.object.shape_key_remove(all=False)

        #Remove the "_" at the end of each shapeKey
        for s_key in bpy.context.object.data.shape_keys.key_blocks:
            
            s_key.name = s_key.name[:-1]
            
        self.report({'INFO'},"SHAPEKEY APPLIED AS BASIS")    
        return {'FINISHED'}
    
class ANIM_OT_zeroallkeys(bpy.types.Operator):
    """Sets all shapekeys to zero"""
    bl_idname = "anim.zeroallkeys"
    bl_label = "zeroallkeys"
    
    def execute(self, context):
        for skey in bpy.context.object.data.shape_keys.key_blocks:
            skey.value = 0.0
        
            
        self.report({'INFO'},"ALL SHAPEKEYS SET TO ZERO!")
        
        return{'FINISHED'}    

class ANIM_OT_insertKeyframe (bpy.types.Operator):
    bl_idname = "shapekeyextras.insert_keyframe"
    bl_label = "Insert Value Keyframe"
    bl_description = "Insert Keyframe (Shape Key Value) for all Shape Keys in Selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.object.data.shape_keys:       
            for skey in bpy.context.object.data.shape_keys.key_blocks:
                if skey != 'Basis':
                    context.object.data.shape_keys.key_blocks[skey].keyframe_insert(data_path="value")
            
            self.report({'INFO'}, "Keyframes inserted")
        else:
            self.report({'WARNING'}, "No shape keys found.")    
        return {'FINISHED'}





# ADD PANEL
class PT_shapeKeyHelpers(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "HOLLOWPIXEL SHAPEKEY OPERATORS"
    bl_idname = "SHAPEHELPER_PT_uipanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"


    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object.type == 'MESH'

    
    def draw(self, context):
        self.layout.separator()
        self.layout.operator(ANIM_OT_add52facialkeys.bl_idname, text="Add 52 Facial keys", icon="KEY_HLT")
        self.layout.operator(ANIM_OT_shapekeyxyz.bl_idname, text="XYZ Shapekeys", icon="AXIS_TOP")
        self.layout.operator(ShapeKeySplitter.bl_idname, text="Split Shapekeys", icon="ARROW_LEFTRIGHT")
        self.layout.operator(ShapeKeyPreserver.bl_idname, text="Apply Modifiers and Keep Shapekeys", icon="MODIFIER")
        self.layout.operator(ShapeKeyApplier.bl_idname, text="Apply Selected Shapekey as Basis", icon="DOT")
        self.layout.operator(ANIM_OT_zeroallkeys.bl_idname, text="ZERO ALL KEYS", icon="DOT")
        self.layout.operator(ANIM_OT_insertKeyframe.bl_idname, text="INSERT KEYFRAME", icon="DOT")


classes = (
    ANIM_OT_add52facialkeys,
    ANIM_OT_shapekeyxyz,
    ShapeKeySplitter,
    ShapeKeyPreserver,
    ShapeKeyApplier,
    ANIM_OT_zeroallkeys,
    ANIM_OT_insertKeyframe,
    PT_shapeKeyHelpers

)
    

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)



if __name__ == "__main__":
    register()
    
   
