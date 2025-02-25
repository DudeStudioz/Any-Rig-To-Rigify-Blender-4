import bpy
import rigify
from mathutils import Matrix, Vector

# # bpy.ops.object.select_all(action="DESELECT")
# # bpy.context.view_layer.objects.active = EXTERNAL_RIG_OBJ
# # EXTERNAL_RIG_OBJ.select_set(True)

EXTERNAL_RIG_NAME = ""
RIGIFY_NAME = "_rigify"


# ===========================================================
# ===========================================================
# ===========================================================


def delete_garbage():
    for block in bpy.data.brushes:
        block.use_fake_user = False
        if block.users == 0:
            bpy.data.brushes.remove(block)

    for block in bpy.data.objects:
        if block.users == 0:
            bpy.data.objects.remove(block)

    for block in bpy.data.actions:
        if block.use_fake_user == False:
            bpy.data.actions.remove(block)

    for block in bpy.data.armatures:
        block.use_fake_user = False
        if block.users == 0:
            bpy.data.armatures.remove(block)

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


# ===========================================================


def get_all_bone_names(obj, mode="EDIT"):
    current_mode = bpy.context.object.mode
    bone_name_list = []
    if mode == "EDIT":
        bpy.ops.object.mode_set(mode="EDIT")
        bone_name_list = [bones.name for bones in obj.data.edit_bones]
    if mode == "POSE":
        bpy.ops.object.mode_set(mode="POSE")
        bone_name_list = [bones.name for bones in obj.pose.bones]
    bpy.ops.object.mode_set(mode=current_mode)
    return bone_name_list


# ===========================================================


def make_bone(
    obj,
    bone_name,
    bone_parent=None,
    head=(0.0, 0.0, 0.0),
    tail=(0.5, 0.0, 0.0),
):
    """creates new bone
    Args:
                                                                                                                                    obj  (str)                       : name of the object to have the new bone
                                                                                                                                    bone_name (str)                       : name of the new bone
                                                                                                                                    bone_parent  (str, optional)             : name of the parent bone. Defaults to "none".
                                                                                                                                    x_head, y_head, z_head (float, optional): position of bone head on x axis . Defaults to 0.
                                                                                                                                    x_tail, y_tail, z_tail (float, optional): position of bone tail on x axis . Defaults to 0.5 or 0
    """
    obArm = bpy.context.active_object  # get the armature object
    ebs = obArm.data.edit_bones
    newBone = ebs.new(bone_name)
    newBone.head = head
    newBone.tail = tail
    if bone_parent != None:
        newBone.parent = ebs[bone_parent]


# ===========================================================

# nose_offset = 0.0


# def aligning_bones(metarig_bone, skeleton_bone, exclude_tail_align=["123"]):
#     """alignes metarig head, tail and roll to skeleton bone"""
#     skeleton_rig_matrix = EXTERNAL_RIG_OBJ.matrix_world

#     bone_world_head = skeleton_rig_matrix @ skeleton_bone.head
#     bone_world_tail = skeleton_rig_matrix @ skeleton_bone.tail

#     metarig_bone.head = bone_world_head

#     if metarig_bone.name not in exclude_tail_align:
#         metarig_bone.tail = bone_world_tail
#     else:
#         metarig_bone.length = skeleton_bone.length

#     # add offset to additional nose bones
#     if "nose" in metarig_bone.name:
#         # print(f"\t naska {metarig_bone}")
#         metarig_bone.head.z += nose_offset * (metarig_bone.length * 0.25)
#         metarig_bone.tail.z += nose_offset * (metarig_bone.length * 0.25)


# ===========================================================


def get_avarage(bone_List, head_tail="tail"):
    """get avarage of palms coordinates for hand.R/L"""
    x_avg, y_avg, z_avg = 0, 0, 0
    cnt = 0
    for bone in bone_List:
        if head_tail == "tail":
            head = bone.tail
        else:
            head = bone.head
        x_avg, y_avg, z_avg = x_avg + head.x, y_avg + head.y, z_avg + head.z
        cnt += 1

    x_avg, y_avg, z_avg = x_avg / cnt, y_avg / cnt, z_avg / cnt
    return x_avg, y_avg, z_avg


# ===========================================================


def get_rotation_diff(bone1, bone1Obj, bone2, bone2Obj):
    """gets difference in rotation of 2 bones"""

    # print(f"\t {bone1Obj.name} [{bone1}]")
    # print(f"\t {bone2Obj.name} [{bone2}]")

    # first_bone = bone1Obj.pose.bones[bone1]
    first_bone_rig_matrix = bone1Obj.matrix_world

    first_bone_matrix = first_bone_rig_matrix @ bone1.matrix
    first_bone_rot_quat_matrix = first_bone_matrix.to_quaternion()

    # second_bone = bone2Obj.pose.bones[bone2]
    second_rig_matrix = bone2Obj.matrix_world

    second_bone_matrix = second_rig_matrix @ bone2.matrix
    second_bone_rot_quat_matrix = second_bone_matrix.to_quaternion()

    return first_bone_rot_quat_matrix, second_bone_rot_quat_matrix


# ===========================================================

# get difference of bones to further delete from maps
def get_bones_key(lst_to_compare, bone_list, toDelete=False):
    key_lst = []
    for value in lst_to_compare:
        if value not in bone_list:
            key_lst.append(value)
    return key_lst


# ===========================================================


def get_keyframes(anim):
    """used to get first frame and last frame of the animation"""
    keyframes = []
    if anim is not None and anim.action is not None:
        for fcu in anim.action.fcurves:
            for keyframe in fcu.keyframe_points:
                x, y = keyframe.co
                if x not in keyframes:
                    keyframes.append((math.ceil(x)))
    return keyframes


# ===========================================================


def renme_current_anim(obj):
    """renames animation so that it would be easier to find it in Dope Sheet"""
    action = obj.animation_data.action
    new_action_name = (
        EXTERNAL_RIG_NAME +
        obj.name.replace(EXTERNAL_RIG_NAME, "") + "_Animation"
    )
    # for a in bpy.data.actions:
    #     print(a.name)
    #     if new_action_name == a.name:
    #         print("same Name", new_action_name)
    #         bpy.data.actions.remove(bpy.data.actions[name])
    action.name = new_action_name

    return action


# ===========================================================


def get_constrain_name(bone, parent_obj):
    """get name of current constraint"""
    bone_constrtaint = parent_obj.pose.bones[bone]
    constraint_list = bone_constrtaint.constraints.keys()
    return constraint_list[len(constraint_list) - 1]


infl = 0.45  # to put different influence to chest

# ===========================================================


