from . import any_rig_to_rigify_v3
from bpy.types import Operator, Panel
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       )
import os
import json
import bpy
import addon_utils

# ===========================================================


def generate_rig(self, objects, params):
    # pop up menu if no object were selected
    if len(objects) == 0:
        print("no objects selected")
        self.report({"ERROR"}, "No object was selected")
    else:
        # get armature from objects selected
        armature_objects = [a for a in objects if a.type == "ARMATURE"]

        # pop up menu if no armature in object selected
        if len(armature_objects) == 0:
            self.report({"ERROR"}, "No armature in object selected")

        for arm in armature_objects:
            # force exit from EDIT/POSE modes
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="DESELECT")

            # make armature active object
            arm.select_set(True)
            bpy.context.view_layer.objects.active = arm
            any_rig_to_rigify_v3.the_script(arm, params)

# ===========================================================


def get_mapping_folder():
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "Any Rig to Rigify":
            filepath = mod.__file__
        else:
            pass
    filepath = filepath.replace("__init__.py", "")
    filepath = filepath.replace("\\", "/")
    mapping_folder = f"{filepath}/mapping_templates"
    # if os.path.isdir(mapping_folder) == False:
    #     make_dir_cmd = f"mkdir mapping_templates"
    #     os.system(make_dir_cmd)
    # path clean-up
    mapping_folder = mapping_folder.replace("\\", "/")
    mapping_folder = mapping_folder.replace("//", "/")

    return mapping_folder

# ===========================================================


def my_settings_callback(scene, context):
    # get to mapping_templates folder or create if there isn't one
    mapping_folder = get_mapping_folder()

    json_presets = []
    files = os.listdir(mapping_folder)
    # get only json files
    for file in files:
        _, file_extension = os.path.splitext(file)
        if file_extension == ".json":
            json_presets.append(file)

    items = []
    for i in json_presets:
        s = (i, i, "")
        items.append(s)

    return items

# ===========================================================


