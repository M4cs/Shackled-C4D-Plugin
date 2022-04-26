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

class SuccessDialog(gui.GeDialog):
    def __init__(self, path):
        self.path = path   


    def CreateLayout(self):
        self.SetTitle("Export Complete!")
        self.GroupBegin(1, c4d.BFH_SCALEFIT, 1, 3)
        self.AddStaticText(2, c4d.BFH_SCALEFIT, name="Export has completed successfully!")
        self.AddStaticText(3, c4d.BFH_SCALEFIT, name="Path Exported: {}".format(self.path))
        self.AddButton(4, c4d.BFH_SCALEFIT, name="Close", initw=70, inith=0)
        self.EndGroup()

    def Command(self, id, msg):
        if id==4:
            self.Close()
        return True



def export(args):
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
            "rotation": args['rot'],
            "renderParams": {
                "backfaceCulling": False,
                "wireframe": False,
                "perspCamera": True,
                "invert": False,
                "objPosition": args['pos'],
                "objScale": args['scale'],
                "backgroundColor": [args['bg']['top'], args['bg']['bottom']],
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
        sdlg = SuccessDialog(fp_out)
        sdlg.Open(c4d.DLG_TYPE_MODAL, defaultw=170, defaulth=50)
   
class ExportDialog(gui.GeDialog):

    SCALE_FIELD = 1339

    SCALE_INPUT = 1338

    
    POS_FIELD = 1220
    POS_X_INPUT = 1221
    POS_Y_INPUT = 1222
    POS_Z_INPUT = 1223   
    
    ROT_FIELD = 1330
    ROT_X_INPUT = 1331
    ROT_Y_INPUT = 1332
    ROT_Z_INPUT = 1333 
    
    BG_T_FIELD = 1440
    BG_B_FIELD = 1447
    BG_T_R_INPUT = 1441
    BG_T_G_INPUT = 1442
    BG_T_B_INPUT = 1443
    BG_B_R_INPUT = 1444
    BG_B_G_INPUT = 1445
    BG_B_B_INPUT = 1446

    CANCEL_BUTTON = 88330
    EXPORT_BUTTON = 187831

    def CreateLayout(self):
        self.SetTitle("Shackled Export Settings")
        
        self.GroupBegin(1, c4d.BFH_SCALEFIT, 3, 1, title="Object Settings")
        self.GroupBorder(c4d.BORDER_ACTIVE_1)
        self.GroupBorderSpace(10, 10, 10, 10)
        self.AddStaticText(self.SCALE_FIELD, c4d.BFH_LEFT, name="Scale:")
        self.AddStaticText(self.SCALE_FIELD, c4d.BFH_LEFT, name="", initw=70)
        self.AddEditNumberArrows(self.SCALE_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(self.POS_FIELD, c4d.BFH_LEFT, name="Position:")
        self.AddStaticText(66670, c4d.BFH_RIGHT, name="x")
        self.AddEditNumber(self.POS_X_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(66667, c4d.BFH_LEFT, name="")
        self.AddStaticText(66668, c4d.BFH_RIGHT, name="y")
        self.AddEditNumber(self.POS_Y_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(66669, c4d.BFH_LEFT, name="")
        self.AddStaticText(66670, c4d.BFH_RIGHT, name="z")
        self.AddEditNumber(self.POS_Z_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(self.ROT_FIELD, c4d.BFH_LEFT, name="Rotation:")
        self.AddStaticText(16670, c4d.BFH_RIGHT, name="x")
        self.AddEditNumber(self.ROT_X_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(16667, c4d.BFH_LEFT, name="")
        self.AddStaticText(16668, c4d.BFH_RIGHT, name="y")
        self.AddEditNumber(self.ROT_Y_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(16669, c4d.BFH_LEFT, name="")
        self.AddStaticText(16670, c4d.BFH_RIGHT, name="z")
        self.AddEditNumber(self.ROT_Z_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.GroupEnd()
        
        self.GroupBegin(2, c4d.BFH_SCALEFIT, 3, 1, title="Background Settings")
        self.GroupBorder(c4d.BORDER_ACTIVE_4)
        self.GroupBorderSpace(10, 10, 10, 10)
        self.AddStaticText(self.BG_T_FIELD, c4d.BFH_LEFT, name="Top:", initw=70)
        self.AddStaticText(45422, c4d.BFH_RIGHT, name="R", initw=70)
        self.AddEditNumber(self.BG_T_R_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(166339, c4d.BFH_SCALEFIT, name="")
        self.AddStaticText(45324422, c4d.BFH_RIGHT, name="G", initw=70)
        self.AddEditNumber(self.BG_T_G_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(1626339, c4d.BFH_SCALEFIT, name="")
        self.AddStaticText(4324422, c4d.BFH_RIGHT, name="B", initw=70)
        self.AddEditNumber(self.BG_T_B_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(self.BG_B_FIELD, c4d.BFH_LEFT, name="Bottom:", initw=70)
        self.AddStaticText(456422, c4d.BFH_RIGHT, name="R", initw=70)
        self.AddEditNumber(self.BG_B_R_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(1668339, c4d.BFH_SCALEFIT, name="")
        self.AddStaticText(453924422, c4d.BFH_RIGHT, name="G", initw=70)
        self.AddEditNumber(self.BG_B_G_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.AddStaticText(162639939, c4d.BFH_SCALEFIT, name="")
        self.AddStaticText(43254422, c4d.BFH_RIGHT, name="B", initw=70)
        self.AddEditNumber(self.BG_B_B_INPUT, c4d.BFH_RIGHT, initw=70, inith=0)
        self.GroupEnd()
        
        self.GroupBegin(3, c4d.BFH_SCALEFIT, 2, 1)
        self.GroupBorder(c4d.BORDER_WITH_TITLE_BOLD)
        self.GroupBorderSpace(10, 10, 10, 10)
        self.AddButton(self.CANCEL_BUTTON, c4d.BFH_SCALE, name="Cancel")
        self.AddButton(self.EXPORT_BUTTON, c4d.BFH_SCALE, name="Export")
        self.GroupEnd()
        return True
        
    def InitValues(self):
        self.SetLong(self.SCALE_INPUT, 1)
        self.SetLong(self.POS_Z_INPUT, -2000)
        self.SetLong(self.BG_T_R_INPUT, 35)
        self.SetLong(self.BG_T_G_INPUT, 35)
        self.SetLong(self.BG_T_B_INPUT, 35)
        self.SetLong(self.BG_B_R_INPUT, 5)
        self.SetLong(self.BG_B_G_INPUT, 5)
        self.SetLong(self.BG_B_B_INPUT, 5)
        return True
    
    def Command(self, id, msg):
        if id==self.CANCEL_BUTTON:
            self.Close()
        elif id==self.EXPORT_BUTTON:
            args = {
                'scale': self.GetInt32(self.SCALE_INPUT),
                'pos': [
                    self.GetLong(self.POS_X_INPUT),
                    self.GetLong(self.POS_Y_INPUT),
                    self.GetLong(self.POS_Z_INPUT)
                ],
                'rot': [
                    self.GetLong(self.ROT_X_INPUT),
                    self.GetLong(self.ROT_Y_INPUT),
                    self.GetLong(self.ROT_Z_INPUT)
                ],
                'bg': {
                    'top': [
                        self.GetLong(self.BG_T_R_INPUT),
                        self.GetLong(self.BG_T_G_INPUT),
                        self.GetLong(self.BG_T_B_INPUT),
                    ],
                    'bottom': [
                        self.GetLong(self.BG_B_R_INPUT),
                        self.GetLong(self.BG_B_G_INPUT),
                        self.GetLong(self.BG_B_B_INPUT),
                    ]
                }
            }
            export(args)
        return True

# Main function
def main():
    dlg = ExportDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=170, defaulth=50)

# Execute main()
if __name__=='__main__':
    main()
