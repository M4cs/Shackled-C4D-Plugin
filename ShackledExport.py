import c4d
from c4d import gui
import json
import os

# Shackled Renderer script for exporting Cinema 4D Objects
# Caveats:

# Must have Studio version of Cinema 4D. It seems lite and S versions
# are missing the Mesh > Commands tab. If you can retriangulate your mesh
# another way, please do let me know @maxbridgland. 
#
# For now, you'll need to retriangulate your mesh and add the Vertex Color
# tag to the object. Refer to the tutorial video if you get lost!
# Feel free to contact me on Discord: macs#0420 with any questions.

output_folder = "D:/Shackled"

try:
    os.makedirs(output_folder)
except:
    pass


# Main function
def main():
    so = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER | c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    
    for o in so:
        verts = []
        cols = []
        
        verts_local = [x for x in o.GetAllPoints()]
        for i, vert in enumerate(verts_local):
            fac = 10
            v0 = int(fac * vert[0])
            v1 = int(fac * vert[1])
            v2 = int(fac * vert[2])
            verts.append([v0,v1,v2])
        
        try:
            color_tag = o.GetTag(c4d.Tvertexcolor)
            data = color_tag.GetDataAddressR()
        
            for idx in range(o.GetPointCount()):
                color = c4d.VertexColorTag.GetColor(data, None, None, idx)
                cols.append(
                    [int(255 * color[0]), int(255 * color[1]), int(255 * color[2])]
                )
        except:
            default_color = [255, 0, 0]
            for i in range(o.GetPointCount()):
                cols.append(
                    default_color
                )
            
        faces = []
        for i, face in enumerate(o.GetAllPolygons()):
            faces.append([face.a, face.b, face.c])
            
        dct = {
            "name": "",
            "description": "",
            "canvasDim": 128,
            "rotation": [0,0,0],
            "renderParams": {
                "backfaceCulling": False,
                "wireframe": False,
                "perspCamera": True,
                "invert": False,
                "objPosition": [0,0,-2000],
                "objScale": 10,
                "backgroundColor": [[255,255,255], [255,255,255]],
                "lightingParams": {
                    "applyLighting": False,
                    "lightAmbiPower": 0,
                    "lightDiffPower": 60000000,
                    "lightSpecPower": 60000000,
                    "inverseShininess": 10,
                    "lightPos": [-200,0,-2000],
                    "lightColAmbi": [255, 255, 255],
                    "lightColSpec": [6, 6, 6],
                    "lightColDiff": [2, 2, 2],
                }
            },
            "verts": verts,
            "cols": cols, 
            "faces": faces
        }
        
        print "Generated Shackled Render File with {} vertices, {} faces, and {} colors.".format(
            len(verts), len(faces), len(cols)
        )
        
        fp_out = "{}/{}.json".format(output_folder, o.GetName())
        with open(fp_out, "w") as f:
            json.dump(dct, f, indent=4)

# Execute main()
if __name__=='__main__':
    main()
