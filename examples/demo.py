
from wassilypy import wassily2d
import H5Gizmos as gz

async def demo():
    #diagram = frame.Diagram(400, 300)
    #await diagram.link()
    #f = diagram.mainFrame
    f = await wassily2d(400, 300, link=True)
    center = [200, 150]
    c = f.circle(center, 100).colored("green")
    s = f.star(center, 50, 5).colored("orange").stroked()
    c.colored("blue").filled()
    a = f.arrow(center, [300, 150], tipLength=30).colored("red").linedWidth(5)
    t = f.textBox([200, 270], "Hello, Wassily!").font("20pt Arial").colored("navyblue").aligned("center")
    f.fit(border=20)
    return f

if __name__ == "__main__":
    gz.serve(demo())
