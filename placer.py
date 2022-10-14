
import maya.cmds as cmds

from .hard_data import PLACER_CURVE_DATA as PCD

import logging as log

LINE_WIDTH = 15.0 # The thickness of nurbsCurve lines (nurbsCurveShape.lineWidth) on placers.

class Placer:
    def __init__(
        self, pos=(0, 0, 0), colour=17, scale=1.0, name='new_dr_placer', mirror_target=None):
        """Constructor for a placer node-- a nurbsCurve known to a rmodule that lets artists define
        the position of build-pieces by moving this transform.

        Args:
            pos (tuple, optional): Moves the created transform to this euler position. 
                Defaults to (0, 0, 0).
            colour (int, optional): Override colour index to be applied. Defaults to 17 (yellow)
            scale (float, optional): Size the transform will be scaled to (before freezing). 
                Defaults to 1.0.
            name (str, optional): The in-scene name of the placer. Defaults to 'new_dr_placer'.
            mirror_target (str, optional): The in-scene name of which placer this mirrors. 
                Defaults to None.

        Raises:
            ValueError: If colour is higher than Maya's indexed colours allow for.
            ValueError: If the scale is negative.
        """   

        if(mirror_target):
            raise NotImplementedError("mirror_target property not implemented.")

        if(colour > 31):
            raise ValueError ("colour can't be higher than 31, as Maya's colour indices end at 31")
        if(scale < 0):
            raise ValueError ("Can't make a placer with a negative scale.")   

        log.debug("Creating the placer \'{}\'.".format(name))

        self.pos = pos
        self.colour = colour
        self.scale = scale
        self.name = name

        # Prep the nodes as nothing before creation.
        self.curve_node = None
        self.curve_shape = None
        # Build it right away.
        self.create()

    def create(self):
        """Build the pre-defined hard-date "ball" shaped nurbsCurve and restore reference to it in 
        this instance.

        Raises:
            AssertionError: If Maya fails to build a nurbsCurve.
            TypeError: If the resulting transnode somehow doesn't have a shapeNode.
        """        

        self.curve_node = cmds.curve(
            per = False,
            p = PCD['pos_vectors'],
            k = PCD['knots'],
            d = PCD['degree'], 
            n = self.name
        )
        if(self.curve_node == None):
            raise AssertionError("A curveNode wasn't ever created.")
        self.curve_shape = cmds.listRelatives(self.curve_node, shapes=True)[0]
        if(self.curve_shape == None):
            raise TypeError("{} didn't have a shape node beneath it.".format(self.curve_node))
        if(PCD['form'] > 0):
            cmds.closeCurve(self.curve_shape, ch=False, rpo=True)
        cmds.setAttr(self.curve_shape + '.overrideEnabled', 1)
        cmds.setAttr(self.curve_shape + '.overrideColor', self.colour)
        cmds.setAttr(self.curve_shape + '.lineWidth', LINE_WIDTH)
        cmds.scale(self.scale, self.scale, self.scale, self.curve_node)
        # Freeze the new scale before moving it.
        cmds.makeIdentity(self.curve_node, apply=True)
        # Now move it.
        cmds.move(self.pos[0], self.pos[1], self.pos[2], self.curve_node)

    def __str__(self):
        return(self.name)