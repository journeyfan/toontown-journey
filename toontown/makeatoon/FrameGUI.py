from direct.gui.DirectGui import *
from .MakeAToonGlobals import *


class ChoiceFrame:

    def __init__(self, parent, image_scale, images, pos, hpr, scale, text, text_scale, text_pos, button_command):
        self.choice_box = DirectFrame(parent=parent, image=images[0], pos=pos, image_scale=image_scale,
                                      relief=None, hpr=hpr, scale=scale, text=text, text_scale=text_scale,
                                      text_pos=text_pos, text_fg=(1, 1, 1, 1))

        self.left_arrow = DirectButton(parent=self.choice_box, relief=None, image=images[1],
                                       image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, extraArgs=[-1],
                                       image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=button_command)
        self.right_arrow = DirectButton(parent=self.choice_box, relief=None, image=images[1],
                                        image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale,
                                        extraArgs=[1], image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0),
                                        command=button_command)

    def destroy(self):
        self.choice_box.destroy()
        self.left_arrow.destroy()
        self.right_arrow.destroy()
        del self.choice_box
        del self.left_arrow
        del self.right_arrow
