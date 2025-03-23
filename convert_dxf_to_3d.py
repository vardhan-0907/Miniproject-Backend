import ezdxf
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone

def convert_dxf_to_3d(dxf_path, model_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    points = [(e.dxf.location.x, e.dxf.location.y, 0) for e in msp.query("POINT")]
    
    if len(points) < 2:
        print("Not enough points for a 3D shape")
        return

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    # Define bottom-left and top-right points for the box
    p1 = gp_Pnt(min_x, min_y, 0)   # Bottom-left corner
    p2 = gp_Pnt(max_x, max_y, 10)  # Top-right corner

    # Create 3D box
    box = BRepPrimAPI_MakeBox(p1, p2).Shape()

    # Save to STEP file
    step_writer = STEPControl_Writer()
    step_writer.Transfer(box, STEPControl_AsIs)

    if step_writer.Write(model_path) == IFSelect_RetDone:
        print(f"3D Model saved: {model_path}")
    else:
        print("Failed to save 3D model")
