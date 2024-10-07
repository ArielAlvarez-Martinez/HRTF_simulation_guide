"""

Add-on for Blender: Aligning 3D Models (Mainly Human Heads) to interaural axis using four points

OVERVIEW: The alignment is based on four key points: the right ear, left ear, nose, and top of the head.

GET VERTICES:
This functionality has four buttons: "Right Ear", "Left Ear", "Nose", and "Top Head". To use it, first select the corresponding vertex and then click the appropriate button. The order of selection does not matter.

ALIGN OBJECT:
This functionality contains four steps that must be performed in order: "Step 1", "Step 2", "Step 3", and "Step 4". Before executing Step 3, you must manually select the object/mesh.

CLEAN DATA:
Contains one button, "Clean Vertices", which clears the stored vertex coordinates.

Breakdown:

GET VERTICES:

The user must select four points (vertices) in Blender: the left ear, right ear, nose, and top of the head.
Ensure that "Interaction Mode" is set to Edit Mode and "Select Mode" is set to Vertex.
ALIGN OBJECT:
The alignment process follows four steps:

Step 1 (AlignToXYplane):

A new face (polygon) is created using the selected ear and nose vertices.
The view is aligned to the Top View (XY Plane).
A plane is inserted on the XY plane, at the same coordinates as the newly created face.
The object is set as a parent to the plane.
The plane is then selected, and both the plane and object are moved to the center.
Step 2 (DeletePlane):

To delete the plane without removing the selected points, it must be deleted via the Outliner.
The context is overridden to access the OUTLINER area.
In the Outliner, select and delete the plane.
Step 3 (Middlepoint):

At this point, the object is centered, and the XY plane (Z = 0) intersects the mesh at the level of the face created with the ears and nose.
The middle point of the interaural axis (the line between the ear vertices) is selected.
The middle point is translated to the coordinate center, moving the entire object/mesh accordingly.
Step 4 (CheckNoseandHead):

Finally, check that the nose is aligned with the positive X-axis and the top of the head is aligned with the positive Z-axis.
Delete the face created in Step 1.

Notes:
This add-on was primarily developed to align 3D models of human heads to the interaural axis. The alignment is based on four vertices from a PLY file: one for each ear, the nose, and the top of the head.

It was created as a tool to support my PhD research, so it is still a work in progress and may be updated in the future.

After completing the alignment, the interaural axis (line between the ears) will be positioned along the Y-axis, with the nose pointing in the positive X-axis direction, and the top of the head aligned with the positive Z-axis.

Important: The object must be selected manually before Step 3. Ensure this is done to avoid errors during alignment.

"""


import bpy # bpy is the Blender API ...  
import bmesh

#Define the addon properties ...Information below is only descriptive ...
bl_info = {
    "name" : "Object Aligner",
    "author" : "aalvmar",
    "description" : "This add-on will allow you align objects selecting 4 points",
    "version" : (0, 0, 1),
    "blender" : (3, 6, 2),
    "location" : "View3D > Sidebar > Item Tab",
    "category" : "Object"
}

# Gather the right ear vertice ...
class GetV1(bpy.types.Operator):
    bl_idname = "object.vertice1"
    bl_label = "Right Ear"

    def execute(self,context):
        
        # Get active mesh ...
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get mesh representation ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None

        # Get selected vertices ...
        for v in bm.verts:
            if v.select:
                global v1
                global v1_co
                global v1_idx
                v1 = v
                v1_co = list(v.co)
                v1_idx = v.index 
                print("Coordinates vertice 1: {}\nIndex vertice 1: {}".format(v1_co,v1_idx))
    
        # Deselect vertice
        bpy.ops.mesh.select_all(action="DESELECT")   

        return{"FINISHED"}

# Gather the left ear vertice ...
class GetV2(bpy.types.Operator):
    bl_idname = "object.vertice2"
    bl_label = "Left Ear"

    def execute(self,context):
        
        # Get active mesh ...
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get mesh representation ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None

        # Get selected vertices ...
        for v in bm.verts:
            if v.select:
                global v2
                global v2_co
                global v2_idx
                v2 = v
                v2_co = list(v.co)
                v2_idx = v.index 
                print("Coordinates vertice 2: {}\nIndex vertice 2: {}".format(v2_co,v2_idx))
    
        # Deselect vertice
        bpy.ops.mesh.select_all(action="DESELECT")   

        return{"FINISHED"}

