
"""
Frames and diagrams and convenience functions for creating interactive visualizations.
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
    """Create a 2D visualization frame.
    
    Args:
        width (float): Width of the frame in pixels.
        height (Optional[float], optional): Height of the frame in pixels. Defaults to None.
        link (bool, optional): If true then print an URL link to open the frame, otherwise try to open it in the browser.
    
    Returns:
        To Be Filled In.
    """
    diagram = Diagram(width, height)
    if link:
        await diagram.link()
    else:
        await diagram.show()
    return diagram.mainFrame

class SwatchView:

    """A square diagram."""
    def __init__(
            self,
            pixelSize: float,
            modelSize: float,
            center: Any = [0,0]) -> None:
        """A square diagram..
        
        Args:
            pixelSize (float): Side length of the square in pixels.
            modelSize (float): Side length of the square in model coordinates.
            center (Any, optional): Center of the square in model coordinates (default is [0,0]).
        """
        self.pixelSize = pixelSize
        self.modelSize = modelSize
        self.center = center
        self.diagram = Diagram(pixelSize, pixelSize)
        self.diagram.call_when_started(self.start)

    def start(self) -> None:
        """Create the model frame for the diagram.
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
    """Create a swatch visualization frame.
    
    Args:
        pixelSize (float): Side length of the square in pixels.
        modelSize (float): Side length of the square in model coordinates.
        center (Any, optional): Center of the square in model coordinates (default is [0,0]).
        link (bool, optional): If true then print an URL link to open the frame, otherwise try to open it in the browser.
    
    Returns:
        Frame: The created swatch frame.
    """
    view = SwatchView(pixelSize, modelSize, center)
    if link:
        await view.diagram.link()
    else:
        await view.diagram.show()
    # frame should have been initialized upon start
    return view.frame

class CubeView:

    """A 3D cube diagram."""
    def __init__(
            self,
            pixelSize: float,
            modelSize: float,
            modelCenter: Any = [0,0,0],
            perspective: bool = True,
            shrink: float = 0.9) -> None:
        """Create a 3D cube diagram.
        
        Args:
            pixelSize (float): Side length of the cube in pixels.
            modelSize (float): Side length of the cube in model coordinates.
            modelCenter (Any, optional): Center of the cube in model coordinates (default is [0,0,0]).
            perspective (bool, optional): If true then use perspective projection, otherwise use orthographic projection.
            shrink (float, optional): Factor by which to shrink the cube in the visualization.
        """
        self.pixelSize = pixelSize
        self.modelSize = modelSize
        self.modelCenter = modelCenter
        self.perspective = perspective
        self.shrink = shrink
        self.diagram = Diagram(pixelSize, pixelSize)
        self.diagram.call_when_started(self.start)

    def start(self) -> None:
        """Create the 3D cube frame for the diagram.
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
    """Create a 3D cube visualization frame.
    
    Args:
        pixelSize (float): Side length of the cube in pixels.
        modelSize (float): Side length of the cube in model coordinates.
        modelCenter (Any, optional): Center of the cube in model coordinates (default is [0,0,0]).
        perspective (bool, optional): If true then use perspective projection, otherwise use orthographic projection.
        shrink (float, optional): Factor by which to shrink the cube in the visualization.
        link (bool, optional): If true then print an URL link to open the frame, otherwise try to open it in the browser.
    
    Returns:
        Frame3d: The created 3D cube frame.
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

    """A canvas diagram with a standard primary frame."""
    def __init__(self, width: float, height: Optional[float] = None) -> None:
        """Make a diagram with a primary frame of the given width and height.
        
        Args:
            width (float): The width of the diagram in pixels.
            height (Optional[float], optional): The height of the diagram in pixels.
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
        """Configure the jQuery element for the diagram.
        
        Args:
            element (Any): The jQuery element to contain the diagram..
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
        """Get a reference to a styled element in the diagram by name.
        
        Args:
            styled_name (str): The name of the styled element to retrieve.
        
        Returns:
            Reference to the JavaScript object for the styled element.
        """
        return self.js_diagram.getStyledByName(styled_name)
    
    def wrapNamed(self, js_ref: Any, prefix: str = "wassilypy") -> Any:
        """Return a reference to a named element in the diagram.
        
        Args:
            js_ref (Any): The JavaScript reference to wrap.
            prefix (str, optional): The prefix for the new identifier.
        
        Returns:
            Reference to the JavaScript object for the named element.
        """
        new_id = gz.new_identifier(prefix)
        gz.do(js_ref.rename(new_id))
        return self.styledRef(new_id)
    

