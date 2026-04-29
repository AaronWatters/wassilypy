
"""
To Be Filled In.
"""

from typing import (
    Any, 
    Callable,
    Optional, 
    Protocol, 
    Sequence, 
    TypeVar,
    Union, 
    Annotated,
    TypeAlias,
    overload
)

import H5Gizmos as gz
import numpy as np

TStyled = TypeVar("TStyled", bound="Styled")
TWrapped = TypeVar("TWrapped", bound="Styled")
Number = Union[int, float]
Vec2 = Union[np.ndarray, Sequence[Number]]
Vec3 = Union[np.ndarray, Sequence[Number]]

class EventHandler(Protocol):
    def __call__(
        self,
        name: str,
        eventType: str,
        canvasXY: Vec2,
        cartesianXY: Vec2,
        frameXY: Vec2,
    ) -> None: ...

def listiffy(x: Any) -> Any:
    # convert numpy arrays and all elements of tuples/lists to lists
    """Convert numpy arrays and all elements of tuples/lists to lists
    
    Args:
        x (Any): Object to convert.
    
    Returns:
        Any: Converted object.
    """
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, tuple) or isinstance(x, list):
        return [listiffy(e) for e in x]
    else:
        return x
    
class Styled:

    """A styled element in the diagram."""
    def __init__(self, js_reference: Any, on_diagram: Any) -> None:
        """Attach a JavaScript reference to the styled element.
        
        Args:
            js_reference: The JavaScript reference.
            on_diagram: The diagram to which the element belongs.
        """
        self.js_reference = js_reference
        self.on_diagram = on_diagram

    def coerceToSubclass(
            self,
            constructor: Callable[[Any, Any], TWrapped]) -> TWrapped:
        """Convert this styled element to a subclass by using the provided constructor.
        
        Args:
            constructor: The constructor for the subclass.
        
        Returns:
            The converted styled element.
        """
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
        """Wrap the result of a JavaScript method call in a styled element.
        
        Args:
            methodname: The name of the JavaScript method to call.
            constructor: The constructor for the wrapped element.
            *arguments: The arguments for the JavaScript method call.
        
        Returns:
            The wrapped styled element.
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
        """Send a message to the JavaScript side without expecting a return value.
        
        Args:
            methodname: The name of the JavaScript method to call.
            *arguments: The arguments for the JavaScript method call.
        
        Returns:
            The styled element that sent the message.
        """
        args = (listiffy(arg) for arg in arguments)
        gz.do(self.js_reference[methodname](*args))
        return self
    
    def transition(self: TStyled, durationSeconds: float) -> TStyled:
        """Create a clone of this styled element representing a transtion to a new state over the specified duration.
        
        Args:
            durationSeconds: Duration of the transition.
        
        Returns:
            The cloned styled element representing the transition final state.
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
            handlerOrNull: Optional[EventHandler] = None,
            ) -> None:
        """Register or unregister an event handler.

        Args:
            eventType: Type of event to handle.
            handlerOrNull: Callback to invoke when the event fires.
                If None, unregisters the current handler.

        The handler is called as:
            handler(name, eventType, canvasXY, cartesianXY, frameXY)
        """
        self.send_only("handleEvent", eventType, handlerOrNull)

    def join(self: TStyled, join_spec: str) -> TStyled:
        """Set the line join style.
        
        Args:
            join_spec: The line join style to set (CanvasLineJoin like "round", "bevel", "miter").
        
        Returns:
            The styled element with the updated line join style.
        """
        return self.send_only("join", join_spec)

    def font(self: TStyled, font_spec: str) -> TStyled:
        """Set the font.
        
        Args:
            font_spec: The font to set (like "16px Arial italic").
        
        Returns:
            The styled element with the updated font.
        """
        return self.send_only("font", font_spec)

    def stroked(self: TStyled) -> TStyled:
        """Set the element to be stroked (not filled).
        
        Returns:
            The styled element with the updated stroke style.
        """
        return self.send_only("stroked")
    
    def filled(self: TStyled) -> TStyled:
        """Set the element to be filled (not stroked).
        
        Returns:
            The styled element with the updated fill style.
        """
        return self.send_only("filled")
    
    def colored(self: TStyled, color_spec: str) -> TStyled:
        """Set the color of the element.
        
        Args:
            color_spec: The color to set (like "red", "#ff0000", or "rgba(255, 0, 0, 1)").
        
        Returns:
            The styled element with the updated color.
        """
        return self.send_only("colored", color_spec)
    
    def linedWidth(self: TStyled, width: float) -> TStyled:
        """Set the width of the line.
        
        Args:
            width (float): The width of the line to set.
        
        Returns:
            The styled element with the updated line width.
        """
        return self.send_only("linedWidth", width)
    
    def dashed(
            self: TStyled, 
            dash_list_or_null: Optional[list[Number]],
            ) -> TStyled:
        """Set the dash pattern for the line.
        
        Args:
            dash_list_or_null (Any): The dash pattern to set like [10, 5].
        
        Returns:
            The styled element with the updated dash pattern.
        """
        return self.send_only("dashed", dash_list_or_null)
    
    def setFramePoint(self: TStyled, xy: Vec2) -> TStyled:
        """Set the position of the element in frame coordinates.
        
        Args:
            xy (Any): The position to set.
        
        Returns:
            The styled element with the updated position.
        """
        xy = listiffy(xy)
        return self.send_only("setFramePoint", xy)
    
    def setPixel(self: TStyled, xy: Vec2) -> TStyled:
        """Set the position of the element in pixel coordinates.
        
        Args:
            xy (Any): The position to set.
        
        Returns:
            The styled element with the updated position.
        """
        xy = listiffy(xy)
        return self.send_only("setPixel", xy)
    
    def position(self: TStyled, xy: Vec2) -> TStyled:
        """Set the position of the element (in frame coordinates).
        
        Args:
            xy (Any): The position to set.
        
        Returns:
            The styled element with the updated position.
        """
        return self.setFramePoint(xy)
    
    def forget(self) -> None:
        """Mark the element to be forgotten (deleted from the diagram)..
        """
        self.send_only("forget")
        self.js_reference = None
        self.on_diagram = None

    def requestRedraw(self: TStyled) -> TStyled:
        """Request a redraw of the diagram containing the element.
        
        Returns:
            The styled element.
        """
        return self.send_only("requestRedraw")


