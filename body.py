'''
body.py
Created: Saturday, 8th October 2022 2:45:05 pm
Matthew Riche
Last Modified: Saturday, 8th October 2022 3:05:28 pm
Modified By: Matthew Riche
'''

import maya.cmds as cmds
from . import rmodule

class Limb(rmodule.RMod):

    def __init__(self):
        """Constructor for generic limb
        """        
        super().__init__()

        # The contents of self plan nested tuples with (name[0], worldspace position[1], parent[2],
        # colour[3], size[4])
        self.plan = (
            ('base', (0.0, 0.0, 0.0), '', 17, 1.0),
            ('middle', (0.0, 17.0, 0.0), '', 17, 1.0),
            ('end', (0.0, 35.0, 0.0), '', 17, 1.0)
        )

    def build_module(self):
        super().build_module()

        # Make a string of joints
        for piece in self.plan:
            build_loc = cmds.ls(piece[0])[0]
            if(cmds.objectType(build_loc) != 'transform'): # TODO Check the shape node instead of the trans
                raise TypeError (
                    "The string found in the plan '{}' is not a transform.".format(piece[0]))
            if(len(cmds.ls(piece[0])) == 1):
                new_joint = cmds.joint(n=(piece[0] + '_jnt'))
                cmds.matchTransform(new_joint, build_loc)

        

                
        