def create_constraint(
    bone_to_get_constr,
    parent_obj,
    target_bone,
    target_bone_obj,
    rotation,
    rot_order="XYZ",
    copy_loc=False,
    copy_scale=False,
    transf_space="WORLD",
):
    """Creates constraints for bones

    Args:
        bone_to_get_constr (pose.bone): bone that will have the constraint
        parent_obj (string): name of object that has the bone to get constraint
        target_bone (string): name of the target bone from whitch constraints will be taken
        target_bone_obj (string): name of object that contains target bone
        rotation (euler): rotation on x,y,z  axis
        rot_order (str, optional): Rotation order of TRANSFORM constraint. Defaults to "XYZ".
    """
    # print(f"bone_to_get_constr {bone_to_get_constr.name}")
    # print(f"parent_obj        {parent_obj} ")
    # print(f"target_bone        {target_bone} ")
    # print(f"target_bone_obj   {target_bone_obj} ")
    # print(f"copy_loc   {copy_loc}")
    # print("")

    bone_to_get_constr.constraints.new("COPY_ROTATION")
    constr_name = get_constrain_name(bone_to_get_constr.name, parent_obj)
    rot_constr = bone_to_get_constr.constraints[constr_name]

    if ".0" not in rot_constr.name:
        rot_constr.target = target_bone_obj
        rot_constr.subtarget = target_bone

        # adds influence
        if "chest" in bone_to_get_constr.name and parent_obj == RIGIFY_NAME:
            global infl
            # .55+.45 = 1 for first time, next time infl = 0
            rot_constr.influence = 0.55 + infl
            infl = 0
            c = parent_obj.pose.bones["chest"].bone
            bpy.context.object.data.bones.active = c
            # else:
            # deletes prior Transformation Constraint for chest
            for c in bpy.context.selected_pose_bones:
                for constr in c.constraints:
                    if "Transformation" in constr.name:
                        c.constraints.remove(constr)

        # to clean up bone constrain tab
        rot_constr.show_expanded = False
    else:
        # delete created constraints cuz it already exists
        bone_to_get_constr.constraints.remove(rot_constr)

    # ===========================================================
    # transform
    bone_to_get_constr.constraints.new("TRANSFORM")
    constr_name = get_constrain_name(bone_to_get_constr.name, parent_obj)
    tran_constr = bone_to_get_constr.constraints[constr_name]

    if ".0" not in tran_constr.name:
        tran_constr.target = parent_obj

        if parent_obj.name == RIGIFY_NAME:
            tran_constr.subtarget = "root"
        else:
            tran_constr.subtarget = "skeleton:TransformationTarget"
        tran_constr.map_from = "ROTATION"
        tran_constr.map_to = "ROTATION"

        tran_constr.to_euler_order = rot_order

        (
            tran_constr.to_min_x_rot,
            tran_constr.to_min_y_rot,
            tran_constr.to_min_z_rot,
        ) = rotation

        tran_constr.owner_space = transf_space
        tran_constr.mix_mode_rot = "AFTER"

        # to clean up bone constrain tab
        tran_constr.show_expanded = False
    else:
        # delete created constraints cuz it already exists
        bone_to_get_constr.constraints.remove(tran_constr)

    # ===========================================================
    # copy location
    if copy_scale == True:

        # print(f"{bone_to_get_constr} ==> {target_bone}")
        bone_to_get_constr.constraints.new("COPY_LOCATION")
        # bone_to_get_constr.constraints.new("COPY_SCALE")
        constr_name = get_constrain_name(bone_to_get_constr.name, parent_obj)
        scale_constr = bone_to_get_constr.constraints[constr_name]
        if ".0" not in scale_constr.name:
            scale_constr.target = bpy.data.objects[target_bone_obj.name]
            scale_constr.subtarget = target_bone
            # scale_constr.owner_space = 'POSE'
            # scale_constr.target_space = 'POSE'

            scale_constr.show_expanded = False  # to clean up bone constrain tab
        else:
            # delete created constraints cuz it already exists
            bone_to_get_constr.constraints.remove(scale_constr)

    # ===========================================================
    # copy location
    if copy_loc == True:
        # print(f"{bone_to_get_constr} ==> {target_bone}")
        bone_to_get_constr.constraints.new("COPY_LOCATION")
        constr_name = get_constrain_name(bone_to_get_constr.name, parent_obj)
        loc_constr = bone_to_get_constr.constraints[constr_name]
        if ".0" not in loc_constr.name:
            loc_constr.target = bpy.data.objects[target_bone_obj.name]
            loc_constr.subtarget = target_bone
            loc_constr.show_expanded = False  # to clean up bone constrain tab
        else:
            # delete created constraints cuz it already exists
            bone_to_get_constr.constraints.remove(loc_constr)


# ======================================================================
def get_bone_location(bone_list, obj):
    """stores bones head and tail vectors"""
    bone_head_tail_loc = {}
    for bone in bone_list:
        metarig_bone = obj.data.edit_bones[bone]
        obj_matrix = obj.matrix_world

        bone_world_head = obj_matrix @ metarig_bone.head
        bone_world_tail = obj_matrix @ metarig_bone.tail

        metarig_bone.head = bone_world_head
        old_head = bone_world_head.copy()
        old_tail = bone_world_tail.copy()
        bone_head_tail_loc[metarig_bone] = [
            old_head, old_tail, metarig_bone.length]
    return bone_head_tail_loc


# ======================================================================
all_bones_between = []


def get_bones_between(starting_bone, ending_bone, sub_str_to_look_for=None):
    for c in starting_bone.children:
        # if sub_str_to_look_for in c.name:
        all_bones_between.append(c.name)
        if c != ending_bone:
            get_bones_between(c, ending_bone)
    return all_bones_between


def clean_bones_between():
    # clean up all_bones_between so that previous bones in list would be deleted
    global all_bones_between
    all_bones_between = []

# ======================================================================
# ======================================================================
# ======================================================================


