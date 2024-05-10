# based on   
# https://towardsdatascience.com/3d-data-processing-with-open3d-c3062aadc72e
# https://github.com/isl-org/Open3D/discussions/6706
# https://stackoverflow.com/questions/62912397/open3d-visualizing-multiple-point-clouds-as-a-video-animation
# http://www.open3d.org/docs/0.8.0/tutorial/Advanced/non_blocking_visualization.html

# open3d repo -> examples/python/visualization/non_blocking_visualization.py

import open3d as o3d
import numpy as np
import cv2

from PIL import Image
import copy
import os
import time
import threading
from functools import partial

# Global variable to control the main loop
keep_running = True

# find current_directory
current_directory = os.path.dirname(os.path.abspath(__file__))

o3d.__version__

def visualize___candel(mesh):
    #vis = o3d.visualization.Visualizer()
    vis = o3d.visualization.VisualizerWithKeyCallback()
    #vis.register_key_callback(ord('q'), key_callback)

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

def animate_mesh1(mesh, vis):
    translation_step = 0.1  # Define the step size for translation
    total_translation = -5  # Define the total translation along X-axis
    num_iterations = int(abs(total_translation) / translation_step)  # Calculate number of iterations
    
    for _ in range(num_iterations):
        translation_matrix = np.identity(4)
        translation_matrix[0, 3] -= translation_step  # Move mesh by translation_step units along the negative X-axis
        mesh.transform(translation_matrix)
        
        # Update visualization
        vis.update_geometry(mesh)
        vis.poll_events()
        vis.update_renderer()
        time.sleep(0.01)  # Add a small delay for smoother animation

def animate_mesh(mesh, vis):
    translation_step = 0.1  # Define the step size for translation
    total_translation = -5  # Define the total translation along X-axis
    num_iterations = int(abs(total_translation) / translation_step)  # Calculate number of iterations
    
    for _ in range(num_iterations):
        translation_matrix = np.identity(4)
        translation_matrix[0, 3] -= translation_step  # Move mesh by translation_step units along the negative X-axis
        mesh.transform(translation_matrix)
        
        # Update visualization
        vis.update_geometry(mesh)
        vis.poll_events()
        vis.update_renderer()

def key_callback(vis):
    global keep_running
    keep_running = False
    print("Hello")
    #global keep_running
    #if key == ord('q') and action == o3d.visualization.KeyEvent.Action.UP:



def main():
    global keep_running

    #vis = o3d.visualization.Visualizer()
    vis = o3d.visualization.VisualizerWithKeyCallback()

    vis.register_key_callback(ord('Q'),partial( key_callback))

    vis.create_window()

    Pirooz_mesh = o3d.io.read_triangle_mesh(os.path.join(current_directory, 'data/01-TeslaModelSplaid.obj'))
    Env_Car1_mesh=o3d.io.read_triangle_mesh(os.path.join(current_directory, 'data/02-Vehicle-01-VanCar.obj'))
    Man1_mesh=o3d.io.read_triangle_mesh(os.path.join(current_directory, 'data/03-Man01.obj')  )
    
    #region Initializing Models
    ######################################## Pirooz_mesh -> Start
    x_theta = deg2rad(0)
    y_theta = deg2rad(90)
    z_theta = deg2rad(0)

    Pirooz_mesh = get_rotated_mesh(Pirooz_mesh, x_theta, y_theta, z_theta)
    Pirooz_mesh.paint_uniform_color([255, 0, 0])
    ######################################## Pirooz_mesh -> End
    ######################################## 02-Vehicle-01-VanCar -> Start
    Env_Car1_mesh = get_rotated_mesh(Env_Car1_mesh, deg2rad(0), deg2rad(180), deg2rad(0))
    Env_Car1_mesh.scale(0.2 ,center=np.array([0.0, 0.0, 0.0])) 
    
    translation_matrix = np.identity(4)
    translation_matrix[1, 3] = -2  # 4 units along the negative Y-axis
    Env_Car1_mesh.transform(translation_matrix)
    ######################################## 02-Vehicle-01-VanCar -> End
    ######################################## 03-Man01 -> Start
    
    Man1_mesh = get_rotated_mesh(Man1_mesh, deg2rad(-90), deg2rad(0), deg2rad(0))
    Man1_mesh = get_rotated_mesh(Man1_mesh, deg2rad(0), deg2rad(90), deg2rad(0))
    Man1_mesh.scale(2 ,center=np.array([0.0, 0.0, 0.0])) 

    translation_matrix2 = np.identity(4)
    translation_matrix2[2, 3] = -5.3  # 20 units along Z-axis
    Man1_mesh.transform(translation_matrix2)

    translation_matrix2 = np.identity(4)
    translation_matrix2[0, 3] = -2.5  # Move 2 units along the X-axis
    Man1_mesh.transform(translation_matrix2)

    ######################################## 03-Man01 -> End

    

    Pirooz_mesh.compute_vertex_normals()
    Env_Car1_mesh.compute_vertex_normals()
    Man1_mesh.compute_vertex_normals()
    #endregion

    #region organize scene

        #region coordinate
    # Creating a mesh of the XYZ axes Cartesian coordinates frame. This mesh will show the directions in which the X, Y & Z-axes point, and 
    # can be overlaid on the 3D mesh to visualize its orientation in the Euclidean space.
    # X-axis : Red arrow
    # Y-axis : Green arrow
    # Z-axis : Blue arrow
    mesh_coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=12, origin=[0, 0, 0])
    #endregion coordinate   

    #endregion

    #region texts on 3D

    # Create text mesh "Hello Open3D"
    hello_open3d_mesh = o3d.t.geometry.TriangleMesh.create_text("Vector Space v1.0", depth=0.1).to_legacy()
    hello_open3d_mesh.paint_uniform_color((0.4, 0.1, 0.9))

    # Define the location for the text mesh
    location = (1, 3, 6)
    hello_open3d_mesh.transform([[0.1, 0, 0, location[0]], [0, 0.1, 0, location[1]], [0, 0, 0.1, location[2]], [0, 0, 0, 1]])

    vis.add_geometry(hello_open3d_mesh)

    #endregion

    #region Organize Scene
    translation_matrix = np.identity(4)
    translation_matrix[2, 3] = -20  # 20 units along Z-axis
    Env_Car1_mesh.transform(translation_matrix)

    translation_matrix2 = np.identity(4)
    translation_matrix2[2, 3] = 20  # 20 units along Z-axis
    Man1_mesh.transform(translation_matrix2)
    #endregion
  


    #draw_geoms_list = [mesh_coord_frame, Pirooz_mesh]
    #vis.add_geometry(draw_geoms_list)
    vis.add_geometry(mesh_coord_frame)
    vis.add_geometry(Pirooz_mesh)
    vis.add_geometry(Env_Car1_mesh)
    vis.add_geometry(Man1_mesh)

    ctr = vis.get_view_control()
    ctr.rotate(-5.0, 0, 0)  # Rotate around X-axis
    ctr.rotate(0, -5.0, 0)  # Rotate around Y-axis

    #o3d.visualization.draw_geometries(draw_geoms_list)
    #vis.update_geometry()
    
    #vis.poll_events()
    #vis.update_renderer()



    # Start animation thread for Pirooz_mesh
    #animation_thread = threading.Thread(target=animate_mesh, args=(Pirooz_mesh, vis))
    #animation_thread.daemon = True  # Make the thread a daemon so it exits when the main thread exits
    #animation_thread.start()

    

    #vis = o3d.visualization.VisualizerWithKeyCallback()

    #vis.register_key_action_callback(ord('q'), key_callback)


    #while True:
    while keep_running:
        print(keep_running)
        #vis.poll_events()

        animate_mesh(Pirooz_mesh, vis)
        print('---')

        # Break the loop if 'q' is pressed 
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     print('aaa')
        #     break 

    # Run the visualization
    #vis.run()
    vis.destroy_window()



if __name__ == "__main__":
    main()