class Frame(marking.Styled):
    
    """A 'model coordinate' frame on the diagram."""
    def __init__(self, js_reference: Any, on_diagram: Any) -> None:
        """Create a new frame.
        
        Args:
            js_reference (Any): The JavaScript reference to the frame.
            on_diagram (Any): The diagram to which the frame belongs.
        """
        super().__init__(js_reference, on_diagram)

    def clear(self) -> "Frame":
        """Clear the frame.
        
        Returns:
            The frame for chaining.
        """
        return self.send_only("clear")

    def fit(self, border: float = 0) -> "Frame":
        """Fit the frame to the diagram.
        
        Args:
            border (float, optional): The border around the frame.
        
        Returns:
            The frame for chaining.
        """
        return self.send_only("fit", border)

    def setAffine(self, listMatrix: Any) -> "Frame":
        """Set the affine transformation for the frame.
        
        Args:
            listMatrix (Any): The matrix to set.
        
        Returns:
            The frame for chaining.
        """
        listMatrix = listiffy(listMatrix)
        return self.send_only("setAffine", listMatrix)
    
    def regionFrame(self,
                    fromMinxy: Any,
                    fromMaxxy: Any,
                    toMinxy: Any,
                    toMaxxy: Any) -> "Frame":
        """A frame region within this frame..
        
        Args:
            fromMinxy (Any): Minimum coordinates of the source region.
            fromMaxxy (Any): Maximum coordinates of the source region.
            toMinxy (Any): Minimum coordinates of the target region.
            toMaxxy (Any): Maximum coordinates of the target region.
        
        Returns:
            The new frame corresponding to the specified region.
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
        """Create a 3D frame.
        
        Args:
            eyePoint (Any): The point from which to view the scene.
            lookAtPoint (Any): The point at which to look.
            perspective (bool, optional): Whether to use perspective projection.
            upVector (Any, optional): The vector indicating the upward direction.
        
        Returns:
            The new 3D frame.
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
        ...

    @overload
    def getStyledByName(
            self,
            styled_name: str,
            constructor: Callable[[Any, Any], TWrapped]) -> TWrapped:
        ...

    def getStyledByName(
            self,
            styled_name: str,
            constructor: Optional[Callable[[Any, Any], TWrapped]] = None
            ) -> marking.Styled:
        """Get a styled element by its name from the frame.
        
        Args:
            styled_name: The name of the styled element to retrieve.
            constructor: The constructor to use for creating the styled element.
        
        Returns:
            A python wrapper for the styled element with the specified name.
        """
        if constructor is None:
            constructor = marking.Styled
        return self.wrapResult("getStyledByName", constructor, styled_name)  
    
    def nameImageFromURL(self, name: str, url: str) -> "Frame":
        """Create an image from a URL and name it.
        
        Args:
            name (str): The name to assign to the image.
            url (str): The URL of the image to create.
        
        Returns:
            The frame for chaining.
        """
        return self.send_only("nameImageFromURL", name, url)

    def pauseRedraw(self) -> "Frame":
        """Pause the redraw of the frame.
        
        Returns:
            The frame for chaining.
        """
        return self.send_only("pauseRedraw")

    def resumeRedraw(self) -> "Frame":
        """Resume the redraw of the frame.
        
        Returns:
            The frame for chaining.
        """
        return self.send_only("resumeRedraw")

    def nameImageFromPNGData(self, name: str, png_data: Any) -> "Frame":
        """Create an image from PNG data and name it.
        
        Args:
            name (str): The name to assign to the image.
            png_data (Any): PNG-encoded binary image data.
        
        Returns:
            The frame for chaining.
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
        """Place a PNG image on the frame.
        
        Args:
            point (Any): The point where the image will be placed in frame coordinates.
            pngdata (Any): The PNG-encoded binary image data.
            size (Any, optional): The size of the image (defaults to image size).

            offset (Any, optional): Shift the image by this amount.
            scaled (bool, optional): Whether the image should be scaled (defaults to False).
        
        Returns:
            A python wrapper for the image.
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
        """Create an image from a named source and place it on the frame.
        
        Args:
            point (Any): The point where the image will be placed in frame coordinates.
            name (str): The name of the image to create.
            size (Any, optional): The size of the image (defaults to image size).
            offset (Any, optional): Shift the image by this amount.
            scaled (bool, optional): Whether the image should be scaled (defaults to False).
        
        Returns:
            A python wrapper for the image.
        """
        return self.wrapResult(
            "namedImage", marking.Image,
            point, name, size, offset, scaled)
    
    def line(self, start: Any, end: Any) -> marking.Line:
        """Create a line on the frame.
        
        Args:
            start (Any): The starting point of the line.
            end (Any): The ending point of the line.
        
        Returns:
            A python wrapper for the line.
        """
        return self.wrapResult("line", marking.Line, start, end)
    
    def dot(
            self,
            center: Any,
            radius: float,
            scaled: bool = False) -> marking.Circle:
        """Create a dot on the frame.
        
        Args:
            center (Any): The center point of the dot.
            radius (float): The radius of the dot.
            scaled (bool, optional): Whether the dot should be scaled (defaults to False).
        
        Returns:
            A python wrapper for the dot.
        """
        return self.wrapResult("dot", marking.Circle, center, radius, scaled)
    
    def circle(
            self,
            center: Any,
            radius: float,
            scaled: bool = True) -> marking.Circle:
        """Create a circle on the frame.
        
        Args:
            center (Any): The center point of the circle.
            radius (float): The radius of the circle.
            scaled (bool, optional): Whether the circle should be scaled (defaults to True).
        
        Returns:
            A python wrapper for the circle.
        """
        return self.wrapResult("circle", marking.Circle, center, radius, scaled)
    
    def rect(
            self,
            point: Any,
            size: Any,
            offset: Any = [0,0],
            scaled: bool = True,
            rotationDegrees: float = 0) -> marking.Rect:
        """Create a rectangle on the frame.
        
        Args:
            point (Any): The point where the rectangle will be placed in frame coordinates.
            size (Any): The size of the rectangle.
            offset (Any, optional): Shift the rectangle by this amount.
            scaled (bool, optional): Whether the rectangle should be scaled (defaults to True).
            rotationDegrees (float, optional): The rotation of the rectangle in degrees (defaults to 0).
        
        Returns:
            A python wrapper for the rectangle.
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
        """Create a box on the frame.
        
        Args:
            point (Any): The point where the box will be placed in frame coordinates.
            size (Any): The size of the box.
            offset (Any, optional): Shift the box by this amount.
            scaled (bool, optional): Whether the box should be scaled (defaults to False).
        
        Returns:
            A python wrapper for the box.
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
        """Create a square on the frame.
        
        Args:
            point (Any): The point where the square will be placed in frame coordinates.
            side (float): The side length of the square.
            offset (Any, optional): Shift the square by this amount.
            scaled (bool, optional): Whether the square should be scaled (defaults to False).
        
        Returns:
            A python wrapper for the square.
        """
        size = [side, side]
        return self.wrapResult(
            "square", marking.Rect, 
            point, size, offset, scaled)
    
    def polyline(self, points: Any) -> marking.Poly:
        """Create a polyline on the frame.
        
        Args:
            points (Any): The points that define the polyline.
        
        Returns:
            A python wrapper for the polyline.
        """
        return self.wrapResult("polyline", marking.Poly, points)
    
    def polygon(self, points: Any) -> marking.Poly:
        """Create a polygon on the frame.
        
        Args:
            points (Any): The points that define the polygon.
        
        Returns:
            A python wrapper for the polygon.
        """
        return self.wrapResult("polygon", marking.Poly, points).filled().closed()
    
    def textBox(
            self,
            point: Any,
            text: str,
            shift: Any = [0,0],
            alignment: str = "left",
            background: Any = None) -> marking.TextBox:
        """Create a text box on the frame.
        
        Args:
            point (Any): The point where the text box will be placed in frame coordinates.
            text (str): The text to display in the text box.
            shift (Any, optional): Shift the text box by this amount.
            alignment (str, optional): The alignment of the text within the box (defaults to "left").
            background (Any, optional): The background color of the text box.
        
        Returns:
            A python wrapper for the text box.
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
        """Create a star on the frame.
        
        Args:
            center (Any): The center point of the star.
            innerRadius (float): The radius of the inner points of the star.
            numPoints (int, optional): The number of points on the star (defaults to 5).
            pointFactor (float, optional): The factor by which to scale the outer points (defaults to 2.0).
            degrees (float, optional): The rotation of the star in degrees (defaults to 0).
        
        Returns:
            A python wrapper for the star.
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
        """Create an arrow on the frame.
        
        Args:
            back (Any): The back point of the arrow.
            tip (Any): The tip point of the arrow.
            tipDegrees (float, optional): The angle of the arrow tip in degrees (defaults to 30).
            tipLength (Optional[float], optional): The length of the arrow tip (defaults to None).
            tipFactor (float, optional): The factor by which to scale the arrow tip (defaults to 0.1).
        
        Returns:
            A python wrapper for the arrow.
        """
        return self.wrapResult(
            "arrow", marking.Arrow,
            back, tip, tipDegrees, tipLength, tipFactor)

