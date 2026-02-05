
from wassilypy import swatch

async def swatchDemo():
    center = [1,1]
    f = await swatch(300, 3, center=center)
    m = -0.5
    M = 2.5
    f.circle(center, 1.3).colored("lightgray").filled().scaling(True)
    f.line([m,m], [M,M]).linedWidth(2).colored("red")
    f.line([M,m], [m,M]).linedWidth(2).colored("blue")
    (f.textBox(center, "Center").
     font("16pt Arial").
     aligned("center").
     valigned("middle").
     colored("green").
     boxed("yellow"))
    return f

if __name__ == "__main__":
    import H5Gizmos as gz
    gz.serve(swatchDemo())