def the_script(skeleton_model, parameters):
    # set 3d cursor to (0,0,0)
    bpy.context.scene.cursor.location = (0, 0, 0)

    # clean up all_bones_between so that previous bones in list would be deleted
    clean_bones_between()

    global RIGIFY_NAME
    # reset RIGIFY_NAME in case it already has value
    RIGIFY_NAME = "_rigify"

    head = parameters["head"]
    first_neck = parameters["first_neck"]
    last_neck = parameters["last_neck"]

    first_spine = parameters["first_spine"]
    last_spine = parameters["last_spine"]

    clav_r = parameters["clav_r"]
    clav_l = parameters["clav_l"]
    uparm_l = parameters["uparm_l"]
    uparm_r = parameters["uparm_r"]
    lowarm_l = parameters["lowarm_l"]
    lowarm_r = parameters["lowarm_r"]
    hand_l = parameters["hand_l"]
    hand_r = parameters["hand_r"]

    palm_pinky_r = parameters["palm_pinky_r"]
    pinky_01_r = parameters["pinky_01_r"]
    pinky_02_r = parameters["pinky_02_r"]
    pinky_03_r = parameters["pinky_03_r"]
    palm_ring_r = parameters["palm_ring_r"]
    ring_01_r = parameters["ring_01_r"]
    ring_02_r = parameters["ring_02_r"]
    ring_03_r = parameters["ring_03_r"]
    palm_middle_r = parameters["palm_middle_r"]
    middle_01_r = parameters["middle_01_r"]
    middle_02_r = parameters["middle_02_r"]
    middle_03_r = parameters["middle_03_r"]
    palm_index_r = parameters["palm_index_r"]
    index_01_r = parameters["index_01_r"]
    index_02_r = parameters["index_02_r"]
    index_03_r = parameters["index_03_r"]
    thumb_01_r = parameters["thumb_01_r"]
    thumb_02_r = parameters["thumb_02_r"]
    thumb_03_r = parameters["thumb_03_r"]
    palm_pinky_l = parameters["palm_pinky_l"]
    pinky_01_l = parameters["pinky_01_l"]
    pinky_02_l = parameters["pinky_02_l"]
    pinky_03_l = parameters["pinky_03_l"]
    palm_ring_l = parameters["palm_ring_l"]
    ring_01_l = parameters["ring_01_l"]
    ring_02_l = parameters["ring_02_l"]
    ring_03_l = parameters["ring_03_l"]
    palm_middle_l = parameters["palm_middle_l"]
    middle_01_l = parameters["middle_01_l"]
    middle_02_l = parameters["middle_02_l"]
    middle_03_l = parameters["middle_03_l"]
    palm_index_l = parameters["palm_index_l"]
    index_01_l = parameters["index_01_l"]
    index_02_l = parameters["index_02_l"]
    index_03_l = parameters["index_03_l"]
    thumb_01_l = parameters["thumb_01_l"]
    thumb_02_l = parameters["thumb_02_l"]
    thumb_03_l = parameters["thumb_03_l"]

    thigh_l = parameters["thigh_l"]
    thigh_r = parameters["thigh_r"]
    calf_l = parameters["calf_l"]
    calf_r = parameters["calf_r"]
    foot_l = parameters["foot_l"]
    foot_r = parameters["foot_r"]
    toe_l = parameters["toe_l"]
    toe_r = parameters["toe_r"]
    heel_l = parameters["heel_l"]
    heel_r = parameters["heel_r"]

    fingers_bool_r = parameters["fingers_bool_r"]
    fingers_bool_l = parameters["fingers_bool_l"]
    copy_loc_constr = parameters["copy_loc_constr"]

    # ===============================================================
    # delete value for fingers if the checkbox is off
    right_fingers = [palm_pinky_r, pinky_01_r, pinky_02_r, pinky_03_r, palm_ring_r, ring_01_r, ring_02_r, ring_03_r, palm_middle_r,
                     middle_01_r, middle_02_r, middle_03_r, palm_index_r, index_01_r, index_02_r, index_03_r, thumb_01_r, thumb_02_r, thumb_03_r]
    left_fingers = [palm_pinky_l, pinky_01_l, pinky_02_l, pinky_03_l, palm_ring_l, ring_01_l, ring_02_l, ring_03_l, palm_middle_l,
                    middle_01_l, middle_02_l, middle_03_l, palm_index_l, index_01_l, index_02_l, index_03_l, thumb_01_l, thumb_02_l, thumb_03_l]
    excluded_bones_to_create = []
    if fingers_bool_r == False:
        # add bones to excluded_bones_to_create to bypass them when creating metarig
        for f in right_fingers:
            excluded_bones_to_create.append(f)
        palm_pinky_r = ""
        pinky_01_r = ""
        pinky_02_r = ""
        pinky_03_r = ""
        palm_ring_r = ""
        ring_01_r = ""
        ring_02_r = ""
        ring_03_r = ""
        palm_middle_r = ""
        middle_01_r = ""
        middle_02_r = ""
        middle_03_r = ""
        palm_index_r = ""
        index_01_r = ""
        index_02_r = ""
        index_03_r = ""
        thumb_01_r = ""
        thumb_02_r = ""
        thumb_03_r = ""
        right_fingers = []

    if fingers_bool_l == False:
        # add bones to excluded_bones_to_create to bypass them when creating metarig
        for f in left_fingers:
            excluded_bones_to_create.append(f)
        palm_pinky_l = ""
        pinky_01_l = ""
        pinky_02_l = ""
        pinky_03_l = ""
        palm_ring_l = ""
        ring_01_l = ""
        ring_02_l = ""
        ring_03_l = ""
        palm_middle_l = ""
        middle_01_l = ""
        middle_02_l = ""
        middle_03_l = ""
        palm_index_l = ""
        index_01_l = ""
        index_02_l = ""
        index_03_l = ""
        thumb_01_l = ""
        thumb_02_l = ""
        thumb_03_l = ""
        left_fingers = []

    # ===============================================================

    # bpy.ops.object.mode_set(mode="OBJECT")
    # skeleton_model = bpy.context.active_object
    EXTERNAL_RIG_NAME = skeleton_model.name
    EXTERNAL_RIG_OBJ = bpy.data.objects[EXTERNAL_RIG_NAME]

    # ===============================================================
    # get all spines
    EXTERNAL_RIG_OBJ.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    all_ext_rig_bone_names = get_all_bone_names(EXTERNAL_RIG_OBJ)

    last_spine_bool = True
    if last_spine == "":
        last_spine_bool = False
        last_spine = first_spine

    last_spine_bone = EXTERNAL_RIG_OBJ.data.edit_bones[last_spine]

    # get all last spines parenst recursively
    all_spines = [i.name for i in last_spine_bone.parent_recursive]

    # add last spine to list of all spines
    all_spines = [last_spine] + all_spines

    # slice spine list till first spine
    all_spines = all_spines[0:all_spines.index(first_spine)+1]

    # remove duplicates
    all_spines = list(dict.fromkeys(all_spines))

    # set second_spine because, used in torso bone loc and in use case where 1st_spine.head == 2nd_spine.head
    first_spine_bone = EXTERNAL_RIG_OBJ.data.edit_bones[first_spine]
    if last_spine_bool == True:
        second_spine = [
            i.name for i in first_spine_bone.children if i.name in all_spines][0]
    else:
        second_spine = first_spine

    # add to parameters dict so these bones are created in metarig
    new_spines = (
        list(set(all_spines) - set([first_spine, last_spine])))

    # adding spine bones to parameters
    for i in new_spines:
        temp = f"new_{i}"
        parameters[temp] = i

    # make parenting dict for spines
    spine_parenting = {}
    for i in all_spines:
        spine_bone = EXTERNAL_RIG_OBJ.data.edit_bones[i]
        for c in spine_bone.children:
            if c.name in all_spines:
                # child: [parent, use_connect]
                spine_parenting[c.name] = [spine_bone.name, True]

    less_spine_bones = True if len(all_spines) <= 2 else False

    # ===============================================================
    # get neck bones
    # clean up all_bones_between so that previous bones in list would be deleted
    clean_bones_between()

    all_necks = []
    neck_parenting = {}
    if last_neck != "":
        last_neck = first_neck
        first_neck_bone = EXTERNAL_RIG_OBJ.data.edit_bones[first_neck]
        last_neck_bone = EXTERNAL_RIG_OBJ.data.edit_bones[last_neck]

        # get all neck bones
        all_necks = get_bones_between(first_neck_bone, last_neck_bone)
        all_necks.extend([first_neck, last_neck])

        # remove duplicates
        all_necks = list(dict.fromkeys(all_necks))

        # add to parameters dict so these bones are created in metarig
        new_necks = (
            list(set(all_necks) - set([first_neck, last_neck])))

        for i in new_necks:
            temp = f"new_{i}"
            parameters[temp] = i

        # make parenting dict for neck bones
        for i in all_necks:
            neck_bone = EXTERNAL_RIG_OBJ.data.edit_bones[i]
            for c in neck_bone.children:
                if c.name in all_necks:
                    # child: [parent, use_connect]
                    neck_parenting[c.name] = [neck_bone.name, True]

        if first_neck_bone == last_neck_bone or first_neck_bone == "":
            all_necks = [first_neck]
            neck_parenting = {}
    else:
        # add the only neck to list and dir
        all_necks = [first_neck]
        neck_parenting[first_neck] = [last_spine, False]
        last_neck = first_neck

    # ===============================================================
    # make new bones for skeleton_model
    bpy.ops.object.mode_set(mode="EDIT")
    make_bone(EXTERNAL_RIG_OBJ, "skeleton:TransformationTarget")
    all_ext_rig_bone_names = get_all_bone_names(EXTERNAL_RIG_OBJ)

    # make new bones for skeleton_model and place it properly
    transf_target_coord_1 = EXTERNAL_RIG_OBJ.data.edit_bones[first_spine].head
    transf_target_coord_2 = EXTERNAL_RIG_OBJ.data.edit_bones[second_spine].head

    if transf_target_coord_2 == transf_target_coord_1:
        transf_target_coord_2 = EXTERNAL_RIG_OBJ.data.edit_bones[second_spine].tail

    x = (transf_target_coord_1.x + transf_target_coord_2.x) / 2
    y = (transf_target_coord_1.y + transf_target_coord_2.y) / 2
    z = (transf_target_coord_1.z + transf_target_coord_2.z) / 2

    hip_tail = EXTERNAL_RIG_OBJ.data.edit_bones[second_spine].tail

    make_bone(
        EXTERNAL_RIG_OBJ,
        "skeleton:torso_bone",
        first_spine,
        (x, y, z),
        (hip_tail.x, hip_tail.y, hip_tail.z),
    )

    bpy.ops.object.mode_set(mode="POSE")
    pose_bone = bpy.context.object.pose.bones["skeleton:torso_bone"]
    pose_bone.rigify_type = "spines.basic_spine"
    pose_bone.rigify_parameters.pivot_pos = 1

    # ===============================================================
    # set inherit_scale = 'NONE' if stretch is on
    if copy_loc_constr == True:
        for bone in EXTERNAL_RIG_OBJ.data.edit_bones:
            bone.inherit_scale = 'NONE'

    # ===============================================================
    # adding human (metarig)
    print("\n\t Adding human (metarig)")

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.armature_human_metarig_add()
    so = bpy.context.active_object

    METARIG_NAME = f"{EXTERNAL_RIG_NAME}_metarig"
    so.name = METARIG_NAME
    METARIG_OBJ = bpy.data.objects[METARIG_NAME]

    # ===============================================================
    # delete bones
    EXTERNAL_RIG_OBJ.select_set(True)
    METARIG_OBJ.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    all_metarig_bone_names = get_all_bone_names(METARIG_OBJ)

    # deletes bones
    print("\n\t Removing extra bones from Metarig")
    for i in all_metarig_bone_names:
        bone = METARIG_OBJ.data.edit_bones[i]
        METARIG_OBJ.data.edit_bones.remove(bone)

    # ===============================================================
    # create bones in metarig
    all_ext_rig_bone_names = get_all_bone_names(EXTERNAL_RIG_OBJ)

    for bone in all_ext_rig_bone_names:
        # if bone in parameters.values():
        if bone not in excluded_bones_to_create:
            ft_bone = EXTERNAL_RIG_OBJ.data.edit_bones[bone]
            bone_world_head = EXTERNAL_RIG_OBJ.matrix_world @ ft_bone.head
            bone_world_tail = EXTERNAL_RIG_OBJ.matrix_world @ ft_bone.tail
            h_x, h_y, h_z = bone_world_head.x, bone_world_head.y, bone_world_head.z
            t_x, t_y, t_z = bone_world_tail.x, bone_world_tail.y, bone_world_tail.z
            # h_x, h_y, h_z = (ft_bone.head.x, ft_bone.head.y, ft_bone.head.z)
            # t_x, t_y, t_z = (ft_bone.tail.x,ft_bone.tail.y,ft_bone.tail.z)
            make_bone(METARIG_OBJ, bone, None,
                      (h_x, h_y, h_z), (t_x, t_y, t_z))

    # ===============================================================
    # add bones
    make_bone(METARIG_OBJ, "new_torso")

    # add heels if thare are no
    if heel_r == "" and heel_l == "":
        heels = {
            "heel_r": foot_r,
            "heel_l": foot_l,
        }

        # assign bone to var
        heel_r = "heel_r"
        heel_l = "heel_l"

        all_matarig_bone_names = get_all_bone_names(METARIG_OBJ)
        for heel, heel_parent in heels.items():
            if heel not in all_matarig_bone_names:
                make_bone(METARIG_OBJ, heel)

                new_heel = METARIG_OBJ.data.edit_bones[heel]
                heel_parent = METARIG_OBJ.data.edit_bones[heel_parent]

                # place heels
                new_heel.parent = heel_parent
                new_heel.tail = heel_parent.head
                new_heel.tail.z = (heel_parent.head.z - 0) / 2
                delta = 1 if heel_parent.head.x > 0 else -1
                new_heel.tail.x += (heel_parent.length/2)*delta

                new_heel.head = new_heel.tail
                new_heel.head.x -= (heel_parent.length)*delta

    # # ===============================================================
    # parent bones, parent bone.tail to child.head, asign use_connect
    parenting_bones = {
        # child: [parent, use_connect]
        head: [last_neck, True],
        first_neck: [last_spine, False],

        # spine_004: [spine_003, True],
        # spine_003: [spine_002, True],
        # spine_002: [spine_001, True],
        second_spine: [first_spine, True],

        thigh_l: [first_spine, False],
        thigh_r: [first_spine, False],
        calf_r: [thigh_r, True],
        foot_r: [calf_r, True],
        toe_r: [foot_r, True],
        calf_l: [thigh_l, True],
        foot_l: [calf_l, True],
        toe_l: [foot_l, True],

        clav_r: [last_spine, False],
        uparm_r: [clav_r, False],
        lowarm_r: [uparm_r, True],
        hand_r: [lowarm_r, True],
        clav_l: [last_spine, False],
        uparm_l: [clav_l, False],
        lowarm_l: [uparm_l, True],
        hand_l: [lowarm_l, True],

        # fingers
        palm_pinky_r: [hand_r, False],
        pinky_01_r: [palm_pinky_r, False],
        pinky_02_r: [pinky_01_r, True],
        pinky_03_r: [pinky_02_r, True],

        palm_ring_r: [hand_r, False],
        ring_01_r: [palm_ring_r, False],
        ring_02_r: [ring_01_r, True],
        ring_03_r: [ring_02_r, True],

        palm_middle_r: [hand_r, False],
        middle_01_r: [palm_middle_r, False],
        middle_02_r: [middle_01_r, True],
        middle_03_r: [middle_02_r, True],

        palm_index_r: [hand_r, False],
        index_01_r: [palm_index_r, False],
        index_02_r: [index_01_r, True],
        index_03_r: [index_02_r, True],

        thumb_01_r: [hand_r, False],
        thumb_02_r: [thumb_01_r, True],
        thumb_03_r: [thumb_02_r, True],

        # left fingers
        palm_pinky_l: [hand_l, False],
        pinky_01_l: [palm_pinky_l, False],
        pinky_02_l: [pinky_01_l, True],
        pinky_03_l: [pinky_02_l, True],

        palm_ring_l: [hand_l, False],
        ring_01_l: [palm_ring_l, False],
        ring_02_l: [ring_01_l, True],
        ring_03_l: [ring_02_l, True],

        palm_middle_l: [hand_l, False],
        middle_01_l: [palm_middle_l, False],
        middle_02_l: [middle_01_l, True],
        middle_03_l: [middle_02_l, True],

        palm_index_l: [hand_l, False],
        index_01_l: [palm_index_l, False],
        index_02_l: [index_01_l, True],
        index_03_l: [index_02_l, True],

        thumb_01_l: [hand_l, False],
        thumb_02_l: [thumb_01_l, True],
        thumb_03_l: [thumb_02_l, True],
    }

    # add spine parenting to parenting_bones dict
    parenting_bones.update(spine_parenting)
    parenting_bones.update(neck_parenting)

    # if no palms, paretn 1st finger bone to hand r/l
    palm_correct = {
        pinky_01_r: hand_r,
        ring_01_r: hand_r,
        middle_01_r: hand_r,
        index_01_r: hand_r,
        pinky_01_l: hand_l,
        ring_01_l: hand_l,
        middle_01_l: hand_l,
        index_01_l: hand_l,
    }
    for f, palm in palm_correct.items():
        if parenting_bones[f][0] == '':
            parenting_bones[f][0] = palm

    # switching hip head with tail if hip head is the same as spine head
    first_spine_bone = METARIG_OBJ.data.edit_bones[first_spine]
    second_spine_bone = METARIG_OBJ.data.edit_bones[second_spine]
    second_spine_bone_head_copy = second_spine_bone.head.copy()
    hip_spine_bool = False
    if first_spine_bone.head == second_spine_bone.head and len(all_spines) > 1:
        hip_spine_bool = True
        first_spine_bone_tail = first_spine_bone.tail.copy()
        first_spine_bone_head = first_spine_bone.head.copy()
        first_spine_bone.head = first_spine_bone_tail
        first_spine_bone.tail = first_spine_bone_head

    exclude_align = {
        # parent: correct child
        first_spine: second_spine,
        # spine_003: spine_004,
        last_spine: first_neck,
        palm_index_l: index_01_l,
        palm_index_r: index_01_r,
        # index_01_r: index_02_r,
        hand_l: None,
        hand_r: None,
        head: None,
    }

    # copy head.head location to further reapply it if head offsets during connect
    head_bone = METARIG_OBJ.data.edit_bones[head]
    head_bone_head = head_bone.head.copy()

    if less_spine_bones == True:
        exclude_align[first_spine] = None

    all_matarig_bone_names = get_all_bone_names(METARIG_OBJ)
    for child, parent in parenting_bones.items():
        if parent[0] != "" and child != "":
            parent_bone = METARIG_OBJ.data.edit_bones[parent[0]]
            child_bone = METARIG_OBJ.data.edit_bones[child]

            child_bone.parent = parent_bone

            # parent bone.tail to child.head
            if parent[0] in exclude_align.keys():
                if exclude_align[parent[0]] != None:
                    if exclude_align[parent[0]] in all_matarig_bone_names:
                        parent_bone.tail = METARIG_OBJ.data.edit_bones[exclude_align[parent[0]]].head
            else:
                parent_bone.tail = child_bone.head

            # connect
            child_bone.use_connect = parent[1]

    if hip_spine_bool == True and less_spine_bones == True:
        second_spine_bone.head = second_spine_bone_head_copy

    # hip tail to 2nd spine head if there are 2 spine bones
    if hip_spine_bool == False and less_spine_bones == True:
        if len(all_spines) == 2:
            first_spine_bone.tail = second_spine_bone_head_copy

    # # reapply head location in case it offsets during connect
    # head_bone = METARIG_OBJ.data.edit_bones[head]
    # head_bone.head = head_bone_head

    # ===============================================================
    # add additional bones
    all_skeleton_pose_bones = get_all_bone_names(EXTERNAL_RIG_OBJ)

    # add new created bones to parameters to further get extra bones
    new_bones = [
        'heel_l',
        'heel_r',
        'new_torso',
        "skeleton:TransformationTarget",
        "skeleton:torso_bone",
    ]

    for i in new_bones:
        parameters[f"new_{i}"] = i

    # store these bones
    extra_bones = [
        bone for bone in all_skeleton_pose_bones if bone not in parameters.values()]

    for bone in extra_bones:
        ext_rig_bone = EXTERNAL_RIG_OBJ.data.edit_bones[bone]
        meta_bone = METARIG_OBJ.data.edit_bones[bone]
        if ext_rig_bone.parent is not None:
            if ext_rig_bone.parent.name in all_matarig_bone_names:
                new_parent = METARIG_OBJ.data.edit_bones[ext_rig_bone.parent.name]
                meta_bone.parent = new_parent

    # ===============================================================
    # places hands at an avarage distance of its child head
    hand_L = METARIG_OBJ.data.edit_bones[hand_l]
    hand_R = METARIG_OBJ.data.edit_bones[hand_r]
    hand_L_children = hand_L.children
    hand_R_children = hand_R.children

    hand_child_names = [i.name for i in (hand_L_children + hand_R_children)]
    bone_head_tail_loc = {}
    bone_head_tail_loc = get_bone_location(hand_child_names, METARIG_OBJ)

    # removes thumbs from heand.children list
    hand_L_children = [f for f in hand_L_children if thumb_01_l != f.name]
    hand_R_children = [f for f in hand_R_children if thumb_01_r != f.name]

    # if models has no palms, get average point of fingers
    alternative_children_r = [pinky_01_r, ring_01_r, middle_01_r, index_01_r]
    alternative_children_l = [pinky_01_l, ring_01_l, middle_01_l, index_01_l]
    if len(hand_R_children) == 0:
        hand_R_children = [METARIG_OBJ.data.edit_bones[f]
                           for f in alternative_children_r if f != ""]
    if len(hand_L_children) == 0:
        hand_L_children = [METARIG_OBJ.data.edit_bones[f]
                           for f in alternative_children_l if f != ""]

    if (len(hand_L_children) < 4) or (len(hand_R_children) < 4):
        finger_child_vectors_L = [fc.head for fc in hand_L_children]
        finger_child_vectors_R = [fc.head for fc in hand_R_children]
        if fingers_bool_l == True:
            median_point_l = sum(finger_child_vectors_L, Vector()) / len(
                finger_child_vectors_L
            )
            hand_L.tail = median_point_l

        if fingers_bool_r == True:
            median_point_r = sum(finger_child_vectors_R, Vector()) / len(
                finger_child_vectors_R
            )
            hand_R.tail = median_point_r

        bone_head_tail_loc = {}
        bone_head_tail_loc[hand_R] = [hand_R.head, hand_R.tail]
        bone_head_tail_loc[hand_L] = [hand_L.head, hand_L.tail]
    else:
        x_avg, y_avg, z_avg = get_avarage(hand_L_children)
        hand_L.tail = (x_avg, y_avg, z_avg)

        x_avg, y_avg, z_avg = get_avarage(hand_R_children)
        hand_R.tail = (x_avg, y_avg, z_avg)

    # ===============================================================
    # fix hands orientation if there are no fingers
    hands_orient = {
        # hand = [parent rot, finger check]
        hand_r: [lowarm_r, fingers_bool_r],
        hand_l: [lowarm_l, fingers_bool_l],
    }

    for key, value in hands_orient.items():
        if value[1] == False:
            hand = METARIG_OBJ.data.edit_bones[key]
            upper_arm_bone = METARIG_OBJ.data.edit_bones[value[0]]

            # quatRot1, quatRot2 = get_rotation_diff(
            #     hand, METARIG_OBJ, upper_arm_bone, METARIG_OBJ)
            # rot_diff_quat = quatRot2.rotation_difference(quatRot1)
            # rot_diff_euler = rot_diff_quat.to_euler()

            arm_len = upper_arm_bone.length
            # arm_len = upper_arm_bone.length.copy()
            # lengthen forearm
            upper_arm_bone.length *= 1.5
            # palce hand tail @ lengthen forearm tail
            hand.tail = upper_arm_bone.tail
            # restore forearm original length
            upper_arm_bone.length = arm_len

    # ===============================================================
    # fixing last fingers bone
    last_fingers_bone = [
        pinky_03_r,
        ring_03_r,
        middle_03_r,
        index_03_r,
        thumb_03_r,
        pinky_03_l,
        ring_03_l,
        middle_03_l,
        index_03_l,
        thumb_03_l,
    ]

    for f in last_fingers_bone:
        if f != "":
            finger_bone = METARIG_OBJ.data.edit_bones[f]
            finger_bone_original = EXTERNAL_RIG_OBJ.data.edit_bones[f]
            if len(finger_bone.children) == 0:
                # check if there is children in original model
                if len(finger_bone_original.children) == 0:
                    for c in EXTERNAL_RIG_OBJ.children:
                        verts_names = [i.name for i in c.vertex_groups]
                        if f in verts_names:
                            finger_vert_vector = []

                            # get vertices
                            finger_vertex_g = c.vertex_groups[f]
                            finger_verts = [
                                vert
                                for vert in c.data.vertices
                                if finger_vertex_g.index in [i.group for i in vert.groups]
                            ]
                            # get location
                            for i in finger_verts:
                                co_final = c.matrix_world @ i.co
                                finger_vert_vector.append(co_final)

                            finger_median_point = sum(finger_vert_vector, Vector()) / len(
                                finger_vert_vector
                            )
                            finger_bone.tail = finger_median_point
                            break
                            # else:
                            # print("no verts")
                            #     print(finger_vert_vector)
                            #     print(finger_vertex_g)

    # ===============================================================
    # fix fingers orientation
    all_metarig_bone_names = get_all_bone_names(METARIG_OBJ)

    all_fingers_but_thumbs = (right_fingers + left_fingers)

    # remove thumbs as they usually don't need axis change
    thumbs = [
        thumb_01_r,
        thumb_02_r,
        thumb_03_r,
        thumb_01_l,
        thumb_02_l,
        thumb_03_l,
    ]

    # remove duplicates, empty variables
    all_fingers_but_thumbs = list(dict.fromkeys(all_fingers_but_thumbs))
    if '' in all_fingers_but_thumbs:
        all_fingers_but_thumbs.remove('')

    for t in thumbs:
        if t in all_fingers_but_thumbs:
            all_fingers_but_thumbs.remove(t)

    METARIG_OBJ.data.show_axes = True

    # make z axis point in bend direction
    for f in all_fingers_but_thumbs:
        if f in all_metarig_bone_names:
            finger_bone = METARIG_OBJ.data.edit_bones[f]
            # finger_bone.align_roll(-finger_bone.z_axis) # works w/ mixamo & fortnite
            # ===============================================================
            roll = finger_bone.tail.copy()
            roll[2] -= 1
            finger_bone.align_roll(-roll)

    # rotation axis to 'X Manual'
    bpy.ops.object.mode_set(mode="POSE")
    for f in all_fingers_but_thumbs:
        pose_bone = METARIG_OBJ.pose.bones[f]
        # pose_bone.rigify_parameters.rotation_axis = "x"
        pose_bone.rigify_parameters.primary_rotation_axis = 'X'

    # ===============================================================

    # assign rig type to bones
    all_ext_rig_bone_names = get_all_bone_names(EXTERNAL_RIG_OBJ)
    all_metarig_bone_names = get_all_bone_names(METARIG_OBJ)

    rigifyType = {
        # head: "spines.super_head",
        first_neck: "spines.super_head",
        clav_l: "basic.super_copy",
        clav_r: "basic.super_copy",
        uparm_r: "limbs.super_limb",
        uparm_l: "limbs.super_limb",
        # fingers
        palm_index_r: "limbs.super_palm",
        pinky_01_r: "limbs.super_finger",
        ring_01_r: "limbs.super_finger",
        middle_01_r: "limbs.super_finger",
        index_01_r: "limbs.super_finger",
        thumb_01_r: "limbs.super_finger",
        # left fnigers
        palm_index_l: "limbs.super_palm",
        pinky_01_l: "limbs.super_finger",
        ring_01_l: "limbs.super_finger",
        middle_01_l: "limbs.super_finger",
        index_01_l: "limbs.super_finger",
        thumb_01_l: "limbs.super_finger",

        first_spine: "spines.basic_spine",
        thigh_l: "limbs.leg",
        thigh_r: "limbs.leg",
    }

    # change rigify type for spine if there's only one spine
    if less_spine_bones == True:
        for s in all_spines:
            rigifyType[s] = "basic.super_copy"
        rigifyType[first_neck] = "basic.super_copy"
        rigifyType[head] = "basic.super_copy"

    bpy.ops.object.mode_set(mode="POSE")
    for bone, rig_type in rigifyType.items():
        if bone in all_metarig_bone_names:
            pose_bone = METARIG_OBJ.pose.bones[bone]
            pose_bone.rigify_type = rig_type
            rigify_param = pose_bone.rigify_parameters

            if bone == thigh_r or bone == thigh_l:
                rigify_param.extra_ik_toe = True
            #     rigify_param.limb_type = "leg"

            # if bone == pelvis:
                # rigify_param['make_control'] = 0

            if bone == last_neck:
                rigify_param.connect_chain = True

            if bone == clav_r or bone == clav_l:
                rigify_param.super_copy_widget_type = "shoulder"

    # ===============================================================
    # adding bones to respective layer
    # Ensure we are in pose mode
    bpy.ops.object.mode_set(mode="POSE")

    # Get existing Rigify bone collections or create new ones
    rigify_collections = METARIG_OBJ.data.collections

    def get_or_create_bone_collection(name):
        """Retrieve an existing Rigify collection or create a new one."""
        if name in rigify_collections:
            return rigify_collections[name]
        else:
            collection = rigify_collections.new(name)
            return collection

    # Define new collections for FK, Tweak, Fingers, and Torso
    bone_collections = {
        "Head": [head],
        "Arm.L (IK)": [uparm_l, lowarm_l, hand_l],
        "Arm.R (IK)": [uparm_r, lowarm_r, hand_r],
        "Leg.L (IK)": [thigh_l, calf_l, foot_l, toe_l, heel_l],
        "Leg.R (IK)": [thigh_r, calf_r, foot_r, toe_r, heel_r],
        "Arm.L (FK)": [uparm_l, lowarm_l, hand_l],
        "Arm.R (FK)": [uparm_r, lowarm_r, hand_r],
        "Leg.L (FK)": [thigh_l, calf_l, foot_l, toe_l, heel_l],
        "Leg.R (FK)": [thigh_r, calf_r, foot_r, toe_r, heel_r],
        "Arm.L (Tweak)": [uparm_l, lowarm_l, hand_l],
        "Arm.R (Tweak)": [uparm_r, lowarm_r, hand_r],
        "Leg.L (Tweak)": [thigh_l, calf_l, foot_l, toe_l, heel_l],
        "Leg.R (Tweak)": [thigh_r, calf_r, foot_r, toe_r, heel_r],
        
        # Fingers (Main Collection)
        "Fingers": [
            palm_index_r, palm_middle_r, palm_ring_r, palm_pinky_r, thumb_01_r,
            palm_index_l, palm_middle_l, palm_ring_l, palm_pinky_l, thumb_01_l,
            index_01_r, middle_01_r, ring_01_r, pinky_01_r,
            index_01_l, middle_01_l, ring_01_l, pinky_01_l,
        ],
        
        # Fingers (Detail) - Tweak Collection
        "Fingers (Detail)": [
            index_02_r, index_03_r,
            middle_02_r, middle_03_r,
            ring_02_r, ring_03_r,
            pinky_02_r, pinky_03_r,
            thumb_02_r, thumb_03_r,
            index_02_l, index_03_l,
            middle_02_l, middle_03_l,
            ring_02_l, ring_03_l,
            pinky_02_l, pinky_03_l,
            thumb_02_l, thumb_03_l,
        ],

        # Torso (Main Collection)
        "Torso": [
            first_spine, first_neck,  # First spine and first neck
        ],

        # Torso (Tweak) - Tweak Collection
        "Torso (Tweak)": [
            first_spine, first_neck,  # First spine and first neck tweaks
        ],
    }

    # Assign bones to collections
    for collection_name, bones in bone_collections.items():
        bone_collection = get_or_create_bone_collection(collection_name)

        for bone in bones:
            if bone in METARIG_OBJ.pose.bones:
                pose_bone = METARIG_OBJ.pose.bones[bone]
                bone_collection.assign(pose_bone.bone)

    print("✅ FK, Tweak, Fingers, and Torso collections created and assigned!")



    # ===============================================================
    # add bones like dyn, clothes bones etc
    # Ensure we are in POSE mode
    bpy.ops.object.mode_set(mode="POSE")

    # Get existing Rigify bone collections or create a new "Additional" collection
    rigify_collections = METARIG_OBJ.data.collections

    # Assign Rigify type to extra bones
    for bone in extra_bones:
        if bone in METARIG_OBJ.pose.bones:
            pose_bone = METARIG_OBJ.pose.bones[bone]
            pose_bone.rigify_type = "basic.super_copy"

    # Create the "Additional" bone collection
    additional_collection = get_or_create_bone_collection("Additional")

    # Assign extra bones to the "Additional" collection
    for bone in extra_bones:
        if bone in METARIG_OBJ.pose.bones:
            pose_bone = METARIG_OBJ.pose.bones[bone]
            additional_collection.assign(pose_bone.bone)

    print("✅ Extra bones assigned to the 'Additional' Rigify collection in Blender 4!")


    # ===============================================================
    # fixing new_torso orinetation
    bpy.ops.object.mode_set(mode="EDIT")
    new_torso_bone = METARIG_OBJ.data.edit_bones["new_torso"]
    spine_bone = METARIG_OBJ.data.edit_bones[second_spine]
    if first_spine == "":
        first_spine_bone = spine_bone.children[0]
    else:
        first_spine_bone = METARIG_OBJ.data.edit_bones[first_spine]

    if first_spine_bone.children:
        new_torso_bone.tail = (first_spine_bone.head + first_spine_bone.tail) / 2
    else:
        new_torso_bone.tail = spine_bone.tail  # Fallback if no children

    new_torso_bone.head = (spine_bone.head + spine_bone.tail) / 2


    # ===============================================================
    # this would be an option
    # get FT height. This is to move upper_arm.R/L, thigh.L/R
    all_z = []
    for corner in EXTERNAL_RIG_OBJ.bound_box:
        corner_vector = EXTERNAL_RIG_OBJ.matrix_world @ Vector(corner)
        all_z.append(corner_vector[2])

    if all_z:
        skeleton_height = max(all_z) - min(all_z)
        skeleton_height_percent = skeleton_height * 0.002
    else:
        skeleton_height_percent = 0  # Safe fallback

    # print(f"skeleton_height         {skeleton_height} ")
    # print(f"skeleton_height_percent {skeleton_height_percent} ")

    changeHeadPos = {
        uparm_l: skeleton_height_percent,
        uparm_r: skeleton_height_percent,
        thigh_l: -skeleton_height_percent,
        thigh_r: -skeleton_height_percent,
    }

    all_metarig_bone_names = get_all_bone_names(METARIG_OBJ)
    for key, value in changeHeadPos.items():
        if key in all_metarig_bone_names:
            METARIG_OBJ.data.edit_bones[key].tail.y += value

    # switching hip head with tail if hip head is the same as spine head
    first_spine_bone = METARIG_OBJ.data.edit_bones[first_spine]
    second_spine_bone = METARIG_OBJ.data.edit_bones[second_spine]
    if hip_spine_bool == True:
        first_spine_bone.head = first_spine_bone.tail
        first_spine_bone.head[2] -= skeleton_height_percent

    bpy.ops.object.mode_set(mode="POSE")

    # # rotation axis to 'X Manual'
    # for key, value in changeHeadPos.items():
    #     if key in all_metarig_bone_names:
    #         print(key, value)
    #         pose_bone = METARIG_OBJ.pose.bones[key]
    #         pose_bone.rigify_parameters.rotation_axis = "x"

    # # ===============================================================
    bpy.ops.object.mode_set(mode="POSE")

    # Define FK & Tweak assignments for arms, legs, and torso
    fk_tweak_assignments = {
        thigh_l: ("Leg.L (FK)", "Leg.L (Tweak)"),
        thigh_r: ("Leg.R (FK)", "Leg.R (Tweak)"),
        uparm_r: ("Arm.R (FK)", "Arm.R (Tweak)"),
        uparm_l: ("Arm.L (FK)", "Arm.L (Tweak)"),
        first_spine: ("Torso", "Torso (Tweak)"),  # ✅ Add Torso assignments
        first_neck: ("Torso", "Torso (Tweak)"),   # ✅ Add Torso assignments
    }

    # Assign FK & Tweak layers to arms, legs, and torso
    for bone, (fk_name, tweak_name) in fk_tweak_assignments.items():
        if bone in METARIG_OBJ.pose.bones:
            pose_bone = METARIG_OBJ.pose.bones[bone]
            rigify_param = pose_bone.rigify_parameters

            # Enable FK/Tweak collections
            rigify_param.assign_fk_collections = True
            rigify_param.assign_tweak_collections = True

            # Ensure the correct bone is active
            bpy.context.object.data.bones.active = pose_bone.bone

            # Assign FK Collection (Torso)
            bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
            if len(rigify_param.fk_coll_refs) > 0:
                rigify_param.fk_coll_refs[-1].name = fk_name

            # Assign Tweak Collection (Torso Tweak)
            bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
            if len(rigify_param.tweak_coll_refs) > 0:
                rigify_param.tweak_coll_refs[-1].name = tweak_name

            print(f"✅ Assigned {fk_name} & {tweak_name} to {bone}")

    bpy.ops.object.mode_set(mode="OBJECT")
    print("✅ FK, Tweak, and Torso assigned correctly!")




    # ===============================================================
    # Remove Rigify type from the root bone
    if "root" in METARIG_OBJ.pose.bones:
        pose_bone = METARIG_OBJ.pose.bones["root"]
        pose_bone.rigify_type = ""  # Remove Rigify settings from root

    print("⚠️ Removed Rigify type from 'root' bone")



    # ===============================================================

    print("\t Generating Rig")

    # Generate Rigify rig
    cnt = bpy.context
    rigify.generate.generate_rig(cnt, METARIG_OBJ)

    # Rename Rigify rig dynamically
    rig = bpy.context.active_object
    rig.select_set(True)

    # Ensure correct naming
    new_rig_name = f"{EXTERNAL_RIG_NAME}_RIGIFY"
    rig.name = new_rig_name
    RIGIFY_NAME = new_rig_name
    RIGIFY_OBJ = bpy.data.objects[RIGIFY_NAME]

    print(f"✅ Generated Rigify rig: {RIGIFY_NAME}")

    # ===============================================================
    # Convert old layer system to Bone Collections
    rigify_collections = RIGIFY_OBJ.data.collections

    # Ensure key control collections are enabled
    def enable_bone_collection(name):
        """Enable a specific Rigify Bone Collection in Blender 4."""
        if name in rigify_collections:
            rigify_collections[name].is_visible = True  # Ensure visibility



    # Enable key control collections
    important_collections = [
        "Torso", "Arm.L (IK)", "Arm.R (IK)", "Leg.L (IK)", "Leg.R (IK)", "Head", "Fingers", "Root", "Additional"
    ]

    for col_name in important_collections:
        enable_bone_collection(col_name)

    print("✅ Enabled key Rigify Bone Collections")

    # ===============================================================
    # Ensure Rigify rig is selected and ready
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    EXTERNAL_RIG_OBJ.select_set(True)
    RIGIFY_OBJ.select_set(True)

    bpy.ops.object.mode_set(mode="POSE")
    EXTERNAL_RIG_OBJ.data.pose_position = "REST"
    RIGIFY_OBJ.data.pose_position = "POSE"

    print("✅ Rigify rig setup complete!")


    # ===============================================================
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    # METARIG_OBJ.select_set(False)
    EXTERNAL_RIG_OBJ.select_set(True)
    RIGIFY_OBJ.select_set(True)

    bpy.ops.object.mode_set(mode="POSE")
    EXTERNAL_RIG_OBJ.data.pose_position = "REST"
    RIGIFY_OBJ.data.pose_position = "POSE"

    # ===============================================================
    # set inherit scale to None for every bone on additional layer
    all_rigify_bone_names = get_all_bone_names(RIGIFY_OBJ, "POSE")

    for pb in extra_bones:
        if pb in all_rigify_bone_names:
            pb = RIGIFY_OBJ.pose.bones[pb]
            pb.bone.inherit_scale = 'NONE'

    # ===============================================================
    ik_fk = [
        "upperarm_parent_r",
        "thigh_parent_r",
        "upperarm_parent_l",
        "thigh_parent_l",
    ]

    all_rigify_bone_names = get_all_bone_names(RIGIFY_OBJ, "POSE")
    for i in ik_fk:
        # in case model doesn't have thighs
        if i in all_rigify_bone_names:
            p_bone = RIGIFY_OBJ.pose.bones[i]
            RIGIFY_OBJ.pose.bones[i]["IK_FK"] = 0

    # ===============================================================
    CONSTRAINTS_MAP = {
        # FT    : rigify
        "skeleton:torso_bone": ["torso", True],
        head: [head, False],
        first_neck: [first_neck, True],
        first_spine: [first_spine, True],
        second_spine: [second_spine, True],
        last_spine: [last_spine, True],
        # spine_001: [spine_001, True],
        # spine_002: [spine_002, True],
        # spine_003: [spine_003, True],
        # spine_004: [spine_004, True],
        clav_r: [clav_r, True],
        clav_l: [clav_l, True],
        uparm_r: [uparm_r, False],
        lowarm_r: [lowarm_r, False],
        hand_r: [hand_r, False],
        uparm_l: [uparm_l, False],
        lowarm_l: [lowarm_l, False],
        hand_l: [hand_l, False],
        # fingers
        palm_pinky_r: [palm_pinky_r, False],
        pinky_01_r: [pinky_01_r, False],
        pinky_02_r: [pinky_02_r, False],
        pinky_03_r: [pinky_03_r, False],
        palm_ring_r: [palm_ring_r, False],
        ring_01_r: [ring_01_r, False],
        ring_02_r: [ring_02_r, False],
        ring_03_r: [ring_03_r, False],
        palm_middle_r: [palm_middle_r, False],
        middle_01_r: [middle_01_r, False],
        middle_02_r: [middle_02_r, False],
        middle_03_r: [middle_03_r, False],
        palm_index_r: [palm_index_r, False],
        index_01_r: [index_01_r, False],
        index_02_r: [index_02_r, False],
        index_03_r: [index_03_r, False],
        thumb_01_r: [thumb_01_r, False],
        thumb_02_r: [thumb_02_r, False],
        thumb_03_r: [thumb_03_r, False],
        palm_pinky_l: [palm_pinky_l, False],
        pinky_01_l: [pinky_01_l, False],
        pinky_02_l: [pinky_02_l, False],
        pinky_03_l: [pinky_03_l, False],
        palm_ring_l: [palm_ring_l, False],
        ring_01_l: [ring_01_l, False],
        ring_02_l: [ring_02_l, False],
        ring_03_l: [ring_03_l, False],
        palm_middle_l: [palm_middle_l, False],
        middle_01_l: [middle_01_l, False],
        middle_02_l: [middle_02_l, False],
        middle_03_l: [middle_03_l, False],
        palm_index_l: [palm_index_l, False],
        index_01_l: [index_01_l, False],
        index_02_l: [index_02_l, False],
        index_03_l: [index_03_l, False],
        thumb_01_l: [thumb_01_l, False],
        thumb_02_l: [thumb_02_l, False],
        thumb_03_l: [thumb_03_l, False],

        thigh_r: [thigh_r, True],
        calf_r: [calf_r, False],
        foot_r: [foot_r, False],
        toe_r: [toe_r, False],
        thigh_l: [thigh_l, True],
        calf_l: [calf_l, False],
        foot_l: [foot_l, False],
        toe_l: [toe_l, False],
    }

    # don't generate torso if there are less than 2 spine bones
    if less_spine_bones == True:
        del CONSTRAINTS_MAP["skeleton:torso_bone"]

    # add spines to dict
    for s in all_spines:
        CONSTRAINTS_MAP[s] = [s, True]

    # add necks to dict
    for n in all_necks:
        CONSTRAINTS_MAP[n] = [n, True]

    # # delete foot bones from list if model doesn't have legs
    # if thigh_r_flag == True:
    #     del CONSTRAINTS_MAP[param_thigh_r]
    #     del CONSTRAINTS_MAP[param_calf_r]
    #     del CONSTRAINTS_MAP[param_foot_r]
    #     del CONSTRAINTS_MAP[param_ball_r]
    # if thigh_l_flag == True:
    #     del CONSTRAINTS_MAP[param_thigh_l]
    #     del CONSTRAINTS_MAP[param_calf_l]
    #     del CONSTRAINTS_MAP[param_foot_l]
    #     del CONSTRAINTS_MAP[param_ball_l]

    EXTERNAL_RIG_OBJ.data.pose_position = "REST"
    RIGIFY_OBJ.data.pose_position = "REST"

    bpy.ops.pose.select_all(action="DESELECT")

    # # ===============================================================
    # copy constraint from rigify to FT
    exclude_def_naming = [
        "torso",
        "neck",
        "chest",
    ]

    all_skeleton_pose_bones = get_all_bone_names(EXTERNAL_RIG_OBJ, "POSE")
    for key, value in CONSTRAINTS_MAP.items():
        # print(f"key   \t: {key}  , {key in all_skeleton_pose_bones} ")
        if key in all_skeleton_pose_bones:
            # changes names of bones
            if "chest" in value[0]:
                value[0] = "chest"

            if value[0] not in exclude_def_naming:
                value[0] = "DEF-" + value[0]

            if "skeleton:torso_bone" in value[0].lower():
                value[0] = "torso"

            # print(f"\t value : {value} ")
            # print(f"\t key   : {key} ")
            # print(f"===================================\n\n")

            bone1 = EXTERNAL_RIG_OBJ.pose.bones[key]
            bone2 = RIGIFY_OBJ.pose.bones[value[0]]

            quatRot1, quatRot2 = get_rotation_diff(
                # key, EXTERNAL_RIG_OBJ, value[0], RIGIFY_OBJ
                bone1, EXTERNAL_RIG_OBJ, bone2, RIGIFY_OBJ
            )
            rot_diff_quat = quatRot2.rotation_difference(quatRot1)
            rot_diff_euler = rot_diff_quat.to_euler()

            copy_loc = value[1]
            # value = RIGIFY_OBJ.pose.bones[value[0]]
            key = EXTERNAL_RIG_OBJ.pose.bones[key]

            create_constraint(
                key,
                EXTERNAL_RIG_OBJ,
                value[0],
                RIGIFY_OBJ,
                rot_diff_euler,
                rot_diff_euler.order,
                copy_loc,
                copy_loc_constr,
            )
    # ===============================================================
    # add constraints to additional bones
    for bone in extra_bones:
        if bone in all_skeleton_pose_bones:
            bone1 = EXTERNAL_RIG_OBJ.pose.bones[bone]
            bone2 = RIGIFY_OBJ.pose.bones[bone]
            quatRot1, quatRot2 = get_rotation_diff(
                bone1,
                EXTERNAL_RIG_OBJ,
                bone2,
                RIGIFY_OBJ,
            )
            rot_diff_quat = quatRot2.rotation_difference(quatRot1)
            rot_diff_euler = rot_diff_quat.to_euler()

            bone = EXTERNAL_RIG_OBJ.pose.bones[bone]

            create_constraint(
                bone,
                EXTERNAL_RIG_OBJ,
                bone.name,
                RIGIFY_OBJ,
                rot_diff_euler,
                rot_diff_euler.order,
                True,
            )

    # ===============================================================
    # custom shape scale
    custom_shape_scale = {
        "head": 1.5,
    }

    for k, v in custom_shape_scale.items():
        if value in all_ext_rig_bone_names:
            pose_bone = RIGIFY_OBJ.pose.bones[k]
            pose_bone.custom_shape_scale_xyz = (v, v, v)

    # # ===============================================================
    # Define which Bone Collections should be enabled
    collections_to_enable = [
        "Torso", "Arm.L (IK)", "Arm.R (IK)", "Leg.L (IK)", "Leg.R (IK)", "Head", "Fingers", "Root", "Additional"
    ]

    # Enable only the specified collections
    for collection in RIGIFY_OBJ.data.collections:
        if collection.name in collections_to_enable:
            collection.is_visible = True
        else:
            collection.is_visible = False  # Hide other collections

    # # ===============================================================

    RIGIFY_OBJ.data.pose_position = "POSE"
    EXTERNAL_RIG_OBJ.data.pose_position = "POSE"

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    METARIG_OBJ.hide_set(True)
    # EXTERNAL_RIG_OBJ.hide_set(True)
    EXTERNAL_RIG_OBJ.select_set(True)
    bpy.ops.object.mode_set(mode="POSE")