PROPS = [
    ("copy_loc_constr", BoolProperty(name="Stretch", default=True)),
    ("fingers_bool_r", BoolProperty(name="right fingers", default=True)),
    ("fingers_bool_l", BoolProperty(name="left fingers", default=True)),

    # # ===========================================================
    # mapping
    ("json_file_name", StringProperty(name="File Name", default="")),
    ("rename_preset", StringProperty(name="New Name", default="")),
    ("presets", EnumProperty(name="Presets", items=my_settings_callback)),


    # # ===========================================================
    # # ===========================================================
    # # ===========================================================
    # # random fbx
     ("head", StringProperty(name="head", default="head")),
     ("first_neck", StringProperty(name="1st neck", default="neck01")),
     ("last_neck", StringProperty(name="last neck", default="neck01")),

     ("spine", StringProperty(name="spine", default="spine05")),
     ("last_spine", StringProperty(name="last_spine", default="neck_01")),

     ("clav_l", StringProperty(name="clav_l", default="shoulder01.L")),
     ("clav_r", StringProperty(name="clav_r", default="shoulder01.R")),
     ("uparm_l", StringProperty(name="uparm_l", default="upperarm02.L")),
     ("uparm_r", StringProperty(name="uparm_l", default="upperarm02.R")),
     ("lowarm_l", StringProperty(name="lowarm_l", default="lowerarm02.L")),
     ("lowarm_r", StringProperty(name="lowarm_l", default="lowerarm02.R")),
     ("hand_l", StringProperty(name="hand_l", default="wrist.L")),
     ("hand_r", StringProperty(name="hand_r", default="wrist.R")),

     # fingers
     ("palm_pinky_r", StringProperty(name="palm_pinky_r", default="metacarpal4.R")),
     ("pinky_01_r", StringProperty(name="pinky_1_r", default="finger5-1.R")),
     ("pinky_02_r", StringProperty(name="pinky_2_r", default="finger5-2.R")),
     ("pinky_03_r", StringProperty(name="pinky_3_r", default="finger5-3.R")),
     ("palm_ring_r", StringProperty(name="palm_ring_r", default="metacarpal3.R")),
     ("ring_01_r", StringProperty(name="ring_1_r", default="finger4-1.R")),
     ("ring_02_r", StringProperty(name="ring_2_r", default="finger4-2.R")),
     ("ring_03_r", StringProperty(name="ring_3_r", default="finger4-3.R")),
     ("palm_middle_r", StringProperty(name="palm_middle_r", default="metacarpal2.R")),
     ("middle_01_r", StringProperty(name="middle_1_r", default="finger3-1.R")),
     ("middle_02_r", StringProperty(name="middle_2_r", default="finger3-2.R")),
     ("middle_03_r", StringProperty(name="middle_3_r", default="finger3-3.R")),
     ("palm_index_r", StringProperty(name="palm_index_r", default="metacarpal1.R")),
     ("index_01_r", StringProperty(name="index_1_r", default="finger2-1.R")),
     ("index_02_r", StringProperty(name="index_2_r", default="finger2-2.R")),
     ("index_03_r", StringProperty(name="index_3_r", default="finger2-3.R")),
     ("thumb_01_r", StringProperty(name="thumb_0_r", default="finger1-1.R")),
     ("thumb_02_r", StringProperty(name="thumb_2_r", default="finger1-2.R")),
     ("thumb_03_r", StringProperty(name="thumb_3_r", default="finger1-3.R")),
     # left fingers
     ("palm_pinky_l", StringProperty(name="palm_pinky_L", default="metacarpal4.L")),
     ("pinky_01_l", StringProperty(name="pinky_1_L", default="finger5-1.L")),
     ("pinky_02_l", StringProperty(name="pinky_2_L", default="finger5-2.L")),
     ("pinky_03_l", StringProperty(name="pinky_3_L", default="finger5-3.L")),
     ("palm_ring_l", StringProperty(name="palm_ring_L", default="metacarpal3.L")),
     ("ring_01_l", StringProperty(name="ring_1_L", default="finger4-1.L")),
     ("ring_02_l", StringProperty(name="ring_2_L", default="finger4-2.L")),
     ("ring_03_l", StringProperty(name="ring_3_L", default="finger4-3.L")),
     ("palm_middle_l", StringProperty(name="palm_middle_L", default="metacarpal2.L")),
     ("middle_01_l", StringProperty(name="middle_1_L", default="finger3-1.L")),
     ("middle_02_l", StringProperty(name="middle_2_L", default="finger3-2.L")),
     ("middle_03_l", StringProperty(name="middle_3_L", default="finger3-3.L")),
     ("palm_index_l", StringProperty(name="palm_index_L", default="metacarpal1.L")),
     ("index_01_l", StringProperty(name="index_1_L", default="finger2-1.L")),
     ("index_02_l", StringProperty(name="index_2_L", default="finger2-2.L")),
     ("index_03_l", StringProperty(name="index_3_L", default="finger2-3.L")),
     ("thumb_01_l", StringProperty(name="thumb_0_L", default="finger1-1.L")),
     ("thumb_02_l", StringProperty(name="thumb_2_L", default="finger1-2.L")),
     ("thumb_03_l", StringProperty(name="thumb_3_L", default="finger1-3.L")),

     # legs
     ("thigh_l", StringProperty(name="thigh_l", default="upperleg02.L")),
     ("thigh_r", StringProperty(name="thigh_r", default="upperleg02.R")),
     ("calf_l", StringProperty(name="calf_l", default="lowerleg01.L")),
     ("calf_r", StringProperty(name="calf_r", default="lowerleg01.R")),
     ("foot_l", StringProperty(name="foot_l", default="foot.L")),
     ("foot_r", StringProperty(name="foot_r", default="foot.R")),
     ("toe_l", StringProperty(name="toe_l", default="toe2-1.L")),
     ("toe_r", StringProperty(name="toe_r", default="toe2-1.R")),
     ("heel_r", StringProperty(name="heel_r", default="")),
     ("heel_l", StringProperty(name="heel_l", default="")),

     # ===========================================================
     # fortnite
     ("head", StringProperty(name="head", default="head")),
     ("first_neck", StringProperty(name="1st neck", default="neck_01")),
     ("last_neck", StringProperty(name="last neck", default="neck_01")),

     ("first_spine", StringProperty(name="1st spine", default="spine_01")),
     ("last_spine", StringProperty(name="last spine", default="spine_05")),

     ("clav_l", StringProperty(name="clav_l", default="clavicle_l")),
     ("clav_r", StringProperty(name="clav_r", default="clavicle_r")),
     ("uparm_l", StringProperty(name="uparm_l", default="upperarm_l")),
     ("uparm_r", StringProperty(name="uparm_l", default="upperarm_r")),
     ("lowarm_l", StringProperty(name="lowarm_l", default="lowerarm_l")),
     ("lowarm_r", StringProperty(name="lowarm_l", default="lowerarm_r")),
     ("hand_l", StringProperty(name="hand_l", default="hand_l")),
     ("hand_r", StringProperty(name="hand_r", default="hand_r")),

     # fingers
     ("palm_pinky_r", StringProperty(name="palm_pinky_r", default="pinky_metacarpal_r")),
     ("pinky_01_r", StringProperty(name="pinky_1_r", default="pinky_01_r")),
     ("pinky_02_r", StringProperty(name="pinky_2_r", default="pinky_02_r")),
     ("pinky_03_r", StringProperty(name="pinky_3_r", default="pinky_03_r")),
     ("palm_ring_r", StringProperty(name="palm_ring_r", default="ring_metacarpal_r")),
     ("ring_01_r", StringProperty(name="ring_1_r", default="ring_01_r")),
     ("ring_02_r", StringProperty(name="ring_2_r", default="ring_02_r")),
     ("ring_03_r", StringProperty(name="ring_3_r", default="ring_03_r")),
     ("palm_middle_r", StringProperty(
         name="palm_middle_r", default="middle_metacarpal_r")),
     ("middle_01_r", StringProperty(name="middle_1_r", default="middle_01_r")),
     ("middle_02_r", StringProperty(name="middle_2_r", default="middle_02_r")),
     ("middle_03_r", StringProperty(name="middle_3_r", default="middle_03_r")),
     ("palm_index_r", StringProperty(name="palm_index_r", default="index_metacarpal_r")),
     ("index_01_r", StringProperty(name="index_1_r", default="index_01_r")),
     ("index_02_r", StringProperty(name="index_2_r", default="index_02_r")),
     ("index_03_r", StringProperty(name="index_3_r", default="index_03_r")),
     ("thumb_01_r", StringProperty(name="thumb_0_r", default="thumb_01_r")),
     ("thumb_02_r", StringProperty(name="thumb_2_r", default="thumb_02_r")),
     ("thumb_03_r", StringProperty(name="thumb_3_r", default="thumb_03_r")),
     # left fingers
     ("palm_pinky_l", StringProperty(name="palm_pinky_l", default="pinky_metacarpal_l")),
     ("pinky_01_l", StringProperty(name="pinky_1_l", default="pinky_01_l")),
     ("pinky_02_l", StringProperty(name="pinky_2_l", default="pinky_02_l")),
     ("pinky_03_l", StringProperty(name="pinky_3_l", default="pinky_03_l")),
     ("palm_ring_l", StringProperty(name="palm_ring_l", default="ring_metacarpal_l")),
     ("ring_01_l", StringProperty(name="ring_1_l", default="ring_01_l")),
     ("ring_02_l", StringProperty(name="ring_2_l", default="ring_02_l")),
     ("ring_03_l", StringProperty(name="ring_3_l", default="ring_03_l")),
     ("palm_middle_l", StringProperty(
         name="palm_middle_l", default="middle_metacarpal_l")),
     ("middle_01_l", StringProperty(name="middle_1_l", default="middle_01_l")),
     ("middle_02_l", StringProperty(name="middle_2_l", default="middle_02_l")),
     ("middle_03_l", StringProperty(name="middle_3_l", default="middle_03_l")),
     ("palm_index_l", StringProperty(name="palm_index_l", default="index_metacarpal_l")),
     ("index_01_l", StringProperty(name="index_1_l", default="index_01_l")),
     ("index_02_l", StringProperty(name="index_2_l", default="index_02_l")),
     ("index_03_l", StringProperty(name="index_3_l", default="index_03_l")),
     ("thumb_01_l", StringProperty(name="thumb_0_l", default="thumb_01_l")),
     ("thumb_02_l", StringProperty(name="thumb_2_l", default="thumb_02_l")),
     ("thumb_03_l", StringProperty(name="thumb_3_l", default="thumb_03_l")),

     # legs
     ("thigh_l", StringProperty(name="thigh_l", default="thigh_l")),
     ("thigh_r", StringProperty(name="thigh_r", default="thigh_r")),
     ("calf_l", StringProperty(name="calf_l", default="calf_l")),
     ("calf_r", StringProperty(name="calf_r", default="calf_r")),
     ("foot_l", StringProperty(name="foot_l", default="foot_l")),
     ("foot_r", StringProperty(name="foot_r", default="foot_r")),
     ("toe_l", StringProperty(name="toe_l", default="ball_l")),
     ("toe_r", StringProperty(name="toe_r", default="ball_r")),
     ("heel_r", StringProperty(name="heel_r", default="")),
     ("heel_l", StringProperty(name="heel_l", default="")),

    # ===========================================================
    # mixamo
    ("head", StringProperty(name="Head", default="mixamorig:Head")),
    ("first_neck", StringProperty(name="1st Neck", default="mixamorig:Neck")),
    ("last_neck", StringProperty(name="Last Neck", default="mixamorig:Neck")),

    ("first_spine", StringProperty(name="Hips", default="mixamorig:Hips")),
    ("last_spine", StringProperty(name="Last Spine", default="mixamorig:Spine2")),

    ("clav_l", StringProperty(name="Clavicle Left", default="mixamorig:LeftShoulder")),
    ("clav_r", StringProperty(name="Clavicle Right", default="mixamorig:RightShoulder")),
    ("uparm_r", StringProperty(name="Upper Arm Right", default="mixamorig:RightArm")),
    ("uparm_l", StringProperty(name="Upper Arm Left", default="mixamorig:LeftArm")),
    ("lowarm_r", StringProperty(name="Forearm Right", default="mixamorig:RightForeArm")),
    ("lowarm_l", StringProperty(name="Forearm Left", default="mixamorig:LeftForeArm")),
    ("hand_r", StringProperty(name="Hand Right", default="mixamorig:RightHand")),
    ("hand_l", StringProperty(name="Hand Left", default="mixamorig:LeftHand")),

    # fingers
    ("palm_pinky_r", StringProperty(name="palm_pinky_r", default="")),
    ("pinky_01_r", StringProperty(name="pinky_1_r",
                                  default="mixamorig:RightHandPinky1")),
    ("pinky_02_r", StringProperty(name="pinky_2_r",
                                  default="mixamorig:RightHandPinky2")),
    ("pinky_03_r", StringProperty(name="pinky_3_r",
                                  default="mixamorig:RightHandPinky3")),
    ("palm_ring_r", StringProperty(name="palm_ring_r", default="")),
    ("ring_01_r", StringProperty(name="ring_1_r",
                                 default="mixamorig:RightHandRing1")),
    ("ring_02_r", StringProperty(name="ring_2_r",
                                 default="mixamorig:RightHandRing2")),
    ("ring_03_r", StringProperty(name="ring_3_r",
                                 default="mixamorig:RightHandRing3")),
    ("palm_middle_r", StringProperty(name="palm_middle_r", default="")),
    ("middle_01_r", StringProperty(name="middle_1_r",
                                   default="mixamorig:RightHandMiddle1")),
    ("middle_02_r", StringProperty(name="middle_2_r",
                                   default="mixamorig:RightHandMiddle2")),
    ("middle_03_r", StringProperty(name="middle_3_r",
                                   default="mixamorig:RightHandMiddle3")),
    ("palm_index_r", StringProperty(name="palm_index_r", default="")),
    ("index_01_r", StringProperty(name="index_1_r",
                                  default="mixamorig:RightHandIndex1")),
    ("index_02_r", StringProperty(name="index_2_r",
                                  default="mixamorig:RightHandIndex2")),
    ("index_03_r", StringProperty(name="index_3_r",
                                  default="mixamorig:RightHandIndex3")),
    ("thumb_01_r", StringProperty(name="thumb_1_r",
                                  default="mixamorig:RightHandThumb1")),
    ("thumb_02_r", StringProperty(name="thumb_2_r",
                                  default="mixamorig:RightHandThumb2")),
    ("thumb_03_r", StringProperty(name="thumb_3_r",
                                  default="mixamorig:RightHandThumb3")),
    # left fingers
    ("palm_pinky_l", StringProperty(name="palm_pinky_l", default="")),
    ("pinky_01_l", StringProperty(
        name="pinky_1_l", default="mixamorig:LeftHandPinky1")),
    ("pinky_02_l", StringProperty(
        name="pinky_2_l", default="mixamorig:LeftHandPinky2")),
    ("pinky_03_l", StringProperty(
        name="pinky_3_l", default="mixamorig:LeftHandPinky3")),
    ("palm_ring_l", StringProperty(name="palm_ring_l", default="")),
    ("ring_01_l", StringProperty(name="ring_1_l", default="mixamorig:LeftHandRing1")),
    ("ring_02_l", StringProperty(name="ring_2_l", default="mixamorig:LeftHandRing2")),
    ("ring_03_l", StringProperty(name="ring_3_l", default="mixamorig:LeftHandRing3")),
    ("palm_middle_l", StringProperty(name="palm_middle_l", default="")),
    ("middle_01_l", StringProperty(
        name="middle_1_l", default="mixamorig:LeftHandMiddle1")),
    ("middle_02_l", StringProperty(
        name="middle_2_l", default="mixamorig:LeftHandMiddle2")),
    ("middle_03_l", StringProperty(
        name="middle_3_l", default="mixamorig:LeftHandMiddle3")),
    ("palm_index_l", StringProperty(name="palm_index_l", default="")),
    ("index_01_l", StringProperty(
        name="index_1_l", default="mixamorig:LeftHandIndex1")),
    ("index_02_l", StringProperty(
        name="index_2_l", default="mixamorig:LeftHandIndex2")),
    ("index_03_l", StringProperty(
        name="index_3_l", default="mixamorig:LeftHandIndex3")),
    ("thumb_01_l", StringProperty(
        name="thumb_1_l", default="mixamorig:LeftHandThumb1")),
    ("thumb_02_l", StringProperty(
        name="thumb_2_l", default="mixamorig:LeftHandThumb2")),
    ("thumb_03_l", StringProperty(
        name="thumb_3_l", default="mixamorig:LeftHandThumb3")),

    # legs
    ("thigh_l", StringProperty(name="Up Leg Left", default="mixamorig:LeftUpLeg")),
    ("thigh_r", StringProperty(name="Up Leg Right", default="mixamorig:RightUpLeg")),
    ("calf_l", StringProperty(name="Leg Left", default="mixamorig:LeftLeg")),
    ("calf_r", StringProperty(name="Leg Right", default="mixamorig:RightLeg")),
    ("foot_l", StringProperty(name="Foot Left", default="mixamorig:LeftFoot")),
    ("foot_r", StringProperty(name="Foot Right", default="mixamorig:RightFoot")),
    ("toe_l", StringProperty(name="Toe Left", default="mixamorig:LeftToeBase")),
    ("toe_r", StringProperty(name="Toe Right", default="mixamorig:RightToeBase")),
    ("heel_r", StringProperty(name="Heel Right", default="")),
    ("heel_l", StringProperty(name="Heel Left", default="")),

    # # ===========================================================
    # # mv
    # ("head", StringProperty(name="head", default="Head")),
    # ("first_neck", StringProperty(name="1st neck", default="Neck_base")),
    # ("last_neck", StringProperty(name="last neck", default="Neck_base")),

    # ("first_spine", StringProperty(name="spine", default="Hips")),
    # ("last_spine", StringProperty(name="last_spine", default="")),

    # ("clav_l", StringProperty(name="clav_l", default="LeftShoulder")),
    # ("clav_r", StringProperty(name="clav_r", default="RightShoulder")),
    # ("uparm_r", StringProperty(name="uparm_r", default="RightArm")),
    # ("uparm_l", StringProperty(name="uparm_l", default="LeftArm")),
    # ("lowarm_r", StringProperty(name="lowarm_r", default="RightForeArm")),
    # ("lowarm_l", StringProperty(name="lowarm_l", default="LeftForeArm")),
    # ("hand_r", StringProperty(name="hand_r", default="RightHand")),
    # ("hand_l", StringProperty(name="hand_l", default="LeftHand")),

    # # fingers
    # ("palm_pinky_r", StringProperty(name="palm_pinky_r", default="")),
    # ("pinky_01_r", StringProperty(name="pinky_1_r", default="RightHandPinky1")),
    # ("pinky_02_r", StringProperty(name="pinky_2_r", default="RightHandPinky2")),
    # ("pinky_03_r", StringProperty(name="pinky_3_r", default="RightHandPinky3")),
    # ("palm_ring_r", StringProperty(name="palm_ring_r", default="")),
    # ("ring_01_r", StringProperty(name="ring_1_r", default="RightHandRing1")),
    # ("ring_02_r", StringProperty(name="ring_2_r", default="RightHandRing2")),
    # ("ring_03_r", StringProperty(name="ring_3_r", default="RightHandRing3")),
    # ("palm_middle_r", StringProperty(name="palm_middle_r", default="")),
    # ("middle_01_r", StringProperty(name="middle_1_r", default="RightHandMiddle1")),
    # ("middle_02_r", StringProperty(name="middle_2_r", default="RightHandMiddle2")),
    # ("middle_03_r", StringProperty(name="middle_3_r", default="RightHandMiddle3")),
    # ("palm_index_r", StringProperty(name="palm_index_r", default="")),
    # ("index_01_r", StringProperty(name="index_1_r", default="RightHandIndex1")),
    # ("index_02_r", StringProperty(name="index_2_r", default="RightHandIndex2")),
    # ("index_03_r", StringProperty(name="index_3_r", default="RightHandIndex3")),
    # ("thumb_01_r", StringProperty(name="thumb_1_r", default="RightHandThumb1")),
    # ("thumb_02_r", StringProperty(name="thumb_2_r", default="RightHandThumb2")),
    # ("thumb_03_r", StringProperty(name="thumb_3_r", default="RightHandThumb3")),
    # # left fingers
    # ("palm_pinky_l", StringProperty(name="palm_pinky_l", default="")),
    # ("pinky_01_l", StringProperty(name="pinky_1_l", default="LeftHandPinky1")),
    # ("pinky_02_l", StringProperty(name="pinky_2_l", default="LeftHandPinky2")),
    # ("pinky_03_l", StringProperty(name="pinky_3_l", default="LeftHandPinky3")),
    # ("palm_ring_l", StringProperty(name="palm_ring_l", default="")),
    # ("ring_01_l", StringProperty(name="ring_1_l", default="LeftHandRing1")),
    # ("ring_02_l", StringProperty(name="ring_2_l", default="LeftHandRing2")),
    # ("ring_03_l", StringProperty(name="ring_3_l", default="LeftHandRing3")),
    # ("palm_middle_l", StringProperty(name="palm_middle_l", default="")),
    # ("middle_01_l", StringProperty(name="middle_1_l", default="LeftHandMiddle1")),
    # ("middle_02_l", StringProperty(name="middle_2_l", default="LeftHandMiddle2")),
    # ("middle_03_l", StringProperty(name="middle_3_l", default="LeftHandMiddle3")),
    # ("palm_index_l", StringProperty(name="palm_index_l", default="")),
    # ("index_01_l", StringProperty(name="index_1_l", default="LeftHandIndex1")),
    # ("index_02_l", StringProperty(name="index_2_l", default="LeftHandIndex2")),
    # ("index_03_l", StringProperty(name="index_3_l", default="LeftHandIndex3")),
    # ("thumb_01_l", StringProperty(name="thumb_1_l", default="LeftHandThumb1")),
    # ("thumb_02_l", StringProperty(name="thumb_2_l", default="LeftHandThumb2")),
    # ("thumb_03_l", StringProperty(name="thumb_3_l", default="LeftHandThumb3")),

    # # legs
    # ("thigh_l", StringProperty(name="thigh_l", default="LeftUpLeg")),
    # ("thigh_r", StringProperty(name="thigh_r", default="RightUpLeg")),
    # ("calf_l", StringProperty(name="calf_l", default="LeftLeg")),
    # ("calf_r", StringProperty(name="calf_r", default="RightLeg")),
    # ("foot_l", StringProperty(name="foot_l", default="LeftFoot")),
    # ("foot_r", StringProperty(name="foot_r", default="RightFoot")),
    # ("toe_l", StringProperty(name="toe_l", default="LeftToeBase")),
    # ("toe_r", StringProperty(name="toe_r", default="RightToeBase")),
    # ("heel_r", StringProperty(name="heel_r", default="")),
    # ("heel_l", StringProperty(name="heel_l", default="")),
]


