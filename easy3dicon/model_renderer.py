import cv2
import numpy as np
import pyvista as pv
from easy3dicon.generate_texture import generate_texture

def remove_transparent_rows_cols(image):
    # Separate the Alpha channel (transparency)
    alpha_channel = image[:, :, 3]
    # Find rows and columns that are not completely transparent
    non_transparent_rows = np.any(alpha_channel != 0, axis=1)
    non_transparent_cols = np.any(alpha_channel != 0, axis=0)
    # Remove completely transparent rows and columns
    return image[non_transparent_rows][:, non_transparent_cols]

def fill_transparent_areas(image, dominant_color):
    # Separate the Alpha channel (transparency)
    alpha_channel = image[:, :, 3]
    # Create a filled version of the image
    filled_image = image.copy()
    # Fill transparent areas with the dominant color
    filled_image[alpha_channel == 0] = [*dominant_color, 255]
    return filled_image

def generate_texture_coordinates(mesh):
    # Get the bounds of the mesh
    bounds = mesh.bounds
    x_min, x_max, y_min, y_max, _, _ = bounds

    # Normalize x and y coordinates to the range 0-1
    x = (mesh.points[:, 0] - x_min) / (x_max - x_min)
    y = (mesh.points[:, 1] - y_min) / (y_max - y_min)

    # Stack x and y coordinates to create texture coordinates
    texcoords = np.column_stack((x, y))

    # Add texture coordinates to the mesh
    mesh.active_t_coords = texcoords
    return mesh

def extract_and_extrude(icon_path, thickness=0.1):
    # Read the image (with Alpha channel)
    image = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise FileNotFoundError(f"File not found: {icon_path}")

    # Remove completely transparent rows and columns
    image = remove_transparent_rows_cols(image)

    # Separate the Alpha channel (transparency)
    alpha_channel = image[:, :, 3]

    # Binarize the image, making transparent parts black and non-transparent parts white
    _, binary = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Convert contours to 3D vertices and create a plane
    meshes = []
    for contour in contours:
        if len(contour) < 3:
            continue

        # Convert contour to 2D vertices
        points = np.array([[x, y] for [[x, y]] in contour], dtype=float)

        # Add Z axis to form a 3D polygon on the plane
        points = np.column_stack((points, np.zeros(points.shape[0])))

        # Create PyVista PolyData object and generate 2D plane
        base = pv.PolyData(points)
        base = base.delaunay_2d()

        # Extrude to form a 3D model
        extruded = base.extrude((0, 0, thickness))

        # Create top and bottom caps
        bottom = base
        top = pv.PolyData(points + [0, 0, thickness]).delaunay_2d()

        # Combine the extruded model, bottom, and top
        meshes.append(pv.MultiBlock([extruded, bottom, top]).combine())

    # Combine all small models into one
    combined = pv.MultiBlock(meshes).combine()

    # Generate texture coordinates for the combined mesh
    combined = generate_texture_coordinates(combined)

    generate_texture(icon_path)

    # Load the filled icon as a texture
    texture = pv.Texture('filled_temp.png')

    # Render the model with the filled texture
    plotter = pv.Plotter()
    plotter.add_mesh(combined, texture=texture, show_edges=False)

    plotter.add_axes()
    plotter.show_bounds()
    plotter.set_background('white')
    plotter.show()

def render_3d_model(path, thickness):
    extract_and_extrude(path, thickness)

if __name__ == '__main__':
    render_3d_model('temp.png', 100)