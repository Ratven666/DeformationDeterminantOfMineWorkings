from abc import ABC, abstractmethod

from app.base.Point import Point


class Geometry(ABC):

    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point

    @abstractmethod
    def get_distance_from_obj_to_point(self, point: Point, get_abs_value=True):
        pass

    @abstractmethod
    def get_closest_point_obj(self, point: Point):
        pass

    @abstractmethod
    def is_point_on_obj(self, point: Point):
        pass

    @abstractmethod
    def get_point_on_obj_at_distance(self, distance):
        pass

    @abstractmethod
    def get_distance_from_start_point_to_point(self, point: Point):
        pass

    @abstractmethod
    def is_point_left_of_obj(self, point: Point):
        pass

    @abstractmethod
    def get_points_on_obj(self, num_points=10):
        pass
