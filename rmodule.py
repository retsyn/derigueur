'''
rmodule.py
Created: Saturday, 8th October 2022 2:11:59 pm
Matthew Riche
Last Modified: Saturday, 8th October 2022 2:12:17 pm
Modified By: Matthew Riche
'''

# Basic module class that will create placers on the first phase, and use those points in space 
# to guide automated builds.

import maya.cmds as cmds
import logging as log
from . import placer as plc

log.basicConfig(level=log.DEBUG)


class RMod:
    def __init__(self, name="Generic RModule", side_enum=1):
        """Constructore for RModule.

        Args:
            name (str, optional): Name of the module. Defaults to "Generic RModule".
            side_enum (int, optional): Enum value for 0,1,2:left,right,centre. Defaults to 1.
        """        
        self.name = name
        self.side_enum = side_enum

        self.plan = () # All required placers for the module.
        # The contents of self plan nested tuples with (name[0], worldspace position[1], parent[2],
        # colour[3], size[4])
        self.placers = [] # Where the actual created locator node names go.

    def create_placers(self):
        """Puts locator nodes into the scene according to the plan data.
        """        

        # Build each piece of the plan as a locator in the maya scene.
        for piece in self.plan:
            log.debug("plan piece data is {}".format(piece))
            print("plan piece data is {}".format(piece))
            new_plc = plc.Placer(name=piece[0], pos=piece[1], scale=piece[4])
            self.placers.append(new_plc.curve_node)

    def build_module(self):
        """Parent class of the actual build structure.
        """        

        log.info(
            "Building module {}, containing {} components".format(self.name, len(self.placers)))




















