
"""
Proxy classes for marking objects in a diagram
"""

import H5Gizmos as gz
import numpy as np


def listiffy(x):
    # convert numpy arrays and all elements of tuples/lists to lists
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, tuple) or isinstance(x, list):
        return [listiffy(e) for e in x]
    else:
        return x
    
class Styled:

    def __init__(self, js_reference, on_diagram):
        self.js_reference = js_reference
        self.on_diagram = on_diagram

    def coerceToSubclass(self, constructor):
        return constructor(self.js_reference, self.on_diagram)

    def wrapResult(self, methodname, constructor=None, *arguments):
        args = (listiffy(arg) for arg in arguments)
        js_ref = self.js_reference[methodname](*args)
        prefix = constructor.__name__ if constructor else "wassilypy"
        wrapper = self.on_diagram.wrapNamed(js_ref, prefix=prefix)
        if constructor is None:
            constructor = Styled
        return constructor(wrapper, self.on_diagram)

    def send_only(self, methodname, *arguments):
        args = (listiffy(arg) for arg in arguments)
        gz.do(self.js_reference[methodname](*args))
        return self

    def handleEvent(self, eventType, handlerOrNull=None):
        """
        Handle event type.  
        Handler if not null has signature:
        handler(name, eventType, canvasXY, cartesianXY, frameXY)
        Null handler cancels previous handler.
        """
        self.send_only("handleEvent", eventType, handlerOrNull)

    def join(self, join_spec):
        self.send_only("join", join_spec)

    def font(self, font_spec):
        self.send_only("font", font_spec)

    def stroked(self):
        return self.send_only("stroked")
    
    def filled(self):
        return self.send_only("filled")
    
    def colored(self, color_spec):
        return self.send_only("colored", color_spec)
    
    def linedWidth(self, width):
        return self.send_only("linedWidth", width)
    
    def dashed(self, dash_list_or_null):
        return self.send_only("dashed", dash_list_or_null)
    
    def setFramePoint(self, xy):
        xy = listiffy(xy)
        return self.send_only("setFramePoint", xy)
    
    def setPixel(self, xy):
        xy = listiffy(xy)
        return self.send_only("setPixel", xy)
    
    def position(self, xy):
        return self.setFramePoint(xy)
    
    def forget(self):
        self.send_only("forget")
        self.js_reference = None
        self.on_diagram = None

    def requestRedraw(self):
        self.send_only("requestRedraw")


class Line(Styled):
    
    def startAt(self, xy):
        xy = listiffy(xy)
        return self.send_only("startAt", xy)
    
    def endAt(self, xy):
        xy = listiffy(xy)
        return self.send_only("endAt", xy)

class Circle(Styled):
    
    def cemterAt(self, xy):
        xy = listiffy(xy)
        return self.send_only("centerAt", xy)
    
    def resize(self, radius):
        return self.send_only("resize", radius)
    
    def scaling(self, boolean):
        return self.send_only("scaling", boolean)

class Rect(Styled):
    
    def degrees(self, angle):
        return self.send_only("degrees", angle)
    
    def resize(self, wh):
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy):
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean):
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy):
        xy = listiffy(xy)
        return self.send_only("locateAt", xy)

class Image(Rect):
    pass

class TextBox(Rect):
    
    def setText(self, text):
        return self.send_only("setText", text)
    
    def valigned(self, alignment):
        return self.send_only("valigned", alignment)
    
    def aligned(self, alignment):
        return self.send_only("aligned", alignment)
    
    def setShift(self, shift):
        shift = listiffy(shift)
        return self.send_only("setShift", shift)
    
    def boxed(self, background_spec_or_null):
        return self.send_only("boxed", background_spec_or_null)
    
    async def getSize(self):
        result = await gz.get(self.js_reference.getSize())
        return result


class Poly(Styled):
    
    def vertices(self, points):
        points = listiffy(points)
        return self.send_only("vertices", points)
    
    def closed(self, boolean=True):
        return self.send_only("closed", boolean)

class Star(Styled):
    pass

class Arrow(Styled):
    pass