# ===========================================================


class MappingSaveOperator(Operator):

    bl_idname = "opr.mapping_save_operator"
    bl_label = "mapping_templates"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        prop_dict = {
            "head": context.scene.head,
            "first_neck": context.scene.first_neck,
            "last_neck": context.scene.last_neck,
            "first_spine": context.scene.first_spine,
            "last_spine": context.scene.last_spine,
            "clav_l": context.scene.clav_l,
            "clav_r": context.scene.clav_r,
            "uparm_r": context.scene.uparm_r,
            "uparm_l": context.scene.uparm_l,
            "lowarm_r": context.scene.lowarm_r,
            "lowarm_l": context.scene.lowarm_l,
            "hand_r": context.scene.hand_r,
            "hand_l": context.scene.hand_l,
            "palm_pinky_r": context.scene.palm_pinky_r,
            "pinky_01_r": context.scene.pinky_01_r,
            "pinky_02_r": context.scene.pinky_02_r,
            "pinky_03_r": context.scene.pinky_03_r,
            "palm_ring_r": context.scene.palm_ring_r,
            "ring_01_r": context.scene.ring_01_r,
            "ring_02_r": context.scene.ring_02_r,
            "ring_03_r": context.scene.ring_03_r,
            "palm_middle_r": context.scene.palm_middle_r,
            "middle_01_r": context.scene.middle_01_r,
            "middle_02_r": context.scene.middle_02_r,
            "middle_03_r": context.scene.middle_03_r,
            "palm_index_r": context.scene.palm_index_r,
            "index_01_r": context.scene.index_01_r,
            "index_02_r": context.scene.index_02_r,
            "index_03_r": context.scene.index_03_r,
            "thumb_01_r": context.scene.thumb_01_r,
            "thumb_02_r": context.scene.thumb_02_r,
            "thumb_03_r": context.scene.thumb_03_r,
            "palm_pinky_l": context.scene.palm_pinky_l,
            "pinky_01_l": context.scene.pinky_01_l,
            "pinky_02_l": context.scene.pinky_02_l,
            "pinky_03_l": context.scene.pinky_03_l,
            "palm_ring_l": context.scene.palm_ring_l,
            "ring_01_l": context.scene.ring_01_l,
            "ring_02_l": context.scene.ring_02_l,
            "ring_03_l": context.scene.ring_03_l,
            "palm_middle_l": context.scene.palm_middle_l,
            "middle_01_l": context.scene.middle_01_l,
            "middle_02_l": context.scene.middle_02_l,
            "middle_03_l": context.scene.middle_03_l,
            "palm_index_l": context.scene.palm_index_l,
            "index_01_l": context.scene.index_01_l,
            "index_02_l": context.scene.index_02_l,
            "index_03_l": context.scene.index_03_l,
            "thumb_01_l": context.scene.thumb_01_l,
            "thumb_02_l": context.scene.thumb_02_l,
            "thumb_03_l": context.scene.thumb_03_l,
            "thigh_l": context.scene.thigh_l,
            "thigh_r": context.scene.thigh_r,
            "calf_l": context.scene.calf_l,
            "calf_r": context.scene.calf_r,
            "foot_l": context.scene.foot_l,
            "foot_r": context.scene.foot_r,
            "toe_l": context.scene.toe_l,
            "toe_r": context.scene.toe_r,
            "heel_r": context.scene.heel_r,
            "heel_l": context.scene.heel_l,
        }

        # ===========================================================
        mapping_folder = get_mapping_folder()

        # ===========================================================
        # Serializing json
        json_object = json.dumps(prop_dict, indent=4)

        if context.scene.json_file_name != "":
            context.scene.json_file_name = context.scene.json_file_name.replace(
                ".json", "")
            json_file_name = f"{context.scene.json_file_name}.json"
            json_path = f"{mapping_folder}/{json_file_name}"

            # Writing to sample.json
            with open(json_path, "w") as outfile:
                outfile.write(json_object)
            context.scene.json_file_name = ""
            self.report({"INFO"}, f"{context.scene.presets} preset saved")
        else:
            self.report({"ERROR"}, "Enter preset name fist")

        return {"FINISHED"}