# Gather the nose vertice ...
class GetV3(bpy.types.Operator):
    bl_idname = "object.vertice3"
    bl_label = "Nose"

    def execute(self,context):
        
        # Get active mesh ...
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get mesh representation ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None

        # Get selected vertices ...
        for v in bm.verts:
            if v.select:
                global v3
                global v3_co
                global v3_idx
                v3 = v
                v3_co = list(v.co)
                v3_idx = v.index 
                print("Coordinates vertice 3: {}\nIndex vertice 3: {}".format(v3_co,v3_idx))
    
        # Deselect vertice
        bpy.ops.mesh.select_all(action="DESELECT")   

        return{"FINISHED"}

# Gather the top head vertice (This vertice will be used to reference the Z axis)...
class GetV4(bpy.types.Operator):
    bl_idname = "object.vertice4"
    bl_label = "Top Head"

    def execute(self,context):
        
        # Get active mesh ...
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get mesh representation ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None

        # Get selected vertices ...
        for v in bm.verts:
            if v.select:
                global v4
                global v4_co
                global v4_idx
                v4 = v
                v4_co = list(v.co)
                v4_idx = v.index 
                print("Coordinates vertice 4: {}\nIndex vertice 4: {}".format(v4_co,v4_idx))
    
        # Deselect vertice
        bpy.ops.mesh.select_all(action="DESELECT")   

        return{"FINISHED"}        

# This class is the "Step 1"
class AlignToXYplane(bpy.types.Operator):
    bl_idname = "object.alignxy"
    bl_label = "Step 1" # Get the active mesh ...
    
    def execute(self,context):
        global v1_idx
        global v2_idx
        global v3_idx
        global v4_idx
        global v1_co
        global v2_co
        global v3_co
        global v4_co
        global face_idx
        
        # Set Edit Mode
        bpy.ops.object.mode_set(mode="EDIT")
        # Get the activate object 
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get the mesh represetantion ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None

        # Select vertices to build the face wich will be the reference to insert the "pivot" plane ...
        bm.verts.ensure_lookup_table()
        bm.verts[v1_idx].select = True
        bm.verts[v2_idx].select = True
        bm.verts[v3_idx].select = True

        # Update chanegs in edit mode 
        #bmesh.update_edit_mesh(me, True) # from Blender version 3 , bmesh.update_edit_mesh() only admit one element  
     	bmesh.update_edit_mesh(me)

        # Create a new face(polygon) with the 3 selected vertices above ...
        # Rigth Ear Vertice, Left Ear Vertice and Nose Vertice ...
        bpy.ops.mesh.edge_face_add()

        # Select the face ...
        # This part of the code will made later , cause I need time to find out the way of select the face automatically 

        # Align view from top view ...
        bpy.ops.view3d.view_axis(type='TOP', align_active=True) 

        # Cursor to selected ...
        bpy.ops.view3d.snap_cursor_to_selected()

        # print the active face ...
        for f in bm.faces:
            if f.select:
                face_idx = f.index
                print(face_idx)
        
        # Get back to Object Mode ... 
        bpy.ops.object.mode_set(mode="OBJECT")

        # Insert a plane ...
        bpy.ops.mesh.primitive_plane_add(align='VIEW')

        # Select the object and the inserted plane to align them 
        bpy.ops.object.select_all(action='SELECT')
        bpy.data.objects['Camera'].select_set(False)
        bpy.data.objects['Light'].select_set(False)
        
        # Set parent ...
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        # Deselect objects 
        bpy.ops.object.select_all(action='DESELECT')

        #Select only the plane
        bpy.data.objects['Plane'].select_set(True)

        # Center the plane ... # it allow move the object by moving(center) the plane 
        bpy.ops.object.rotation_clear(clear_delta=False)
        bpy.ops.object.location_clear(clear_delta=False)

        # Clear parent ..
        bpy.ops.object.select_all(action='SELECT')
        bpy.data.objects['Camera'].select_set(False)
        bpy.data.objects['Light'].select_set(False)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.select_all(action='DESELECT')
 
        # Set 3D cursor to the coordinate center ....  
        bpy.context.scene.cursor.location[0] = 0  
        bpy.context.scene.cursor.location[1] = 0
        bpy.context.scene.cursor.location[2] = 0

        # Apply transform ...  
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.data.objects['Camera'].select_set(False)
        bpy.data.objects['Light'].select_set(False)
        bpy.data.objects['Plane'].select_set(False)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Plane'].select_set(True)

        return{"FINISHED"}