class Line(Styled):
    
    """A line segment element."""
    def startAt(self, xy: Vec2) -> "Line":
        """Set the starting point of the line.
        
        Args:
            xy (Any): The starting point to set.
        
        Returns:
            The line element with the updated starting point.
        """
        xy = listiffy(xy)
        return self.send_only("startAt", xy)
    
    def endAt(self, xy: Vec2) -> "Line":
        """Set the ending point of the line.
        
        Args:
            xy (Any): The ending point to set.
        
        Returns:
            The line element with the updated ending point.
        """
        xy = listiffy(xy)
        return self.send_only("endAt", xy)

class Circle(Styled):
    
    """To Be Filled In."""
    def centerAt(self, xy: Vec2) -> "Circle":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("centerAt", xy)
    
    def resize(self, radius: float) -> "Circle":
        """To Be Filled In.
        
        Args:
            radius (float): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("resize", radius)
    
    def scaling(self, boolean: bool) -> "Circle":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("scaling", boolean)

class Rect(Styled):
    
    """To Be Filled In."""
    def degrees(self, angle: float) -> "Rect":
        """To Be Filled In.
        
        Args:
            angle (float): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("degrees", angle)
    
    def resize(self, wh: Vec2) -> "Rect":
        """To Be Filled In.
        
        Args:
            wh (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy: Vec2) -> "Rect":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean: bool) -> "Rect":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy: Vec2) -> "Rect":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
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
            To Be Filled In.
        """
        return self.send_only("setText", text)
    
    def valigned(self, alignment: str) -> "TextBox":
        """To Be Filled In.
        
        Args:
            alignment (str): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("valigned", alignment)
    
    def aligned(self, alignment: str) -> "TextBox":
        """To Be Filled In.
        
        Args:
            alignment (str): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("aligned", alignment)
    
    def setShift(self, shift: Any) -> "TextBox":
        """To Be Filled In.
        
        Args:
            shift (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        shift = listiffy(shift)
        return self.send_only("setShift", shift)
    
    def boxed(self, background_spec_or_null: Any) -> "TextBox":
        """To Be Filled In.
        
        Args:
            background_spec_or_null (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("boxed", background_spec_or_null)
    
    async def getSize(self) -> Any:
        """To Be Filled In.
        
        Returns:
            To Be Filled In.
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
            To Be Filled In.
        """
        points = listiffy(points)
        return self.send_only("vertices", points)
    
    def closed(self, boolean: bool = True) -> "Poly":
        """To Be Filled In.
        
        Args:
            boolean (bool, optional): To Be Filled In.
        
        Returns:
            To Be Filled In.
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
            To Be Filled In.
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
            To Be Filled In.
        """
        return self.send_only("normalColored", defaultxyz, alpha)

class Rect3d(Styled):
    
    """To Be Filled In."""
    def degrees(self, angle: float) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            angle (float): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("degrees", angle)
    
    def resize(self, wh: Vec2) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            wh (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        wh = listiffy(wh)
        return self.send_only("resize", wh)
    
    def offsetBy(self, xy: Vec2) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("offsetBy", xy)
    
    def scaling(self, boolean: bool) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            boolean (bool): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("scaling", boolean)
    
    def locateAt(self, xy: Vec2) -> "Rect3d":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
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
            To Be Filled In.
        """
        return self.send_only("scaling", boolean)
    
    def centered(self, xy: Vec2) -> "Circle3d":
        """To Be Filled In.
        
        Args:
            xy (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        xy = listiffy(xy)
        return self.send_only("centered", xy)
    
    def resized(self, radius: float) -> "Circle3d":
        """To Be Filled In.
        
        Args:
            radius (float): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("resized", radius)