# ===========================================================


class MappingImportOperator(Operator):

    bl_idname = "opr.mapping_import_operator"
    bl_label = "mapping_templates_import"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        json_file = f"{get_mapping_folder()}/{context.scene.presets}"
        # Opening JSON file
        with open(json_file) as json_file:
            data = json.load(json_file)

        context.scene.head = data["head"]
        context.scene.first_neck = data["first_neck"]
        context.scene.last_neck = data["last_neck"]
        context.scene.first_spine = data["first_spine"]
        context.scene.last_spine = data["last_spine"]
        context.scene.clav_l = data["clav_l"]
        context.scene.clav_r = data["clav_r"]
        context.scene.uparm_r = data["uparm_r"]
        context.scene.uparm_l = data["uparm_l"]
        context.scene.lowarm_r = data["lowarm_r"]
        context.scene.lowarm_l = data["lowarm_l"]
        context.scene.hand_r = data["hand_r"]
        context.scene.hand_l = data["hand_l"]
        context.scene.palm_pinky_r = data["palm_pinky_r"]
        context.scene.pinky_01_r = data["pinky_01_r"]
        context.scene.pinky_02_r = data["pinky_02_r"]
        context.scene.pinky_03_r = data["pinky_03_r"]
        context.scene.palm_ring_r = data["palm_ring_r"]
        context.scene.ring_01_r = data["ring_01_r"]
        context.scene.ring_02_r = data["ring_02_r"]
        context.scene.ring_03_r = data["ring_03_r"]
        context.scene.palm_middle_r = data["palm_middle_r"]
        context.scene.middle_01_r = data["middle_01_r"]
        context.scene.middle_02_r = data["middle_02_r"]
        context.scene.middle_03_r = data["middle_03_r"]
        context.scene.palm_index_r = data["palm_index_r"]
        context.scene.index_01_r = data["index_01_r"]
        context.scene.index_02_r = data["index_02_r"]
        context.scene.index_03_r = data["index_03_r"]
        context.scene.thumb_01_r = data["thumb_01_r"]
        context.scene.thumb_02_r = data["thumb_02_r"]
        context.scene.thumb_03_r = data["thumb_03_r"]
        context.scene.palm_pinky_l = data["palm_pinky_l"]
        context.scene.pinky_01_l = data["pinky_01_l"]
        context.scene.pinky_02_l = data["pinky_02_l"]
        context.scene.pinky_03_l = data["pinky_03_l"]
        context.scene.palm_ring_l = data["palm_ring_l"]
        context.scene.ring_01_l = data["ring_01_l"]
        context.scene.ring_02_l = data["ring_02_l"]
        context.scene.ring_03_l = data["ring_03_l"]
        context.scene.palm_middle_l = data["palm_middle_l"]
        context.scene.middle_01_l = data["middle_01_l"]
        context.scene.middle_02_l = data["middle_02_l"]
        context.scene.middle_03_l = data["middle_03_l"]
        context.scene.palm_index_l = data["palm_index_l"]
        context.scene.index_01_l = data["index_01_l"]
        context.scene.index_02_l = data["index_02_l"]
        context.scene.index_03_l = data["index_03_l"]
        context.scene.thumb_01_l = data["thumb_01_l"]
        context.scene.thumb_02_l = data["thumb_02_l"]
        context.scene.thumb_03_l = data["thumb_03_l"]
        context.scene.thigh_l = data["thigh_l"]
        context.scene.thigh_r = data["thigh_r"]
        context.scene.calf_l = data["calf_l"]
        context.scene.calf_r = data["calf_r"]
        context.scene.foot_l = data["foot_l"]
        context.scene.foot_r = data["foot_r"]
        context.scene.toe_l = data["toe_l"]
        context.scene.toe_r = data["toe_r"]
        context.scene.heel_r = data["heel_r"]
        context.scene.heel_l = data["heel_l"]

        self.report({"INFO"}, f"{context.scene.presets} preset imported")
        return {"FINISHED"}

