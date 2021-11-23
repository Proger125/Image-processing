from point import Point


class Cutter(object):
    def __init__(self, left_up_point, right_down_point):
        self.left_up_point = left_up_point
        self.right_down_point = right_down_point
