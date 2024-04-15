from compas_timber.connections import TButtJoint
from compas_timber.fabrication import BTLx
from compas_timber.fabrication import BTLxJackCut
from compas_timber.fabrication import BTLxDoubleCut
from compas_timber.fabrication.btlx_processes.btlxlap import BTLxLap
from compas.geometry import intersection_plane_plane, intersection_plane_plane_plane, Vector, Plane, Frame, Transformation, Point
import math


class TButtFactory(object):
    """Factory class for creating T-Butt joints."""

    def __init__(self):
        self.main_part = None
        self.cross_part = None

    @staticmethod
    def calc_params_birdsmouth(joint, main_part, cross_part):
        face_dict = joint._beam_side_incidence(main_part.beam, cross_part.beam, ignore_ends=True)
        face_dict = sorted(face_dict, key=face_dict.get)
        frame1, frame2 = cross_part.beam.faces[face_dict[0]], cross_part.beam.faces[face_dict[1]]
        plane1, plane2 = Plane.from_frame(frame1), Plane.from_frame(frame2)
        intersect_vec = Vector.from_start_end(*intersection_plane_plane(plane2, plane1))

        angles_dict = {}
        for i, face in enumerate(main_part.beam.faces):
            angles_dict[i] = (face.normal.angle(intersect_vec))
        ref_frame_id = min(angles_dict, key=angles_dict.get)
        ref_frame = main_part.beam.faces[ref_frame_id]

        start_point = Point(*intersection_plane_plane_plane(plane1, plane2, Plane.from_frame(ref_frame)))
        start_point.transform(Transformation.from_frame_to_frame(ref_frame, Frame.worldXY()))
        StartX, StartY = start_point[0], start_point[1]

        intersect_vec1 = Vector.from_start_end(*intersection_plane_plane(plane1, Plane.from_frame(ref_frame)))
        intersect_vec2 = Vector.from_start_end(*intersection_plane_plane(plane2, Plane.from_frame(ref_frame)))
        Angle2 = math.degrees(intersect_vec1.angle(ref_frame.xaxis))
        Angle1 = math.degrees(intersect_vec2.angle(ref_frame.xaxis))

        normal_plane1 = Plane.from_frame(frame1).normal
        normal_plane2 = Plane.from_frame(frame2).normal
        Inclination1 = math.degrees(normal_plane1.angle(ref_frame.zaxis))
        Inclination2 = math.degrees(normal_plane2.angle(ref_frame.zaxis))

        return {
            "Orientation": "start",
            "StartX": StartX,
            "StartY": StartY,
            "Angle1": Angle1,
            "Inclination1": Inclination1,
            "Angle2": Angle2,
            "Inclination2": Inclination2,
            "ReferencePlaneID": ref_frame_id
        }



    @classmethod
    def apply_processings(cls, joint, parts):
        """
        Apply processings to the joint and its associated parts.

        Parameters
        ----------
        joint : :class:`~compas_timber.connections.joint.Joint`
            The joint object.
        parts : dict
            A dictionary of the BTLxParts connected by this joint, with part keys as the dictionary keys.

        Returns
        -------
        None

        """

        main_part = parts[str(joint.main_beam.key)]
        cross_part = parts[str(joint.cross_beam.key)]
        cut_plane = joint.get_main_cutting_plane()[0]
        if joint.birdsmouth == True:
            #calculate the process params
            joint_params = TButtFactory.calc_params_birdsmouth(joint, main_part, cross_part)
            main_part.processings.append(BTLxDoubleCut.create_process(joint_params, "T-Butt Joint"))
            #put processing here
        else:
            main_part.processings.append(BTLxJackCut.create_process(main_part, cut_plane, "T-Butt Joint"))

        if joint.mill_depth > 0:
            cross_part = parts[str(joint.cross_beam.key)]
            cross_part.processings.append(BTLxLap.create_process(joint.btlx_params_cross, "T-Butt Joint"))


BTLx.register_joint(TButtJoint, TButtFactory)
