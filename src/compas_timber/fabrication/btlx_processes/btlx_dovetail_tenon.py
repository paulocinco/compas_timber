from collections import OrderedDict
from compas_timber.fabrication import BTLx
from compas_timber.fabrication import BTLxProcess


class BTLxDoveTailTenon(object):
    """
    Represents a dovetail_tenon process for timber fabrication.

    Parameters
    ----------
    param_dict : dict
        A dictionary containing the parameters for the BTLx lap process.
    joint_name : str
        The name of the joint. If not provided, the default name is "lap".
    kwargs : dict
        Additional keyword arguments to be added to the object.

    """

    PROCESS_TYPE = "DoubleCut"

    def __init__(self, param_dict, joint_name=None, **kwargs):
        self.apply_process = True
        self.reference_plane_id = param_dict["ReferencePlaneID"]
        self.orientation = param_dict["Orientation"]
        self.start_x = param_dict["StartX"]
        self.start_y = param_dict["StartY"]
        self.start_depth = param_dict["StartDepth"]
        self.angle = param_dict["Angle"]
        self.inclination = param_dict["Inclination"]
        self.rotation = param_dict["Rotation"]
        self.length_limited_top = param_dict["LengthLimitedTop"]
        self.length_limited_bottom = param_dict["LengthLimitedBottom"]
        self.length = param_dict["Length"]
        self.width = param_dict["Width"]
        self.height = param_dict["Height"]
        self.cone_angle = param_dict["ConeAngle"]
        self.use_flank_angle = param_dict["UseFlankAngle"]
        self.flank_angle = param_dict["FlankAngle"]
        self.shape = param_dict["Shape"]
        self.shape_radius = param_dict["ShapeRadius"]

        for key, value in param_dict.items():
            setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)

        if joint_name:
            self.name = joint_name
        else:
            self.name = "dovetail_tenon"

    @property
    def header_attributes(self):
        """the following attributes are required for all processes, but the keys and values of header_attributes are process specific."""
        return {
            "Name": self.name,
            "Process": "yes",
            "Priority": "0",
            "ProcessID": "0",
            "ReferencePlaneID": str(self.reference_plane_id + 1),
        }

    @property
    def process_params(self):
        """This property is required for all process types. It returns a dict with the geometric parameters to fabricate the joint."""

        if self.apply_process:
            """the following attributes are specific to Dovetail_Tenon"""
            od = OrderedDict(
                [
                    ("Orientation", str(self.orientation)),
                    ("StartX", "{:.{prec}f}".format(self.start_x, prec=BTLx.POINT_PRECISION)),
                    ("StartY", "{:.{prec}f}".format(self.start_y, prec=BTLx.POINT_PRECISION)),
                    ("StartDepth", "{:.{prec}f}".format(self.start_depth, prec=BTLx.POINT_PRECISION)),

                    ("Angle", "{:.{prec}f}".format(self.angle, prec=BTLx.ANGLE_PRECISION)),
                    ("Inclination", "{:.{prec}f}".format(self.inclination, prec=BTLx.ANGLE_PRECISION)),
                    ("Rotation", "{:.{prec}f}".format(self.rotation, prec=BTLx.ANGLE_PRECISION)),

                    ("LengthLimitedTop", bool(self.length_limited_top)),
                    ("LengthLimitedBottom", bool(self.length_limited_bottom)),

                    ("Length", "{:.{prec}f}".format(self.length, prec=BTLx.POINT_PRECISION)),
                    ("Width", "{:.{prec}f}".format(self.width, prec=BTLx.POINT_PRECISION)),
                    ("Height", "{:.{prec}f}".format(self.height, prec=BTLx.POINT_PRECISION)),

                    ("ConeAngle", "{:.{prec}f}".format(self.cone_angle, prec=BTLx.POINT_PRECISION)),
                    ("UseFlankAngle", bool(self.use_flank_angle)),

                    ("FlankAngle", "{:.{prec}f}".format(self.flank_angle, prec=BTLx.POINT_PRECISION)),
                    ("Shape", self.shape),
                    ("ShapeRadius", "{:.{prec}f}".format(self.shape_radius, prec=BTLx.POINT_PRECISION))
                ]
            )
            print("param dict", od)
            return od
        else:
            return None

    @classmethod
    def create_process(cls, param_dict, joint_name=None, **kwargs):
        """Creates a dovetail_tenon process from a dictionary of parameters."""
        dovetail_t = BTLxDoveTailTenon(param_dict, joint_name, **kwargs)
        return BTLxProcess(BTLxDoveTailTenon.PROCESS_TYPE, dovetail_t.header_attributes, dovetail_t.process_params)