# This class is the "Step 2"
class DeletePlane(bpy.types.Operator):
    bl_idname = "object.deleteplane"
    bl_label = "Step 2"

    def execute(self,context):
        # Delete the plane
        bpy.data.objects['Plane'].select_set(True)

        # To delete the plane without delete the selected points we need 
        # to delete it through 'outliner' operator ... to use outliner operators we need to 
        # override the active context and select the right one , in this case is the 
        # 'OUTLINER' area ... 
        override = bpy.context.copy()
        for area in bpy.context.screen.areas:
         if area.type == 'OUTLINER':
            override['area'] = area
            bpy.ops.outliner.delete(override)
            bpy.ops.outliner.collection_objects_select(override)
        
        return{'FINISHED'}

# This class is the "Step 3" ... It's necessary select the object manually before this step
class Middlepoint(bpy.types.Operator):
    bl_idname = "object.middlepoint"
    bl_label = "Step 3"

    def execute(self,context):
        global v1_idx
        global v2_idx
        global v3_idx
        global v4_idx
        global v1_co
        global v2_co
        global v3_co
        global v4_co
        global v1_co_new
        global v2_co_new
        

        # Aplly all changes rotation , translation and scale
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Set edit mode ... and select vertice
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
          
        # Get active mesh ...
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get mesh representation ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None 
        
        # Get the new coordinates of the points , this is due the rotation and transaltion ...
        # in the plane rotation step ...
        bm.verts.ensure_lookup_table()
        v1_co_new = list(bm.verts[v1_idx].co)
        v2_co_new = list(bm.verts[v2_idx].co)

        

        # Center of the line
        # Introduce the scale factor , cause it gonna affect the middle point of the line, so I've it into account in the formula ...
        #middle = (((v1[0]+v2[0])/2)*bpy.context.object.scale[0],((v1[1]+v2[1])/2)*bpy.context.object.scale[1],((v1[2]+v2[2])/2)*bpy.context.object.scale[2])
        middle = [sum(i)/2 for i in zip(v1_co_new,v2_co_new)]
        #print(middle)

        # Move the 3D cursor to the middle point of the line
        bpy.context.scene.cursor.location = middle


        # Move the Origin to the 3D Cursor ...
        bpy.ops.object.editmode_toggle()
        # Select the object
        bpy.context.active_object.select_set(state=True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        
        # Set 3D cursor to the coordinate center
        bpy.context.scene.cursor.location[0] = 0  
        bpy.context.scene.cursor.location[1] = 0
        bpy.context.scene.cursor.location[2] = 0

        # Set the object to the center of the coordinate center :
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0 
        bpy.context.object.location[2] = 0

        # Apply transform 
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)     


        return{"FINISHED"}

# This is the "Step 4"
class CheckNoseandHead(bpy.types.Operator):
    bl_idname = "object.checknoseandhead"
    bl_label = "Step 4"

    def execute(self,context):
        global v1_idx
        global v2_idx
        global v3_idx
        global v4_idx
        global v1_co
        global v2_co
        global v3_co
        global v4_co
        global v4_co_new
        global v3_co_new
        
        # Get active mesh ...
        bpy.ops.object.mode_set(mode='EDIT')
        obj = bpy.context.edit_object
        me = obj.data
     
        # Get mesh representation ...
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None 

        # Check the top head is in the positive z axis and the nose is in the positive
        # x axis ...
        bm.verts.ensure_lookup_table()
        v4_co_new = list(bm.verts[v4_idx].co)
        v3_co_new = list(bm.verts[v3_idx].co)
        if v4_co_new[2] < 0:
            bpy.context.object.rotation_euler[0] = 3.14159
	    # Apply transform 
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)	

        if v3_co_new[0] < 0:
            bpy.context.object.rotation_euler[2] = 3.14159
	    # Apply transform 
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        # Deleting the face created in the Step 1, it was the reference to insert the plane.        
        # Apply transform 
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='FACE')

        return{"FINISHED"}