# ===========================================================


class MappingDeleteOperator(Operator):

    bl_idname = "opr.mapping_delete_operator"
    bl_label = "mapping_templates_delete"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        json_file = f"{get_mapping_folder()}/{context.scene.presets}"
        print(json_file)
        protected_files = [
            "fortnite.json",
            "mixamo.json",
        ]
        if context.scene.presets not in protected_files:
            delete_preset = context.scene.presets
            os.remove(json_file)
            self.report({"INFO"}, f"{delete_preset} reset was deleted")
        else:
            self.report(
                {"ERROR"}, f"{context.scene.presets} is restricted file")

        return {"FINISHED"}


# ===========================================================


class MappingRenameOperator(Operator):

    bl_idname = "opr.mapping_rename_operator"
    bl_label = "mapping_templates_rename"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        json_file = f"{get_mapping_folder()}/{context.scene.presets}"
        protected_files = [
            "fortnite.json",
            "mixamo.json",
        ]

        old_file_name = context.scene.presets
        if context.scene.presets not in protected_files:
            new_name = f"{context.scene.rename_preset}.json"
            new_file_name = json_file.replace(context.scene.presets, new_name)
            os.rename(json_file, new_file_name)
            self.report(
                {"INFO"}, f"{old_file_name} renamed to {context.scene.presets}")
            context.scene.rename_preset = ""
        else:
            self.report(
                {"ERROR"}, f"{context.scene.presets} is restricted file")

        return {"FINISHED"}


