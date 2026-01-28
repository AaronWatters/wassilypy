
"""
Wrapping wassilyjs frames.
"""

import H5Gizmos as gz
import numpy as np
import importlib.resources
import os
from abc import ABC, abstractmethod
from . import marking
from .marking import listiffy


class Diagram(gz.jQueryComponent):

    def __init__(self, width, height=None):
        tag = "<div/>"
        super().__init__(tag)
        if height is None:
            height = width
        self.hw = (height, width)
        files = importlib.resources.files('wassilypy')
        js_path = str(files / 'data' / "wassilyts.umd.js")
        assert os.path.isfile(js_path)
        self.js_file(js_path)

    def configure_jQuery_element(self, element):
        super().configure_jQuery_element(element)
        domdiv = element[0]
        wassilyts = self.window.wassilyts
        console = self.window.console
        gz.do(console.log("wassilyts loaded", wassilyts))
        gz.do(console.log("domdiv", domdiv))
        (h, w) = self.hw
        self.js_frame = self.cache("mainFrame", wassilyts.drawOn(domdiv, w, h))
        self.mainFrame = Frame(self.js_frame, self)
        gz.do(console.log("frame", self.js_frame))
        self.js_diagram = self.cache("diagram", self.js_frame.diagram)
        gz.do(console.log("diagram", self.js_diagram))

    def styledRef(self, styled_name):
        return self.js_diagram.getStyledByName(styled_name)
    
    def wrapNamed(self, js_ref, prefix="wassilypy"):
        new_id = gz.new_identifier(prefix)
        gz.do(js_ref.rename(new_id))
        return self.styledRef(new_id)
    

class Frame(marking.Styled):
    
    def __init__(self, js_reference, on_diagram):
        super().__init__(js_reference, on_diagram)

    def clear(self):
        self.send_only("clear")

    def fit(self, border=0):
        self.send_only("fit", border)

    def setAffine(self, listMatrix):
        listMatrix = listiffy(listMatrix)
        self.send_only("setAffine", listMatrix)

    def regionFrame(self,
                    fromMinxy,
                    fromMaxxy,
                    toMinxy,
                    toMaxxy,):
        fromMinxy = listiffy(fromMinxy)
        fromMaxxy = listiffy(fromMaxxy)
        toMinxy = listiffy(toMinxy)
        toMaxxy = listiffy(toMaxxy)
        return self.wrapResult("regionFrame", Frame,
                               fromMinxy,
                               fromMaxxy,
                               toMinxy,
                               toMaxxy)
    
    def frame3d(self,
                eyePoint,
                lookAtPoint,
                perspective=True,
                upVector=None):
        eyePoint = listiffy(eyePoint)
        lookAtPoint = listiffy(lookAtPoint)
        if upVector is not None:
            upVector = listiffy(upVector)
        return self.wrapResult("frame3d", Frame3d,
                               eyePoint,
                               lookAtPoint,
                               perspective,
                               upVector)
    
    def getStyledByName(self, styled_name, constructor=None):
        if constructor is None:
            constructor = marking.Styled
        return self.wrapResult("getStyledByName", constructor, styled_name)  
    
    def nameImageFromURL(self, name, url):
        self.send_only("nameImageFromURL", name, url)

    def pauseRedraw(self):
        self.send_only("pauseRedraw")

    def resumeRedraw(self):
        self.send_only("resumeRedraw")

    def nameImageFromPNGData(self, name, png_data):
        """
        name a PNG encoded binary image from raw data.
        """
        png_data = force_uint8_array(png_data)
        self.send_only("nameImageFromPNGData", name, png_data)

    def pngImage(self, point, pngdata, size=None, offset=[0,0], scaled=False):
        pngdata = force_uint8_array(pngdata)
        return self.wrapResult(
            "pngImage", marking.Image,
            point, pngdata, size, offset, scaled)
    
    def namedImage(self, point, name, size=None, offset=[0,0], scaled=False):
        return self.wrapResult(
            "namedImage", marking.Image,
           point, name, size, offset, scaled)
    
    def line(self, start, end):
        return self.wrapResult("line", marking.Line, start, end)
    
    def dot(self, center, radius, scaled=False):
        return self.wrapResult("dot", marking.Circle, center, radius, scaled)
    
    def circle(self, center, radius, scaled=True):
        return self.wrapResult("circle", marking.Circle, center, radius, scaled)
    
    def rect(self, point, size, offset=[0,0], scaled=True, rotationDegrees=0):
        return self.wrapResult(
            "rect", marking.Rect, 
            point, size, offset, scaled, rotationDegrees)
    
    def box(self, point, size, offset=[0,0], scaled=False):
        return self.wrapResult(
            "box", marking.Rect, 
            point, size, offset, scaled)
    
    def square(self, point, side, offset=[0,0], scaled=False):
        return self.wrapResult(
            "square", marking.Rect, 
            point, side, offset, scaled)
    
    def polyline(self, points):
        return self.wrapResult("polyline", marking.Poly, points)
    
    def polygon(self, points):
        return self.wrapResult("polygon", marking.Poly, points)
    
    def textBox(self, point, text, shift=[0,0], alignment="left", background=None):
        return self.wrapResult(
            "textBox", marking.TextBox,
            point, text, shift, alignment, background)
        
    def star(
            self,
            center,
            innerRadius,
            numPoints=5,
            pointFactor=2.0,
            degrees=0):
        return self.wrapResult(
            "star", marking.Star,
            center, innerRadius, numPoints, pointFactor, degrees)
    
    def arrow(
            self,
            back,
            tip,
            tipDegrees=30,
            tipLength=None,
            tipFactor=0.1):
        return self.wrapResult(
            "arrow", marking.Arrow,
            back, tip, tipDegrees, tipLength, tipFactor)

def force_uint8_array(x):
    if isinstance(x, np.ndarray):
        if x.dtype != np.uint8:
            return x.astype(np.uint8)
        else:
            return x
    elif isinstance(x, bytes):
        return np.frombuffer(x, dtype=np.uint8).copy()
    else:
        raise TypeError("Expected bytes or numpy ndarray") 

class Frame3d(marking.Styled):
    pass