class DeleteVertices(bpy.types.Operator):
    bl_idname = "object.deletevertices"
    bl_label = "Clean Vertices"

    def execute(self,context):
       global v1_idx 
       global v1_co
       global v2_idx 
       global v2_co
       global v3_idx 
       global v3_co
       global v4_idx 
       global v4_co
       global v1_co_new
       global v2_co_new

       # Select the object ...
       bpy.ops.object.mode_set(mode='OBJECT')
       bpy.ops.object.select_all(action='SELECT')
       bpy.data.objects['Camera'].select_set(False)
       bpy.data.objects['Light'].select_set(False)
       # Set edit mode ... 
       bpy.ops.object.mode_set(mode='EDIT')

       # Delete created face ... This is only a test , probably it will implemented in other area ... 
       bpy.ops.mesh.delete(type="FACE")
       
       # Deselect vertices in case it has been selected ...
       bpy.ops.mesh.select_all(action="DESELECT")  


       # Delete the values of the vertices 
       v1_idx = 0
       v1_co = []
       v2_idx = 0
       v2_co = []
       v3_idx = 0
       v3_co = []
       v4_idx = 0
       v4_co = []
       v1_co_new = []
       v2_co_new = []

       # Set vertice selection 
       bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

       return{"FINISHED"}

# Define the main class of the addon panel , it define the visual structure of the addon ...
class Main_panel(bpy.types.Panel):
    bl_label = "Object Aligner"
    bl_idname = "ADD1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Object Aligner"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Render the button
        # Create a row where the buttons are aligned 
        #row = layout.row()
        #row.operator("object.coordinates")
        #row.operator("object.print_coordinates")
        
        # Create two columns by using split layout
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="               GET VERTICES")
        col.operator("object.vertice1")
        col.operator("object.vertice2")
        col.operator("object.vertice3")
        col.operator("object.vertice4")
        col.label(text="")
        col.label(text="              ALIGN OBJECT")
        col.operator("object.alignxy")
        col.operator("object.deleteplane")
        col.label(text="       *select object manually*")
        col.operator("object.middlepoint")    
        col.operator("object.checknoseandhead")
        col.label(text="")
        col.label(text="                CLEAN DATA")
        col.operator("object.deletevertices")
    
# Register classes 
def register():
    print(">>>>> Addon registered <<<<<")
    bpy.utils.register_class(Main_panel)
    bpy.utils.register_class(GetV1)
    bpy.utils.register_class(GetV2)
    bpy.utils.register_class(GetV3)
    bpy.utils.register_class(GetV4)
    bpy.utils.register_class(AlignToXYplane)
    bpy.utils.register_class(DeletePlane)
    bpy.utils.register_class(Middlepoint)
    bpy.utils.register_class(CheckNoseandHead)
    bpy.utils.register_class(DeleteVertices)

def unregister():
    print(">>>>> Addon unregistered <<<<<")
    bpy.utils.unregister_class(Main_panel)
    bpy.utils.unregister_class(GetV1)
    bpy.utils.unregister_class(GetV2)
    bpy.utils.unregister_class(GetV3)
    bpy.utils.unregister_class(GetV4)
    bpy.utils.unregister_class(AlignToXYplane)
    bpy.utils.unregister_class(DeletePlane)
    bpy.utils.unregister_class(Middlepoint)
    bpy.utils.unregister_class(CheckNoseandHead)
    bpy.utils.unregister_class(DeleteVertices)

if __name__ == "__main__":
    register()