# ===========================================================


class ObjectOperator(Operator):

    bl_idname = "opr.object_operator"
    bl_label = "Any Rig to Rigify"
    bl_options = {"UNDO"}

    def execute(self, context):
        params = {
            "head": context.scene.head,
            "first_neck": context.scene.first_neck,
            "last_neck": context.scene.last_neck,
            "first_spine": context.scene.first_spine,
            "last_spine": context.scene.last_spine,
            "clav_r": context.scene.clav_r,
            "clav_l": context.scene.clav_l,
            "uparm_l": context.scene.uparm_l,
            "uparm_r": context.scene.uparm_r,
            "lowarm_l": context.scene.lowarm_l,
            "lowarm_r": context.scene.lowarm_r,
            "hand_l": context.scene.hand_l,
            "hand_r": context.scene.hand_r,

            "palm_pinky_r": context.scene.palm_pinky_r,
            "pinky_01_r": context.scene.pinky_01_r,
            "pinky_02_r": context.scene.pinky_02_r,
            "pinky_03_r": context.scene.pinky_03_r,
            "palm_ring_r": context.scene.palm_ring_r,
            "ring_01_r": context.scene.ring_01_r,
            "ring_02_r": context.scene.ring_02_r,
            "ring_03_r": context.scene.ring_03_r,
            "palm_middle_r": context.scene.palm_middle_r,
            "middle_01_r": context.scene.middle_01_r,
            "middle_02_r": context.scene.middle_02_r,
            "middle_03_r": context.scene.middle_03_r,
            "palm_index_r": context.scene.palm_index_r,
            "index_01_r": context.scene.index_01_r,
            "index_02_r": context.scene.index_02_r,
            "index_03_r": context.scene.index_03_r,
            "thumb_01_r": context.scene.thumb_01_r,
            "thumb_02_r": context.scene.thumb_02_r,
            "thumb_03_r": context.scene.thumb_03_r,

            "palm_pinky_l": context.scene.palm_pinky_l,
            "pinky_01_l": context.scene.pinky_01_l,
            "pinky_02_l": context.scene.pinky_02_l,
            "pinky_03_l": context.scene.pinky_03_l,
            "palm_ring_l": context.scene.palm_ring_l,
            "ring_01_l": context.scene.ring_01_l,
            "ring_02_l": context.scene.ring_02_l,
            "ring_03_l": context.scene.ring_03_l,
            "palm_middle_l": context.scene.palm_middle_l,
            "middle_01_l": context.scene.middle_01_l,
            "middle_02_l": context.scene.middle_02_l,
            "middle_03_l": context.scene.middle_03_l,
            "palm_index_l": context.scene.palm_index_l,
            "index_01_l": context.scene.index_01_l,
            "index_02_l": context.scene.index_02_l,
            "index_03_l": context.scene.index_03_l,
            "thumb_01_l": context.scene.thumb_01_l,
            "thumb_02_l": context.scene.thumb_02_l,
            "thumb_03_l": context.scene.thumb_03_l,
            "thigh_l": context.scene.thigh_l,
            "thigh_r": context.scene.thigh_r,
            "calf_l": context.scene.calf_l,
            "calf_r": context.scene.calf_r,
            "foot_l": context.scene.foot_l,
            "foot_r": context.scene.foot_r,
            "toe_l": context.scene.toe_l,
            "toe_r": context.scene.toe_r,
            "heel_l": context.scene.heel_l,
            "heel_r": context.scene.heel_r,

            "fingers_bool_r": context.scene.fingers_bool_r,
            "fingers_bool_l": context.scene.fingers_bool_l,
            "copy_loc_constr": context.scene.copy_loc_constr,
        }

        objects = bpy.context.selected_objects
        generate_rig(self, objects, params)

        return {"FINISHED"}


