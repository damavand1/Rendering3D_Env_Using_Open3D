# based on   
# https://towardsdatascience.com/3d-data-processing-with-open3d-c3062aadc72e
# https://github.com/isl-org/Open3D/discussions/6706
# https://stackoverflow.com/questions/62912397/open3d-visualizing-multiple-point-clouds-as-a-video-animation

import open3d as o3d
import numpy as np

from PIL import Image
import copy
import os

# # Load stereo images
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Load stereo images
# img_left =cv2.imread( os.path.join(current_directory, 'B.jpg'))

o3d.__version__

def visualize(mesh):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    vis.run()
    vis.destroy_window()

# Defining a function to create a custom animation for the visualizations.

def deg2rad(deg):
    return deg * np.pi/180

def custom_animation(vis):
    
    global i
    #global imgs_list
    
    if i == 0:
        ctr = vis.get_view_control()
        ctr.scale(-5)
        i+=1
        return False
    
    elif i <= 446:
        y = 4*np.sin(deg2rad((i-1)/(223/360)))
        
        ctr = vis.get_view_control()
        ctr.rotate(-5.0, y)
        
    else:
        vis.close()
    
    # vis.capture_screen_image(f"images/sample_image_{i}.png", do_render=False)
    img = vis.capture_screen_float_buffer()
    img = (255 * np.asarray(img)).astype(np.uint8)
    img = Image.fromarray(img).convert("RGB")
    #imgs_list.append(img)
    
    i += 1
    
    return False

def get_rotated_mesh(mesh, x_theta, y_theta, z_theta):
    
    """Rotate the 3D mesh about the X, Y & Z-axes.
    
    Args:
        mesh: An open3d.geometry.TriangleMesh object.
        x_theta: (float) An angle value in radians to rotate the mesh about the X-axis.
        y_theta: (float) An angle value in radians to rotate the mesh about the Y-axis.
        z_theta: (float) An angle value in radians to rotate the mesh about the Z-axis.
        
    Returns:
        mesh_rotated: The rotated 3D mesh as a open3d.geometry.TriangleMesh object.
    """
    
    mesh_rotated = copy.deepcopy(mesh)
    R = mesh_rotated.get_rotation_matrix_from_axis_angle([x_theta, y_theta, z_theta])
    mesh_rotated.rotate(R, center=(0, 0, 0))
    
    return mesh_rotated


i = 0
def main():
    mesh_path ="0 handwrite detector/0Temp/data/3d_model.obj"

    Pirooz_mesh = o3d.io.read_triangle_mesh(mesh_path)
    #visualize(mesh)

    Pirooz_mesh.compute_vertex_normals()

    #region coordinate
    # Creating a mesh of the XYZ axes Cartesian coordinates frame. This mesh will show the directions in which the X, Y & Z-axes point, and 
    # can be overlaid on the 3D mesh to visualize its orientation in the Euclidean space.
    # X-axis : Red arrow
    # Y-axis : Green arrow
    # Z-axis : Blue arrow
    mesh_coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=12, origin=[0, 0, 0])
    #endregion coordinate   

    #region Pirooz & coordinate

    #Pirooz_mesh.paint_uniform_color([255, 255, 255])

    x_theta = deg2rad(0)
    y_theta = deg2rad(90)
    z_theta = deg2rad(0)

    Pirooz_mesh = get_rotated_mesh(Pirooz_mesh, x_theta, y_theta, z_theta)

    draw_geoms_list = [mesh_coord_frame, Pirooz_mesh]
    o3d.visualization.draw_geometries(draw_geoms_list)


    #o3d.visualization.draw_geometries_with_animation_callback(draw_geoms_list, custom_animation)
    #endregion

    #region Draw Pirooz
   
    
    #mesh

    # Visualizing the mesh with the estimated surface normals.
    #draw_geoms_list = [mesh]
    #o3d.visualization.draw_geometries(draw_geoms_list)
    #endregion aaaa

main()