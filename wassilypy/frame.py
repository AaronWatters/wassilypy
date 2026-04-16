
"""
To Be Filled In.
"""

from typing import Any, Callable, Optional, TypeVar, overload

import H5Gizmos as gz
import numpy as np
import importlib.resources
import os
from . import marking
from .marking import listiffy

EPSILON = 1e-10
TWrapped = TypeVar("TWrapped", bound=marking.Styled)


async def wassily2d(
        width: float,
        height: Optional[float] = None,
        link: bool = True) -> "Frame":
    """To Be Filled In.
    
    Args:
        width (float): To Be Filled In.
        height (Optional[float], optional): To Be Filled In.
        link (bool, optional): To Be Filled In.
    
    Returns:
        'Frame': To Be Filled In.
    """
    diagram = Diagram(width, height)
    if link:
        await diagram.link()
    else:
        await diagram.show()
    return diagram.mainFrame

class SwatchView:

    """To Be Filled In."""
    def __init__(
            self,
            pixelSize: float,
            modelSize: float,
            center: Any = [0,0]) -> None:
        """To Be Filled In.
        
        Args:
            pixelSize (float): To Be Filled In.
            modelSize (float): To Be Filled In.
            center (Any, optional): To Be Filled In.
        """
        self.pixelSize = pixelSize
        self.modelSize = modelSize
        self.center = center
        self.diagram = Diagram(pixelSize, pixelSize)
        self.diagram.call_when_started(self.start)

    def start(self) -> None:
        """To Be Filled In.
        """
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

async def swatch(
        pixelSize: float,
        modelSize: float,
        center: Any = [0,0],
        link: bool = True) -> "Frame":
    """To Be Filled In.
    
    Args:
        pixelSize (float): To Be Filled In.
        modelSize (float): To Be Filled In.
        center (Any, optional): To Be Filled In.
        link (bool, optional): To Be Filled In.
    
    Returns:
        'Frame': To Be Filled In.
    """
    view = SwatchView(pixelSize, modelSize, center)
    if link:
        await view.diagram.link()
    else:
        await view.diagram.show()
    # frame should have been initialized upon start
    return view.frame

class CubeView:

    """To Be Filled In."""
    def __init__(
            self,
            pixelSize: float,
            modelSize: float,
            modelCenter: Any = [0,0,0],
            perspective: bool = True,
            shrink: float = 0.9) -> None:
        """To Be Filled In.
        
        Args:
            pixelSize (float): To Be Filled In.
            modelSize (float): To Be Filled In.
            modelCenter (Any, optional): To Be Filled In.
            perspective (bool, optional): To Be Filled In.
            shrink (float, optional): To Be Filled In.
        """
        self.pixelSize = pixelSize
        self.modelSize = modelSize
        self.modelCenter = modelCenter
        self.perspective = perspective
        self.shrink = shrink
        self.diagram = Diagram(pixelSize, pixelSize)
        self.diagram.call_when_started(self.start)

    def start(self) -> None:
        """To Be Filled In.
        """
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