# ===========================================================


class GENERATE_panel(bpy.types.Panel):
    bl_idname = "GENERATE_PT_panel"
    bl_label = "Generate"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_OPENED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        box = self.layout.box()
        box.label(text="Generate")
        box.operator("opr.object_operator", text="Generate Rigify")
        box.prop(scn, "copy_loc_constr")


# ===========================================================

class MAPPING_panel(bpy.types.Panel):
    bl_idname = "MAPPING_PT_panel"
    bl_label = "Mapping"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        # row = layout.row()
        # icon = 'TRIA_DOWN' if scn.subpanel_status_upper else 'TRIA_RIGHT'
        # row.prop(scn, 'subpanel_status_mapping', icon=icon, icon_only=True)
        # row.label(text='Mapping')
        # if scn.subpanel_status_mapping:

        box = layout.box()
        box.label(text="save mapping")

        box.prop(scn, "json_file_name")
        box.operator("opr.mapping_save_operator", text="save mapping")

        box = layout.box()
        box.label(text="import presets")
        box.prop(scn, "presets")
        box.operator("opr.mapping_import_operator", text="import mapping")

        box = layout.box()
        box.label(text="delete active preset")
        box.operator("opr.mapping_delete_operator",
                     text=f"delete {scn.presets}")

        box = layout.box()
        box.label(text="rename active reset")
        box.prop(scn, "rename_preset")
        box.operator("opr.mapping_rename_operator", text="rename preset")


