import cv2
import numpy as np
import ezdxf

def convert_image_to_dxf(image_path, dxf_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 50, 150)

    doc = ezdxf.new()
    msp = doc.modelspace()

    for y in range(edges.shape[0]):
        for x in range(edges.shape[1]):
            if edges[y, x] > 0:
                msp.add_point((x, -y))

    doc.saveas(dxf_path)
    print(f"DXF saved: {dxf_path}")