async def cube(
        pixelSize: float,
        modelSize: float,
        modelCenter: Any = [0,0,0],
        perspective: bool = True,
        shrink: float = 0.9,
        link: bool = True) -> "Frame3d":
    """To Be Filled In.
    
    Args:
        pixelSize (float): To Be Filled In.
        modelSize (float): To Be Filled In.
        modelCenter (Any, optional): To Be Filled In.
        perspective (bool, optional): To Be Filled In.
        shrink (float, optional): To Be Filled In.
        link (bool, optional): To Be Filled In.
    
    Returns:
        'Frame3d': To Be Filled In.
    """
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

    """To Be Filled In."""
    def __init__(self, width: float, height: Optional[float] = None) -> None:
        """To Be Filled In.
        
        Args:
            width (float): To Be Filled In.
            height (Optional[float], optional): To Be Filled In.
        """
        tag = "<div/>"
        super().__init__(tag)
        if height is None:
            height = width
        self.hw = (height, width)
        files = importlib.resources.files('wassilypy')
        js_path = str(files / 'data' / "wassilyts.umd.js")
        assert os.path.isfile(js_path)
        self.js_file(js_path)

    def configure_jQuery_element(self, element: Any) -> None:
        """To Be Filled In.
        
        Args:
            element (Any): To Be Filled In.
        """
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

    def styledRef(self, styled_name: str) -> Any:
        """To Be Filled In.
        
        Args:
            styled_name (str): To Be Filled In.
        
        Returns:
            Any: To Be Filled In.
        """
        return self.js_diagram.getStyledByName(styled_name)
    
    def wrapNamed(self, js_ref: Any, prefix: str = "wassilypy") -> Any:
        """To Be Filled In.
        
        Args:
            js_ref (Any): To Be Filled In.
            prefix (str, optional): To Be Filled In.
        
        Returns:
            Any: To Be Filled In.
        """
        new_id = gz.new_identifier(prefix)
        gz.do(js_ref.rename(new_id))
        return self.styledRef(new_id)
    