# ===========================================================


class UPPER_BODY_panel(bpy.types.Panel):
    bl_idname = "UPPER_BODY_PT_panel"
    bl_label = "Upper body"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        box = layout.box()
        box.prop(scn, "head")
        box.prop(scn, "first_neck")
        box.prop(scn, "last_neck")
        box.prop(scn, "clav_r")
        box.prop(scn, "clav_l")
# ===========================================================


class SPINES_panel(bpy.types.Panel):
    bl_idname = "SPINES_PT_panel"
    bl_label = "Spines"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        # Spines
        row = layout.row()
        row.label(text='Spines')

        box = layout.box()
        box.prop(scn, "first_spine")
        box.prop(scn, "last_spine")

# ===========================================================


class ARMS_panel(bpy.types.Panel):
    bl_idname = "ARMS_PT_panel"
    bl_label = "Arms"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        box = layout.box()

        box.prop(scn, "uparm_r")
        box.prop(scn, "lowarm_r")
        box.prop(scn, "hand_r")
        box.prop(scn, "uparm_l")
        box.prop(scn, "lowarm_l")
        box.prop(scn, "hand_l")


# ===========================================================


class FINGERS_panel(bpy.types.Panel):
    bl_idname = "FINGERS_PT_panel"
    bl_label = "Fingers"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        # right fingers
        box = layout.box()
        box.prop(scn, "fingers_bool_r")
        if scn.fingers_bool_r == True:
            box.prop(scn, "thumb_01_r")
            box.prop(scn, "thumb_02_r")
            box.prop(scn, "thumb_03_r")
            box.prop(scn, "palm_index_r")
            box.prop(scn, "index_01_r")
            box.prop(scn, "index_02_r")
            box.prop(scn, "index_03_r")
            box.prop(scn, "palm_middle_r")
            box.prop(scn, "middle_01_r")
            box.prop(scn, "middle_02_r")
            box.prop(scn, "middle_03_r")
            box.prop(scn, "palm_ring_r")
            box.prop(scn, "ring_01_r")
            box.prop(scn, "ring_02_r")
            box.prop(scn, "ring_03_r")
            box.prop(scn, "palm_pinky_r")
            box.prop(scn, "pinky_01_r")
            box.prop(scn, "pinky_02_r")
            box.prop(scn, "pinky_03_r")


        # left fingers
        box.prop(scn, "fingers_bool_l")
        if scn.fingers_bool_l == True:
            box.prop(scn, "thumb_01_l")
            box.prop(scn, "thumb_02_l")
            box.prop(scn, "thumb_03_l")
            box.prop(scn, "palm_index_l")
            box.prop(scn, "index_01_l")
            box.prop(scn, "index_02_l")
            box.prop(scn, "index_03_l")
            box.prop(scn, "palm_middle_l")
            box.prop(scn, "middle_01_l")
            box.prop(scn, "middle_02_l")
            box.prop(scn, "middle_03_l")
            box.prop(scn, "palm_ring_l")
            box.prop(scn, "ring_01_l")
            box.prop(scn, "ring_02_l")
            box.prop(scn, "ring_03_l")
            box.prop(scn, "palm_pinky_l")
            box.prop(scn, "pinky_01_l")
            box.prop(scn, "pinky_02_l")
            box.prop(scn, "pinky_03_l")

# ===========================================================


class LEGS_panel(bpy.types.Panel):
    bl_idname = "LEGS_PT_panel"
    bl_label = "Legs"
    bl_category = "Any Rig to Rigify"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        box = layout.box()

        box.prop(scn, "thigh_r")
        box.prop(scn, "calf_r")
        box.prop(scn, "foot_r")
        box.prop(scn, "toe_r")
        box.prop(scn, "heel_r")
        box.prop(scn, "thigh_l")
        box.prop(scn, "calf_l")
        box.prop(scn, "foot_l")
        box.prop(scn, "toe_l")
        box.prop(scn, "heel_l")
