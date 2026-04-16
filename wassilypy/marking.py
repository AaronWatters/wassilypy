
"""
Proxy classes for marking objects in a diagram
"""

from typing import Any, Callable, Optional, TypeVar, Union, overload

import H5Gizmos as gz
import numpy as np

TStyled = TypeVar("TStyled", bound="Styled")
TWrapped = TypeVar("TWrapped", bound="Styled")


def listiffy(x: Any) -> Any:
    # convert numpy arrays and all elements of tuples/lists to lists
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, tuple) or isinstance(x, list):
        return [listiffy(e) for e in x]
    else:
        return x
    
class Styled:

    def __init__(self, js_reference: Any, on_diagram: Any) -> None:
        self.js_reference = js_reference
        self.on_diagram = on_diagram

    def coerceToSubclass(
            self,
            constructor: Callable[[Any, Any], TWrapped]) -> TWrapped:
        return constructor(self.js_reference, self.on_diagram)

    @overload
    def wrapResult(
            self,
            methodname: str,
            constructor: None = None,
            *arguments: Any) -> "Styled":
        ...

    @overload
    def wrapResult(
            self,
            methodname: str,
            constructor: Callable[[Any, Any], TWrapped],
            *arguments: Any) -> TWrapped:
        ...

    def wrapResult(
            self,
            methodname: str,
            constructor: Optional[Callable[[Any, Any], TWrapped]] = None,
            *arguments: Any) -> Union["Styled", TWrapped]:
        args = (listiffy(arg) for arg in arguments)
        js_ref = self.js_reference[methodname](*args)
        prefix = constructor.__name__ if constructor else "wassilypy"
        wrapper = self.on_diagram.wrapNamed(js_ref, prefix=prefix)
        if constructor is None:
            constructor = Styled
        return constructor(wrapper, self.on_diagram)

    def send_only(
            self: TStyled,
            methodname: str,
            *arguments: Any) -> TStyled:
        args = (listiffy(arg) for arg in arguments)
        gz.do(self.js_reference[methodname](*args))
        return self
    
    def transition(self: TStyled, durationSeconds: float) -> TStyled:
        myClassConstructor = self.__class__
        jsTransitionCall = self.js_reference.transition(durationSeconds)
        # JS side cache will uncache after the transition is collected on the python side.
        softCache = self.on_diagram.cache(name=None, js_reference=jsTransitionCall, soft=True)
        wrapper = myClassConstructor(softCache, self.on_diagram)
        return wrapper

    def handleEvent(
            self,
            eventType: str,
            handlerOrNull: Any = None) -> None:
        """
        Handle event type.  
        Handler if not null has signature:
        handler(name, eventType, canvasXY, cartesianXY, frameXY)
        Null handler cancels previous handler.
        """
        self.send_only("handleEvent", eventType, handlerOrNull)

    def join(self: TStyled, join_spec: Any) -> TStyled:
        return self.send_only("join", join_spec)

    def font(self: TStyled, font_spec: Any) -> TStyled:
        return self.send_only("font", font_spec)

    def stroked(self: TStyled) -> TStyled:
        return self.send_only("stroked")
    
    def filled(self: TStyled) -> TStyled:
        return self.send_only("filled")
    
    def colored(self: TStyled, color_spec: Any) -> TStyled:
        return self.send_only("colored", color_spec)
    
    def linedWidth(self: TStyled, width: float) -> TStyled:
        return self.send_only("linedWidth", width)
    
    def dashed(self: TStyled, dash_list_or_null: Any) -> TStyled:
        return self.send_only("dashed", dash_list_or_null)
    
    def setFramePoint(self: TStyled, xy: Any) -> TStyled:
        xy = listiffy(xy)
        return self.send_only("setFramePoint", xy)
    
    def setPixel(self: TStyled, xy: Any) -> TStyled:
        xy = listiffy(xy)
        return self.send_only("setPixel", xy)
    
    def position(self: TStyled, xy: Any) -> TStyled:
        return self.setFramePoint(xy)
    
    def forget(self) -> None:
        self.send_only("forget")
        self.js_reference = None
        self.on_diagram = None

    def requestRedraw(self: TStyled) -> TStyled:
        return self.send_only("requestRedraw")


class Line(Styled):
    
    def startAt(self, xy: Any) -> "Line":
        xy = listiffy(xy)
        return self.send_only("startAt", xy)
    
    def endAt(self, xy: Any) -> "Line":
        xy = listiffy(xy)
        return self.send_only("endAt", xy)

class Circle(Styled):
    
    def centerAt(self, xy: Any) -> "Circle":
        xy = listiffy(xy)
        return self.send_only("centerAt", xy)
    
    def resize(self, radius: float) -> "Circle":
        return self.send_only("resize", radius)
    
    def scaling(self, boolean: bool) -> "Circle":
        return self.send_only("scaling", boolean)

class Rect(Styled):
    
    def degrees(self, angle: float) -> "Rect":
        return self.send_only("degrees", angle)
    
    def resize(self, wh: Any) -> "Rect":
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy: Any) -> "Rect":
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean: bool) -> "Rect":
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy: Any) -> "Rect":
        xy = listiffy(xy)
        return self.send_only("locateAt", xy)

class Image(Rect):
    pass

class TextBox(Rect):
    
    def setText(self, text: str) -> "TextBox":
        return self.send_only("setText", text)
    
    def valigned(self, alignment: str) -> "TextBox":
        return self.send_only("valigned", alignment)
    
    def aligned(self, alignment: str) -> "TextBox":
        return self.send_only("aligned", alignment)
    
    def setShift(self, shift: Any) -> "TextBox":
        shift = listiffy(shift)
        return self.send_only("setShift", shift)
    
    def boxed(self, background_spec_or_null: Any) -> "TextBox":
        return self.send_only("boxed", background_spec_or_null)
    
    async def getSize(self) -> Any:
        result = await gz.get(self.js_reference.getSize())
        return result


class Poly(Styled):
    
    def vertices(self, points: Any) -> "Poly":
        points = listiffy(points)
        return self.send_only("vertices", points)
    
    def closed(self, boolean: bool = True) -> "Poly":
        return self.send_only("closed", boolean)

class Star(Styled):
    pass

class Arrow(Styled):
    pass

class Poly3d(Styled):

    def closed(self, boolean: bool = True) -> "Poly3d":
        return self.send_only("closed", boolean)
    
    def normalColored(
            self,
            defaultxyz: Any = [1,0,0],
            alpha: Optional[float] = None) -> "Poly3d":
        return self.send_only("normalColored", defaultxyz, alpha)

class Rect3d(Styled):
    
    def degrees(self, angle: float) -> "Rect3d":
        return self.send_only("degrees", angle)
    
    def resize(self, wh: Any) -> "Rect3d":
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy: Any) -> "Rect3d":
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean: bool) -> "Rect3d":
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy: Any) -> "Rect3d":
        xy = listiffy(xy)
        return self.send_only("locateAt", xy)

class Image3d(Rect3d):
    pass

class TextBox3d(Rect3d):
    pass

class Line3d(Styled):
    pass

class Circle3d(Styled):

    def scaling(self, boolean: bool) -> "Circle3d":
        return self.send_only("scaling", boolean)
    
    def centered(self, xy: Any) -> "Circle3d":
        xy = listiffy(xy)
        return self.send_only("centered", xy)
    
    def resized(self, radius: float) -> "Circle3d":
        return self.send_only("resized", radius)