class Frame(marking.Styled):
    
    """To Be Filled In."""
    def __init__(self, js_reference: Any, on_diagram: Any) -> None:
        """To Be Filled In.
        
        Args:
            js_reference (Any): To Be Filled In.
            on_diagram (Any): To Be Filled In.
        """
        super().__init__(js_reference, on_diagram)

    def clear(self) -> "Frame":
        """To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        return self.send_only("clear")

    def fit(self, border: float = 0) -> "Frame":
        """To Be Filled In.
        
        Args:
            border (float, optional): To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        return self.send_only("fit", border)

    def setAffine(self, listMatrix: Any) -> "Frame":
        """To Be Filled In.
        
        Args:
            listMatrix (Any): To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        listMatrix = listiffy(listMatrix)
        return self.send_only("setAffine", listMatrix)
    
    def regionFrame(self,
                    fromMinxy: Any,
                    fromMaxxy: Any,
                    toMinxy: Any,
                    toMaxxy: Any) -> "Frame":
        """To Be Filled In.
        
        Args:
            fromMinxy (Any): To Be Filled In.
            fromMaxxy (Any): To Be Filled In.
            toMinxy (Any): To Be Filled In.
            toMaxxy (Any): To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
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
                eyePoint: Any,
                lookAtPoint: Any,
                perspective: bool = True,
                upVector: Any = None) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            eyePoint (Any): To Be Filled In.
            lookAtPoint (Any): To Be Filled In.
            perspective (bool, optional): To Be Filled In.
            upVector (Any, optional): To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        eyePoint = listiffy(eyePoint)
        lookAtPoint = listiffy(lookAtPoint)
        if upVector is not None:
            upVector = listiffy(upVector)
        return self.wrapResult("frame3d", Frame3d,
                               eyePoint,
                               lookAtPoint,
                                perspective,
                                upVector)
    
    @overload
    def getStyledByName(
            self,
            styled_name: str,
            constructor: None = None) -> marking.Styled:
        """To Be Filled In.
        
        Args:
            styled_name (str): To Be Filled In.
            constructor (None, optional): To Be Filled In.
        
        Returns:
            marking.Styled: To Be Filled In.
        """
        ...

    @overload
    def getStyledByName(
            self,
            styled_name: str,
            constructor: Callable[[Any, Any], TWrapped]) -> TWrapped:
        """To Be Filled In.
        
        Args:
            styled_name (str): To Be Filled In.
            constructor (Callable[[Any, Any], TWrapped]): To Be Filled In.
        
        Returns:
            TWrapped: To Be Filled In.
        """
        ...

    def getStyledByName(
            self,
            styled_name: str,
            constructor: Optional[Callable[[Any, Any], TWrapped]] = None
            ) -> marking.Styled:
        """To Be Filled In.
        
        Args:
            styled_name (str): To Be Filled In.
            constructor (Optional[Callable[[Any, Any], TWrapped]], optional): To Be Filled In.
        
        Returns:
            marking.Styled: To Be Filled In.
        """
        if constructor is None:
            constructor = marking.Styled
        return self.wrapResult("getStyledByName", constructor, styled_name)  
    
    def nameImageFromURL(self, name: str, url: str) -> "Frame":
        """To Be Filled In.
        
        Args:
            name (str): To Be Filled In.
            url (str): To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        return self.send_only("nameImageFromURL", name, url)

    def pauseRedraw(self) -> "Frame":
        """To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        return self.send_only("pauseRedraw")

    def resumeRedraw(self) -> "Frame":
        """To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        return self.send_only("resumeRedraw")

    def nameImageFromPNGData(self, name: str, png_data: Any) -> "Frame":
        """To Be Filled In.
        
        Args:
            name (str): To Be Filled In.
            png_data (Any): To Be Filled In.
        
        Returns:
            'Frame': To Be Filled In.
        """
        png_data = force_uint8_array(png_data)
        return self.send_only("nameImageFromPNGData", name, png_data)

    def pngImage(
            self,
            point: Any,
            pngdata: Any,
            size: Any = None,
            offset: Any = [0,0],
            scaled: bool = False) -> marking.Image:
        """To Be Filled In.
        
        Args:
            point (Any): To Be Filled In.
            pngdata (Any): To Be Filled In.
            size (Any, optional): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Image: To Be Filled In.
        """
        pngdata = force_uint8_array(pngdata)
        return self.wrapResult(
            "pngImage", marking.Image,
            point, pngdata, size, offset, scaled)
    
    def namedImage(
            self,
            point: Any,
            name: str,
            size: Any = None,
            offset: Any = [0,0],
            scaled: bool = False) -> marking.Image:
        """To Be Filled In.
        
        Args:
            point (Any): To Be Filled In.
            name (str): To Be Filled In.
            size (Any, optional): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Image: To Be Filled In.
        """
        return self.wrapResult(
            "namedImage", marking.Image,
            point, name, size, offset, scaled)
    
    def line(self, start: Any, end: Any) -> marking.Line:
        """To Be Filled In.
        
        Args:
            start (Any): To Be Filled In.
            end (Any): To Be Filled In.
        
        Returns:
            marking.Line: To Be Filled In.
        """
        return self.wrapResult("line", marking.Line, start, end)
    
    def dot(
            self,
            center: Any,
            radius: float,
            scaled: bool = False) -> marking.Circle:
        """To Be Filled In.
        
        Args:
            center (Any): To Be Filled In.
            radius (float): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Circle: To Be Filled In.
        """
        return self.wrapResult("dot", marking.Circle, center, radius, scaled)
    
    def circle(
            self,
            center: Any,
            radius: float,
            scaled: bool = True) -> marking.Circle:
        """To Be Filled In.
        
        Args:
            center (Any): To Be Filled In.
            radius (float): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Circle: To Be Filled In.
        """
        return self.wrapResult("circle", marking.Circle, center, radius, scaled)
    
    def rect(
            self,
            point: Any,
            size: Any,
            offset: Any = [0,0],
            scaled: bool = True,
            rotationDegrees: float = 0) -> marking.Rect:
        """To Be Filled In.
        
        Args:
            point (Any): To Be Filled In.
            size (Any): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
            rotationDegrees (float, optional): To Be Filled In.
        
        Returns:
            marking.Rect: To Be Filled In.
        """
        return self.wrapResult(
            "rect", marking.Rect, 
            point, size, offset, scaled, rotationDegrees)
    
    def box(
            self,
            point: Any,
            size: Any,
            offset: Any = [0,0],
            scaled: bool = False) -> marking.Rect:
        """To Be Filled In.
        
        Args:
            point (Any): To Be Filled In.
            size (Any): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Rect: To Be Filled In.
        """
        return self.wrapResult(
            "box", marking.Rect, 
            point, size, offset, scaled)
    
    def square(
            self,
            point: Any,
            side: float,
            offset: Any = [0,0],
            scaled: bool = False) -> marking.Rect:
        """To Be Filled In.
        
        Args:
            point (Any): To Be Filled In.
            side (float): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Rect: To Be Filled In.
        """
        size = [side, side]
        return self.wrapResult(
            "square", marking.Rect, 
            point, size, offset, scaled)
    
    def polyline(self, points: Any) -> marking.Poly:
        """To Be Filled In.
        
        Args:
            points (Any): To Be Filled In.
        
        Returns:
            marking.Poly: To Be Filled In.
        """
        return self.wrapResult("polyline", marking.Poly, points)
    
    def polygon(self, points: Any) -> marking.Poly:
        """To Be Filled In.
        
        Args:
            points (Any): To Be Filled In.
        
        Returns:
            marking.Poly: To Be Filled In.
        """
        return self.wrapResult("polygon", marking.Poly, points).filled().closed()
    
    def textBox(
            self,
            point: Any,
            text: str,
            shift: Any = [0,0],
            alignment: str = "left",
            background: Any = None) -> marking.TextBox:
        """To Be Filled In.
        
        Args:
            point (Any): To Be Filled In.
            text (str): To Be Filled In.
            shift (Any, optional): To Be Filled In.
            alignment (str, optional): To Be Filled In.
            background (Any, optional): To Be Filled In.
        
        Returns:
            marking.TextBox: To Be Filled In.
        """
        return self.wrapResult(
            "textBox", marking.TextBox,
            point, text, shift, alignment, background)
        
    def star(
            self,
            center: Any,
            innerRadius: float,
            numPoints: int = 5,
            pointFactor: float = 2.0,
            degrees: float = 0) -> marking.Star:
        """To Be Filled In.
        
        Args:
            center (Any): To Be Filled In.
            innerRadius (float): To Be Filled In.
            numPoints (int, optional): To Be Filled In.
            pointFactor (float, optional): To Be Filled In.
            degrees (float, optional): To Be Filled In.
        
        Returns:
            marking.Star: To Be Filled In.
        """
        return self.wrapResult(
            "star", marking.Star,
            center, innerRadius, numPoints, pointFactor, degrees)
    
    def arrow(
            self,
            back: Any,
            tip: Any,
            tipDegrees: float = 30,
            tipLength: Optional[float] = None,
            tipFactor: float = 0.1) -> marking.Arrow:
        """To Be Filled In.
        
        Args:
            back (Any): To Be Filled In.
            tip (Any): To Be Filled In.
            tipDegrees (float, optional): To Be Filled In.
            tipLength (Optional[float], optional): To Be Filled In.
            tipFactor (float, optional): To Be Filled In.
        
        Returns:
            marking.Arrow: To Be Filled In.
        """
        return self.wrapResult(
            "arrow", marking.Arrow,
            back, tip, tipDegrees, tipLength, tipFactor)

def force_uint8_array(x: Any) -> np.ndarray:
    """To Be Filled In.
    
    Args:
        x (Any): To Be Filled In.
    
    Returns:
        np.ndarray: To Be Filled In.
    """
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

    """To Be Filled In."""
    def lookAt(self, lookAtPoint: Any, epsilon: float = EPSILON) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            lookAtPoint (Any): To Be Filled In.
            epsilon (float, optional): To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        lookAtPoint = listiffy(lookAtPoint)
        return self.send_only("lookAt", lookAtPoint, epsilon)
    
    def lookFrom(
            self,
            eyePoint: Any,
            upVector: Any = None,
            epsilon: float = EPSILON) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            eyePoint (Any): To Be Filled In.
            upVector (Any, optional): To Be Filled In.
            epsilon (float, optional): To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        eyePoint = listiffy(eyePoint)
        if upVector is not None:
            upVector = listiffy(upVector)
        return self.send_only("lookFrom", eyePoint, upVector, epsilon)
    
    def orbit(self) -> "Frame3d":
        """To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        return self.send_only("orbit")
    
    def clear(self) -> "Frame3d":
        """To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        return self.send_only("clear")
    
    def fit(self, border: float = 0) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            border (float, optional): To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        return self.send_only("fit", border)
    
    def nameImageFromURL(self, name: str, url: str) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            name (str): To Be Filled In.
            url (str): To Be Filled In.
        
        Returns:
            'Frame3d': To Be Filled In.
        """
        return self.send_only("nameImageFromURL", name, url)
    
    def imageFromURL(
            self,
            point3d: Any,
            url: str,
            size: Any = None,
            offset: Any = [0,0],
            scaled: bool = False) -> marking.Image3d:
        """To Be Filled In.
        
        Args:
            point3d (Any): To Be Filled In.
            url (str): To Be Filled In.
            size (Any, optional): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Image3d: To Be Filled In.
        """
        return self.wrapResult(
            "imageFromURL", marking.Image3d,
            point3d, url, size, offset, scaled)
    
    def namedImage(
            self,
            point3d: Any,
            name: str,
            size: Any = None,
            offset: Any = [0,0],
            scaled: bool = False) -> marking.Image3d:
        """To Be Filled In.
        
        Args:
            point3d (Any): To Be Filled In.
            name (str): To Be Filled In.
            size (Any, optional): To Be Filled In.
            offset (Any, optional): To Be Filled In.
            scaled (bool, optional): To Be Filled In.
        
        Returns:
            marking.Image3d: To Be Filled In.
        """
        return self.wrapResult(
            "namedImage", marking.Image3d,
            point3d, name, size, offset, scaled)

    def textBox(
            self,
            point3d: Any,
            text: str,
            shift: Any = [0,0],
            alignment: str = "left",
            background: Any = None) -> marking.TextBox3d:
        """To Be Filled In.
        
        Args:
            point3d (Any): To Be Filled In.
            text (str): To Be Filled In.
            shift (Any, optional): To Be Filled In.
            alignment (str, optional): To Be Filled In.
            background (Any, optional): To Be Filled In.
        
        Returns:
            marking.TextBox3d: To Be Filled In.
        """
        return self.wrapResult(
            "textBox", marking.TextBox3d,
            point3d, text, shift, alignment, background)
    
    def line(self, start3d: Any, end3d: Any) -> marking.Line3d:
        """To Be Filled In.
        
        Args:
            start3d (Any): To Be Filled In.
            end3d (Any): To Be Filled In.
        
        Returns:
            marking.Line3d: To Be Filled In.
        """
        return self.wrapResult("line", marking.Line3d, start3d, end3d)
    
    def polygon(self, points3d: Any) -> marking.Poly3d:
        """To Be Filled In.
        
        Args:
            points3d (Any): To Be Filled In.
        
        Returns:
            marking.Poly3d: To Be Filled In.
        """
        return self.wrapResult("polygon", marking.Poly3d, points3d)
    
    def polyline(self, points3d: Any) -> marking.Poly3d:
        """To Be Filled In.
        
        Args:
            points3d (Any): To Be Filled In.
        
        Returns:
            marking.Poly3d: To Be Filled In.
        """
        return self.wrapResult("polyline", marking.Poly3d, points3d)
    
    def circle(self, center3d: Any, radius: float) -> marking.Circle3d:
        """To Be Filled In.
        
        Args:
            center3d (Any): To Be Filled In.
            radius (float): To Be Filled In.
        
        Returns:
            marking.Circle3d: To Be Filled In.
        """
        return self.wrapResult("circle", marking.Circle3d, center3d, radius)
