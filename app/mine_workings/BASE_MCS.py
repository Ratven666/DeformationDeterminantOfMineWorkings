from app.base.Arc2D import Arc2D
from app.base.Line import Line
from app.base.Point import Point
from app.mine_workings.MineCrossSection import MineCrossSection

MCS = MineCrossSection(Point(0, 0, 0),
                       Line(start_point=Point(x=2.1, y=0, z=0),
                            end_point=Point(x=2.1, y=0.7, z=0)),
                       Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=1.004,
                                                                                                       y=0.7),
                                                                                    start_point=Point(x=2.1, y=0.7,
                                                                                                      z=0),
                                                                                    end_point=Point(x=1.7044, y=1.5477,
                                                                                                    z=0)),
                       Arc2D.create_arc_from_center_point_with_start_and_end_points(
                           center_point=Point(x=0, y=-0.806, z=0),
                           start_point=Point(x=1.7044, y=1.5477, z=0),
                           end_point=Point(x=0, y=2.1)),
                       Arc2D.create_arc_from_center_point_with_start_and_end_points(
                           center_point=Point(x=0, y=-0.806, z=0),
                           start_point=Point(x=0, y=2.1),
                           end_point=Point(x=-1.7044, y=1.5477, z=0)),
                       Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=-1.004,
                                                                                                       y=0.7),
                                                                                    start_point=Point(x=-1.7044,
                                                                                                      y=1.5477, z=0),
                                                                                    end_point=Point(x=-2.1, y=0.7)),
                       Line(start_point=Point(x=-2.1, y=0.7),
                            end_point=Point(x=-2.1, y=-2.1)),
                       Line(start_point=Point(x=-2.1, y=-2.1),
                            end_point=Point(x=2.1, y=-2.1)),
                       Line(start_point=Point(x=2.1, y=-2.1),
                            end_point=Point(x=2.1, y=0)))
