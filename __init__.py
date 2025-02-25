# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Any Rig to Rigify",
    "author": "demania",
    "description": "This Addon Is Not Made By Me And I Do Not Claim Ownership Of The Addon. I'm Just Supporting This With Updates For Blender 4+ All Credits Goes To It's Respected Owner.",
    "blender": (3, 0, 0),
    "version": (0, 0, 3),
    "location": "View3D",
    "warning": "",
    "category": "Object",
}

from . import ui
from .ui import (
    # CustomPanel,
    ObjectOperator,
    MappingSaveOperator,
    MappingImportOperator,
    MappingDeleteOperator,
    MappingRenameOperator,
    GENERATE_panel,
    MAPPING_panel,
    UPPER_BODY_panel,
    SPINES_panel,
    ARMS_panel,
    FINGERS_panel,
    LEGS_panel,
)
import bpy

# ===========================================================


classes = [
    # CustomPanel,
    ObjectOperator,
    MappingSaveOperator,
    MappingImportOperator,
    MappingDeleteOperator,
    MappingRenameOperator,
    GENERATE_panel,
    MAPPING_panel,
    UPPER_BODY_panel,
    SPINES_panel,
    ARMS_panel,
    FINGERS_panel,
    LEGS_panel,
]


def register():
    for (prop_name, prop_value) in ui.PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for c in classes:
        try:
            bpy.utils.unregister_class(c)  # Unregister first if already registered
        except RuntimeError:
            pass  # Ignore if not registered
        bpy.utils.register_class(c)



def unregister():
    for (prop_name, _) in ui.PROPS:
        if hasattr(bpy.types.Scene, prop_name):  # Check if the property exists
            delattr(bpy.types.Scene, prop_name)

    for c in reversed(classes):  # Reverse order to avoid dependency issues
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass  # Ignore errors if already unregistered