def force_uint8_array(x: Any) -> np.ndarray:
    """Convert bytes or numpy array to uint8 array.
    
    Args:
        x (Any): The input data to convert.
    
    Returns:
        np.ndarray: The converted uint8 array.
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
        """Look at a point in 3D space. 
        
        Args:
            lookAtPoint (Any): To Be Filled In.
            epsilon (float, optional): To Be Filled In.
        
        Returns:
            To Be Filled In.
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
            To Be Filled In.
        """
        eyePoint = listiffy(eyePoint)
        if upVector is not None:
            upVector = listiffy(upVector)
        return self.send_only("lookFrom", eyePoint, upVector, epsilon)
    
    def orbit(self) -> "Frame3d":
        """To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("orbit")
    
    def clear(self) -> "Frame3d":
        """To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("clear")
    
    def fit(self, border: float = 0) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            border (float, optional): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.send_only("fit", border)
    
    def nameImageFromURL(self, name: str, url: str) -> "Frame3d":
        """To Be Filled In.
        
        Args:
            name (str): To Be Filled In.
            url (str): To Be Filled In.
        
        Returns:
            To Be Filled In.
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
            To Be Filled In.
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
            To Be Filled In.
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
            To Be Filled In.
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
            To Be Filled In.
        """
        return self.wrapResult("line", marking.Line3d, start3d, end3d)
    
    def polygon(self, points3d: Any) -> marking.Poly3d:
        """To Be Filled In.
        
        Args:
            points3d (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.wrapResult("polygon", marking.Poly3d, points3d)
    
    def polyline(self, points3d: Any) -> marking.Poly3d:
        """To Be Filled In.
        
        Args:
            points3d (Any): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.wrapResult("polyline", marking.Poly3d, points3d)
    
    def circle(self, center3d: Any, radius: float) -> marking.Circle3d:
        """To Be Filled In.
        
        Args:
            center3d (Any): To Be Filled In.
            radius (float): To Be Filled In.
        
        Returns:
            To Be Filled In.
        """
        return self.wrapResult("circle", marking.Circle3d, center3d, radius)
