
"""
To Be Filled In.
"""

from typing import Any, Callable, Optional, TypeVar, Union, overload

import H5Gizmos as gz
import numpy as np

TStyled = TypeVar("TStyled", bound="Styled")
TWrapped = TypeVar("TWrapped", bound="Styled")


def listiffy(x: Any) -> Any:
    # convert numpy arrays and all elements of tuples/lists to lists
    """To Be Filled In.
    
    Args:
        x (Any): To Be Filled In.
    
    Returns:
        Any: To Be Filled In.
    """
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, tuple) or isinstance(x, list):
        return [listiffy(e) for e in x]
    else:
        return x
    
class Styled:

    """To Be Filled In."""
    def __init__(self, js_reference: Any, on_diagram: Any) -> None:
        """To Be Filled In.
        
        Args:
            js_reference (Any): To Be Filled In.
            on_diagram (Any): To Be Filled In.
        """
        self.js_reference = js_reference
        self.on_diagram = on_diagram

    def coerceToSubclass(
            self,
            constructor: Callable[[Any, Any], TWrapped]) -> TWrapped:
        """To Be Filled In.
        
        Args:
            constructor (Callable[[Any, Any], TWrapped]): To Be Filled In.
        
        Returns:
            TWrapped: To Be Filled In.
        """
        return constructor(self.js_reference, self.on_diagram)

    @overload
    def wrapResult(
            self,
            methodname: str,
            constructor: None = None,
            *arguments: Any) -> "Styled":
        """To Be Filled In.
        
        Args:
            methodname (str): To Be Filled In.
            constructor (None, optional): To Be Filled In.
            *arguments (Any): To Be Filled In.
        
        Returns:
            'Styled': To Be Filled In.
        """
        ...

    @overload
    def wrapResult(
            self,
            methodname: str,
            constructor: Callable[[Any, Any], TWrapped],
            *arguments: Any) -> TWrapped:
        """To Be Filled In.
        
        Args:
            methodname (str): To Be Filled In.
            constructor (Callable[[Any, Any], TWrapped]): To Be Filled In.
            *arguments (Any): To Be Filled In.
        
        Returns:
            TWrapped: To Be Filled In.
        """
        ...

    def wrapResult(
            self,
            methodname: str,
            constructor: Optional[Callable[[Any, Any], TWrapped]] = None,
            *arguments: Any) -> Union["Styled", TWrapped]:
        """To Be Filled In.
        
        Args:
            methodname (str): To Be Filled In.
            constructor (Optional[Callable[[Any, Any], TWrapped]], optional): To Be Filled In.
            *arguments (Any): To Be Filled In.
        
        Returns:
            Union['Styled', TWrapped]: To Be Filled In.
        """
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
        """To Be Filled In.
        
        Args:
            methodname (str): To Be Filled In.
            *arguments (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        args = (listiffy(arg) for arg in arguments)
        gz.do(self.js_reference[methodname](*args))
        return self
    
    def transition(self: TStyled, durationSeconds: float) -> TStyled:
        """To Be Filled In.
        
        Args:
            durationSeconds (float): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
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
        """To Be Filled In.
        
        Args:
            eventType (str): To Be Filled In.
            handlerOrNull (Any, optional): To Be Filled In. If not null, the
                handler signature is
                ``handler(name, eventType, canvasXY, cartesianXY, frameXY)``.
                A null handler cancels the previous handler.
        """
        self.send_only("handleEvent", eventType, handlerOrNull)

    def join(self: TStyled, join_spec: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            join_spec (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("join", join_spec)

    def font(self: TStyled, font_spec: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            font_spec (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("font", font_spec)

    def stroked(self: TStyled) -> TStyled:
        """To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("stroked")
    
    def filled(self: TStyled) -> TStyled:
        """To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("filled")
    
    def colored(self: TStyled, color_spec: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            color_spec (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("colored", color_spec)
    
    def linedWidth(self: TStyled, width: float) -> TStyled:
        """To Be Filled In.
        
        Args:
            width (float): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("linedWidth", width)
    
    def dashed(self: TStyled, dash_list_or_null: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            dash_list_or_null (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("dashed", dash_list_or_null)
    
    def setFramePoint(self: TStyled, xy: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("setFramePoint", xy)
    
    def setPixel(self: TStyled, xy: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("setPixel", xy)
    
    def position(self: TStyled, xy: Any) -> TStyled:
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.setFramePoint(xy)
    
    def forget(self) -> None:
        """To Be Filled In.
        """
        self.send_only("forget")
        self.js_reference = None
        self.on_diagram = None

    def requestRedraw(self: TStyled) -> TStyled:
        """To Be Filled In.
        
        Returns:
            TStyled: To Be Filled In.
        """
        return self.send_only("requestRedraw")


class Line(Styled):
    
    """To Be Filled In."""
    def startAt(self, xy: Any) -> "Line":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Line': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("startAt", xy)
    
    def endAt(self, xy: Any) -> "Line":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Line': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("endAt", xy)

class Circle(Styled):
    
    """To Be Filled In."""
    def centerAt(self, xy: Any) -> "Circle":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Circle': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("centerAt", xy)
    
    def resize(self, radius: float) -> "Circle":
        """To Be Filled In.
        
        Args:
            radius (float): To Be Filled In.
        
        Returns:
            'Circle': To Be Filled In.
        """
        return self.send_only("resize", radius)
    
    def scaling(self, boolean: bool) -> "Circle":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            'Circle': To Be Filled In.
        """
        return self.send_only("scaling", boolean)

class Rect(Styled):
    
    """To Be Filled In."""
    def degrees(self, angle: float) -> "Rect":
        """To Be Filled In.
        
        Args:
            angle (float): To Be Filled In.
        
        Returns:
            'Rect': To Be Filled In.
        """
        return self.send_only("degrees", angle)
    
    def resize(self, wh: Any) -> "Rect":
        """To Be Filled In.
        
        Args:
            wh (Any): To Be Filled In.
        
        Returns:
            'Rect': To Be Filled In.
        """
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy: Any) -> "Rect":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Rect': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean: bool) -> "Rect":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            'Rect': To Be Filled In.
        """
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy: Any) -> "Rect":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Rect': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("locateAt", xy)

class Image(Rect):
    """To Be Filled In."""
    pass

class TextBox(Rect):
    
    """To Be Filled In."""
    def setText(self, text: str) -> "TextBox":
        """To Be Filled In.
        
        Args:
            text (str): To Be Filled In.
        
        Returns:
            'TextBox': To Be Filled In.
        """
        return self.send_only("setText", text)
    
    def valigned(self, alignment: str) -> "TextBox":
        """To Be Filled In.
        
        Args:
            alignment (str): To Be Filled In.
        
        Returns:
            'TextBox': To Be Filled In.
        """
        return self.send_only("valigned", alignment)
    
    def aligned(self, alignment: str) -> "TextBox":
        """To Be Filled In.
        
        Args:
            alignment (str): To Be Filled In.
        
        Returns:
            'TextBox': To Be Filled In.
        """
        return self.send_only("aligned", alignment)
    
    def setShift(self, shift: Any) -> "TextBox":
        """To Be Filled In.
        
        Args:
            shift (Any): To Be Filled In.
        
        Returns:
            'TextBox': To Be Filled In.
        """
        shift = listiffy(shift)
        return self.send_only("setShift", shift)
    
    def boxed(self, background_spec_or_null: Any) -> "TextBox":
        """To Be Filled In.
        
        Args:
            background_spec_or_null (Any): To Be Filled In.
        
        Returns:
            'TextBox': To Be Filled In.
        """
        return self.send_only("boxed", background_spec_or_null)
    
    async def getSize(self) -> Any:
        """To Be Filled In.
        
        Returns:
            Any: To Be Filled In.
        """
        result = await gz.get(self.js_reference.getSize())
        return result


class Poly(Styled):
    
    """To Be Filled In."""
    def vertices(self, points: Any) -> "Poly":
        """To Be Filled In.
        
        Args:
            points (Any): To Be Filled In.
        
        Returns:
            'Poly': To Be Filled In.
        """
        points = listiffy(points)
        return self.send_only("vertices", points)
    
    def closed(self, boolean: bool = True) -> "Poly":
        """To Be Filled In.
        
        Args:
            boolean (bool, optional): To Be Filled In.
        
        Returns:
            'Poly': To Be Filled In.
        """
        return self.send_only("closed", boolean)

class Star(Styled):
    """To Be Filled In."""
    pass

class Arrow(Styled):
    """To Be Filled In."""
    pass

class Poly3d(Styled):

    """To Be Filled In."""
    def closed(self, boolean: bool = True) -> "Poly3d":
        """To Be Filled In.
        
        Args:
            boolean (bool, optional): To Be Filled In.
        
        Returns:
            'Poly3d': To Be Filled In.
        """
        return self.send_only("closed", boolean)
    
    def normalColored(
            self,
            defaultxyz: Any = [1,0,0],
            alpha: Optional[float] = None) -> "Poly3d":
        """To Be Filled In.
        
        Args:
            defaultxyz (Any, optional): To Be Filled In.
            alpha (Optional[float], optional): To Be Filled In.
        
        Returns:
            'Poly3d': To Be Filled In.
        """
        return self.send_only("normalColored", defaultxyz, alpha)

class Rect3d(Styled):
    
    """To Be Filled In."""
    def degrees(self, angle: float) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            angle (float): To Be Filled In.
        
        Returns:
            'Rect3d': To Be Filled In.
        """
        return self.send_only("degrees", angle)
    
    def resize(self, wh: Any) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            wh (Any): To Be Filled In.
        
        Returns:
            'Rect3d': To Be Filled In.
        """
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy: Any) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Rect3d': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean: bool) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            'Rect3d': To Be Filled In.
        """
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy: Any) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Rect3d': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("locateAt", xy)

class Image3d(Rect3d):
    """To Be Filled In."""
    pass

class TextBox3d(Rect3d):
    """To Be Filled In."""
    pass

class Line3d(Styled):
    """To Be Filled In."""
    pass

class Circle3d(Styled):

    """To Be Filled In."""
    def scaling(self, boolean: bool) -> "Circle3d":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            'Circle3d': To Be Filled In.
        """
        return self.send_only("scaling", boolean)
    
    def centered(self, xy: Any) -> "Circle3d":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            'Circle3d': To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("centered", xy)
    
    def resized(self, radius: float) -> "Circle3d":
        """To Be Filled In.
        
        Args:
            radius (float): To Be Filled In.
        
        Returns:
            'Circle3d': To Be Filled In.
        """
        return self.send_only("resized", radius)
