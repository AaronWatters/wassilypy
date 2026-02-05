
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

EPSILON = 1e-10

async def wassily2d(width, height=None, link=True):
    diagram = Diagram(width, height)
    if link:
        await diagram.link()
    else:
        await diagram.show()
    return diagram.mainFrame

class SwatchView:

    def __init__(self, pixelSize, modelSize, center=[0,0]):
        self.pixelSize = pixelSize
        self.modelSize = modelSize
        self.center = center
        self.diagram = Diagram(pixelSize, pixelSize)
        self.diagram.call_when_started(self.start)

    def start(self):
        modelSize = self.modelSize
        pixelSize = self.pixelSize
        center = np.array(self.center)
        model2 = modelSize / 2
        #pixelOffset = np.array([pixel2, pixel2])
        modelOffset = np.array([model2, model2])
        fromMin = [0,0]
        fromMax = [pixelSize, pixelSize]
        toMin = center - modelOffset
        toMax = center + modelOffset
        mainFrame = self.diagram.mainFrame
        swatchFrame = mainFrame.regionFrame(fromMin, fromMax, toMin, toMax)
        self.frame = swatchFrame

async def swatch(pixelSize, modelSize, center=[0,0], link=True):
    view = SwatchView(pixelSize, modelSize, center)
    if link:
        await view.diagram.link()
    else:
        await view.diagram.show()
    # frame should have been initialized upon start
    return view.frame

class CubeView:

    def __init__(self, pixelSize, modelSize, modelCenter=[0,0,0], perspective=True, shrink=0.9):
        self.pixelSize = pixelSize
        self.modelSize = modelSize
        self.modelCenter = modelCenter
        self.perspective = perspective
        self.shrink = shrink
        self.diagram = Diagram(pixelSize, pixelSize)
        self.diagram.call_when_started(self.start)

    def start(self):
        modelSize = self.modelSize
        pixelSize = self.pixelSize
        modelCenter = np.array(self.modelCenter)
        eyeOffset = np.array([0, 0, -1.5 * modelSize])
        eye = modelCenter + eyeOffset
        lookAt = modelCenter
        mainFrame = self.diagram.mainFrame
        swatchWidth = pixelSize * self.shrink
        model2 = modelSize / 2
        swatchFrame = mainFrame.regionFrame(
            [0,0],
            [swatchWidth, swatchWidth],
            modelCenter[0:2] - model2,
            modelCenter[0:2] + model2)
        cubeFrame = swatchFrame.frame3d(
            eyePoint=eye,
            lookAtPoint=lookAt,
            perspective=self.perspective)
        self.frame = cubeFrame


async def cube(pixelSize, modelSize, modelCenter=[0,0,0], perspective=True, shrink=0.9, link=True):
    view = CubeView(pixelSize, modelSize, modelCenter, perspective, shrink)
    if link:
        await view.diagram.link()
    else:
        await view.diagram.show()
    # frame should have been initialized upon start
    return view.frame

'''
async def cube(pixelSize, modelSize, modelCenter=[0,0,0], perspective=True, shrink=0.9):
    eyeOffset = np.array([0, 0, -1.5 * modelSize])
    modelCenter = np.array(modelCenter)
    eye = modelCenter + eyeOffset
    lookAt = modelCenter
    swatchWidth = pixelSize * shrink
    swatchFrame = await swatch(swatchWidth, modelSize, center=modelCenter[0:2])
    print(eye, lookAt, perspective)
    cubeFrame = swatchFrame.frame3d(
        eyePoint=eye,
        lookAtPoint=lookAt,
        perspective=perspective)
    return cubeFrame'''

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
        return self.send_only("clear")

    def fit(self, border=0):
        return self.send_only("fit", border)

    def setAffine(self, listMatrix):
        listMatrix = listiffy(listMatrix)
        return self.send_only("setAffine", listMatrix)
    
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
        return self.send_only("nameImageFromURL", name, url)

    def pauseRedraw(self):
        return self.send_only("pauseRedraw")

    def resumeRedraw(self):
        return self.send_only("resumeRedraw")

    def nameImageFromPNGData(self, name, png_data):
        """
        name a PNG encoded binary image from raw data.
        """
        png_data = force_uint8_array(png_data)
        return self.send_only("nameImageFromPNGData", name, png_data)

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
        size = [side, side]
        return self.wrapResult(
            "square", marking.Rect, 
            point, size, offset, scaled)
    
    def polyline(self, points):
        return self.wrapResult("polyline", marking.Poly, points)
    
    def polygon(self, points):
        return self.wrapResult("polygon", marking.Poly, points).filled().closed()
    
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

    def lookAt(self, lookAtPoint, epsilon=EPSILON):
        lookAtPoint = listiffy(lookAtPoint)
        return self.send_only("lookAt", lookAtPoint, epsilon)
    
    def lookFrom(self, eyePoint, upVector=None, epsilon=EPSILON):
        eyePoint = listiffy(eyePoint)
        if upVector is not None:
            upVector = listiffy(upVector)
        return self.send_only("lookFrom", eyePoint, upVector, epsilon)
    
    def orbit(self):
        return self.send_only("orbit")
    
    def clear(self):
        return self.send_only("clear")
    
    def fit(self, border=0):
        return self.send_only("fit", border)
    
    def nameImageFromURL(self, name, url):
        return self.send_only("nameImageFromURL", name, url)
    
    def imageFromURL(self, point3d, url, size=None, offset=[0,0], scaled=False):
        return self.wrapResult(
            "imageFromURL", marking.Image3d,
            point3d, url, size, offset, scaled)
    
    def namedImage(self, point3d, name, size=None, offset=[0,0], scaled=False):
        return self.wrapResult(
            "namedImage", marking.Image3d,
            point3d, name, size, offset, scaled)

    def textBox(self, point3d, text, shift=[0,0], alignment="left", background=None):
        return self.wrapResult(
            "textBox", marking.TextBox3d,
            point3d, text, shift, alignment, background)
    
    def line(self, start3d, end3d):
        return self.wrapResult("line", marking.Line3d, start3d, end3d)
    
    def polygon(self, points3d):
        return self.wrapResult("polygon", marking.Poly3d, points3d)
    
    def polyline(self, points3d):
        return self.wrapResult("polyline", marking.Poly3d, points3d)
    
    def circle(self, center3d, radius):
        return self.wrapResult("circle", marking.Circle3d, center3d, radius)