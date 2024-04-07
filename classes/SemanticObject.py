''' 
    This class provides transmitting pixel pairs via udp connection
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

from enum import Enum



class SemanticObject():
    def __init__(self, x, y, h = 0, w = 0, object_id = 0):
        #constants
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.object_id = object_id

    def to_list(self):
        res = [self.x, self.y, self.h, self.w, self.object_id]
        return res
    