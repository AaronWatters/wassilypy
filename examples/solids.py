
from wassilypy import cube, CubeView
import H5Gizmos as gz
import numpy as np

JSON ={
  "source_note": "Coordinates are centered at origin. Faces are CCW as seen from outside for a typical right-handed basis (minor variations in ordering are usually harmless).",
  "solids": {
    "tetrahedron": {
      "name": "tetrahedron",
      "vertex": [[1,1,1],[-1,-1,1],[-1,1,-1],[1,-1,-1]],
      "face": [[0,1,3],[0,2,1],[0,3,2],[1,2,3]],
      "edge": [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    },
    "cube": {
      "name": "cube",
      "vertex": [[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]],
      "face": [[0,4,6,2],[0,1,5,4],[0,2,3,1],[7,6,4,5],[7,5,1,3],[7,3,2,6]],
      "edge": [[0,1],[0,2],[0,4],[1,3],[1,5],[2,3],[2,6],[3,7],[4,5],[4,6],[5,7],[6,7]]
    },
    "octahedron": {
      "name": "octahedron",
      "vertex": [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],
      "face": [[0,2,4],[0,4,3],[0,3,5],[0,5,2],[1,4,2],[1,3,4],[1,5,3],[1,2,5]],
      "edge": [[0,2],[0,3],[0,4],[0,5],[1,2],[1,3],[1,4],[1,5],[2,4],[2,5],[3,4],[3,5]]
    },
    "icosahedron": {
      "name": "icosahedron",
      "vertex": [[-1,1.618034,0],[1,1.618034,0],[-1,-1.618034,0],[1,-1.618034,0],[0,-1,1.618034],[0,1,1.618034],[0,-1,-1.618034],[0,1,-1.618034],[1.618034,0,-1],[1.618034,0,1],[-1.618034,0,-1],[-1.618034,0,1]],
      "face": [[0,1,5],[0,5,11],[0,7,1],[0,10,7],[0,11,10],[1,7,8],[1,8,9],[1,9,5],[2,3,6],[2,4,3],[2,6,10],[2,10,11],[2,11,4],[3,4,9],[3,8,6],[3,9,8],[4,5,9],[4,11,5],[6,8,7],[6,7,10]],
      "edge": [[0,1],[0,5],[0,7],[0,10],[0,11],[1,5],[1,7],[1,8],[1,9],[2,3],[2,4],[2,6],[2,10],[2,11],[3,4],[3,6],[3,8],[3,9],[4,5],[4,9],[4,11],[5,9],[5,11],[6,7],[6,8],[6,10],[7,8],[7,10],[8,9],[10,11]]
    },
    "dodecahedron": {
      "name": "dodecahedron",
      "vertex": [[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1],[0,-0.618034,-1.618034],[0,-0.618034,1.618034],[0,0.618034,-1.618034],[0,0.618034,1.618034],[-0.618034,-1.618034,0],[-0.618034,1.618034,0],[0.618034,-1.618034,0],[0.618034,1.618034,0],[-1.618034,0,-0.618034],[-1.618034,0,0.618034],[1.618034,0,-0.618034],[1.618034,0,0.618034]],
      "face": [[0,8,10,2,16],[0,12,14,4,8],[0,16,17,1,12],[1,9,5,14,12],[1,17,3,11,9],[2,10,6,15,3],[2,3,17,16,18],[4,14,5,19,18],[4,18,6,10,8],[5,9,11,7,19],[6,18,19,7,15],[7,11,3,15,19]],
      "edge": [[0,8],[0,12],[0,16],[1,9],[1,12],[1,17],[2,10],[2,16],[2,17],[3,11],[3,15],[3,17],[4,8],[4,14],[4,18],[5,9],[5,14],[5,19],[6,10],[6,15],[6,18],[7,11],[7,15],[7,19],[8,10],[12,14],[16,17],[18,19],[9,11],[14,5]]
    }
  }
}

async def solidDiagram(target = "icosahedron", onFrame=None):
    target_info = JSON["solids"][target]
    target_vertices = target_info["vertex"]
    target_faces = target_info["face"]
    target_edges = target_info["edge"]
    center = np.array([0,0,0])
    if onFrame is not None:
        f = onFrame
    else:
        f = await cube(900, 8, modelCenter=center, perspective=True)
    f.lookFrom(eyePoint=[-2,-1,-2.5])
    f.clear()
    for face in target_faces:
        face_verts = [target_vertices[i] for i in face]
        polygon = f.polygon(face_verts).normalColored(alpha=0.7)
    for edge in target_edges:
        edge_verts = [target_vertices[i] for i in edge]
        line = f.line(edge_verts[0], edge_verts[1]).linedWidth(2).colored("black")
    for v in target_vertices:
        point = f.circle(v, 0.03).filled().colored("red")
    f.fit(border=60)
    f.orbit()
    return f

solidsInfo = JSON["solids"]
solidsNames = list(solidsInfo.keys())

async def allSolids():
    D = gz.DropDownSelect(
        label_value_pairs = solidsNames,
        selected_value=solidsNames[0],
        legend="Solid: ",
    )
    D.resize(width=300, height=100)
    C = CubeView(900, 8, modelCenter=[0,0,0], perspective=True)
    def fitDiagram(*ignored):
        C.frame.fit(border=60)
    fitButton = gz.Button("Fit Diagram", on_click=fitDiagram)
    dashboard = gz.Stack([
        D, 
        C.diagram,
        fitButton,
        "Solid Viewer Demo: drag over the diagram to rotate.",])
    await dashboard.link()
    await solidDiagram(target=solidsNames[0], onFrame=C.frame)
    def onSelectChange(*ignored):
        [selected_value] = D.selected_values
        gz.schedule_task(solidDiagram(target=selected_value, onFrame=C.frame))
    D.set_on_click(onSelectChange)


if __name__ == "__main__":
    #gz.serve(solidDiagram())
    gz.serve(allSolids())