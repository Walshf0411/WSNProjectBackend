import os
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from .models import Image
from django.core.files import File

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_PATH = os.path.join(BASE_DIR, 'media')

# x cordinates and y coordinates respectively of the nodes.
# this is for plotting individual temprature sensor on the figure
x_coordinates = [2, 4, 6, 6, 4, 2]
y_coordinates = [2, 2, 2, 4, 4, 4]
# generate sizes for the makers
s = [20*4**4 for n in range(6)]
# coordinates of the nodes
NODES = {
    1: [2, 2],
    2: [4, 2], 
    3: [6, 2], 
    4: [6, 4], 
    5: [4, 4], 
    6: [2, 4],
}
EXTRA_POINTS = (
    (2, 6),
    (4, 6), 
    (6, 6), 
    (8, 6), 
    (8, 4), 
    (8, 2),
)
difference = 2
max_temp = 30
min_temp = 18
temp = None
avg_temp = None
threshold = 23.5

def get_key(coordinates):
    for key, node in NODES.items():
        if node == coordinates:
            return key
    return None

def get_temprature(node):
    if node[0] == 0 or node[1] == 0 or node[0] >= 6 or node[1] >= 6:
        return avg_temp
    else:
        value = temp[get_key(node) - 1]
        if value:
            return value
        else:
            return avg_temp

def normalize_temprature(temprature):
    return (temprature - min_temp) / (max_temp - min_temp)

def plot_individual_regions(set_of_nodes):
    if isinstance(set_of_nodes, dict):
        iterable = set_of_nodes.values()
    else:
        iterable = set_of_nodes
    
    for node in iterable:
        # the three points of the region
        adjacent = node[0] - difference, node[1] - difference
        left = node[0] - difference, node[1]
        below = node[0], node[1] - difference
        
        # get the temprature for each of the points
        temp_node = get_temprature(list(node))
        temp_adjacent = get_temprature(list(adjacent))
        temp_left = get_temprature(list(left))
        temp_below = get_temprature(list(below))
        
        # mean temprature of a block
        temprature_block = np.mean([temp_node, temp_adjacent, temp_left, temp_below])
        
        # finding the center of a region
        avg_x = np.mean([node[0], adjacent[0], left[0], below[0]])
        avg_y = np.mean([node[1], adjacent[1], left[1], below[1]])
        plt.xlim(0, 8)
        plt.ylim(0, 6)
        print(temprature_block)
        if temprature_block > threshold:
            plt.scatter([avg_x, ], [avg_y], c=[(1, 0, 0, normalize_temprature(temprature_block)), ], marker='s', s=s)
        else:
            plt.scatter([avg_x, ], [avg_y], c=[(0, 0, 1, normalize_temprature(temprature_block)), ], marker='s', s=s)
        
    
def do_visualization(temprature_data):
    global temp, avg_temp
    temp = temprature_data
    avg_temp = np.mean(temp)
    # initialize a figure
    plt.figure(figsize=(5.15, 4.))

    print("Threshold temprature: ", threshold)
    print("=" * 10, "Temprature of the blocks", "=" * 10)
    # plot the basic regions built by the temprature sensor
    plot_individual_regions(NODES)
    # plot the extra regiosns
    plot_individual_regions(EXTRA_POINTS)

    plt.scatter(x_coordinates, y_coordinates, c='blue', label="Temprature sensors")
    #plt.grid()
    plt.legend(handles=[
        Patch(facecolor=(1, 0, 0, normalize_temprature(avg_temp)), edgecolor='r', label='Temprature higher than threshold'),
        Patch(facecolor=(0, 0, 1, normalize_temprature(avg_temp)), edgecolor='r', label='Temprature lower than threshold'), 
        Line2D([0], [0], marker='o', color='w', label='Temprature Sensors', markerfacecolor='b', markersize=8),
    ])
    base_name = "temprature_profile.png"
    # generating an image path
    path_to_image = os.path.join(MEDIA_PATH, base_name)
    # saving the image at that path
    plt.savefig(path_to_image)

    # open the image to get an file object to create an entry for the image in the database
    image_file = File(open(path_to_image, "rb"), name=base_name)
    process = Image(image=image_file)
    Image.save(process)
    return process.image.url