# #     # # ===============================================================

# #     delete_garbage()

# # # # ===============================================================
# # delete or comment this line when released
# params = ['head', 'neck_01', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'clavicle_r', 'clavicle_l', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'pinky_metacarpal_r', 'pinky_01_r', 'pinky_02_r', 'pinky_03_r', 'ring_metacarpal_r', 'ring_01_r', 'ring_02_r', 'ring_03_r', 'middle_metacarpal_r', 'middle_01_r', 'middle_02_r', 'middle_03_r', 'index_metacarpal_r', 'index_01_r', 'index_02_r', 'index_03_r',
#           'thumb_01_r', 'thumb_01_r', 'thumb_02_r', 'thumb_03_r', 'pinky_metacarpal_l', 'pinky_01_l', 'pinky_02_l', 'pinky_03_l', 'ring_metacarpal_l', 'ring_01_l', 'ring_02_l', 'ring_03_l', 'middle_metacarpal_l', 'middle_01_l', 'middle_02_l', 'middle_03_l', 'index_metacarpal_l', 'index_01_l', 'index_02_l', 'index_03_l', 'thumb_01_l', 'thumb_01_l', 'thumb_02_l', 'thumb_03_l', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r', '', '']
# bpy.ops.object.mode_set(mode="OBJECT")
# skeleton_model = bpy.context.active_object
# the_script(skeleton_model, params)
