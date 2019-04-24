import os
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D
from .models import Image
from django.core.files import File
from WSN import settings

# generate sizes for the makers
s = [20*4**4 for n in range(settings.NUMBER_OF_NODES)]

difference = 2
max_temp = None
min_temp = None
temp = None
avg_temp = None
threshold = 22.5

def get_key(coordinates):
    for key, node in settings.NODES.items():
        if node == coordinates:
            return key
    return None

def get_temprature(node):
    if node[0] == 0 or node[1] == 0 or node[0] >= settings.NUMBER_OF_NODES or node[1] >= settings.NUMBER_OF_NODES:
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
    
    for i, node in enumerate(iterable):
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

        if isinstance(set_of_nodes, dict): 
            # if it is instance of dict then it means we are plotting the main blocks
            print("Block " + str(i + 1) + ": " +str(temprature_block))
        else:
            # if it is not an instance of dict it means that it is one of the extra nodes
            print("Block " + str(i + 1 + settings.NUMBER_OF_NODES) + ": " +str(temprature_block))

        if temprature_block > threshold:
            plt.scatter([avg_x, ], [avg_y], c=[(1, 0, 0, normalize_temprature(temprature_block)), ], marker='s', s=s)
        else:
            plt.scatter([avg_x, ], [avg_y], c=[(0, 0, 1, normalize_temprature(temprature_block)), ], marker='s', s=s)
        
    
def do_visualization(temprature_data):
    global temp, avg_temp, max_temp, min_temp, threshold
    temp = temprature_data
    avg_temp = np.mean(temp)
    
    threshold = avg_temp

    min_temp = min(temprature_data) - 2
    max_temp = max(temprature_data) + 2

    # initialize a figure
    plt.figure(figsize=(5.15, 4.))

    print("Threshold temperature: ", threshold)
    print("=" * 10, "Temperature of the blocks", "=" * 10)
    # plot the basic regions built by the temprature sensor
    plot_individual_regions(settings.NODES)
    # plot the extra regiosns
    plot_individual_regions(settings.EXTRA_POINTS)

    plt.scatter(settings.x_coordinates, settings.y_coordinates, c='blue', label="Temperature sensors")
    #plt.grid()
    plt.plot([7, 8, 7, 8, 7, 7], [1.5, 1.5, 1, 1, 1.5, 1], label='Entrance', color='g')
    plt.legend(handles=[
        Patch(facecolor=(1, 0, 0, 1), edgecolor='r', label='Temperature > '+str(threshold)),
        Patch(facecolor=(0, 0, 1, 1), edgecolor='b', label='Temperature < ' + str(threshold)), 
        Line2D([0], [0], marker='o', color='w', label='Temperature Sensors', markerfacecolor='b', markersize=8),
        Line2D([0], [0], lw=4, color='g', label='Entrance')
    ])

    base_name = "temprature_profile.png"
    # generating an image path
    path_to_image = os.path.join(settings.MEDIA_ROOT, base_name)
    # saving the image at that path
    plt.savefig(path_to_image)

    # open the image to get an file object to create an entry for the image in the database
    image_file = File(open(path_to_image, "rb"), name=base_name)
    process = Image(image=image_file)
    Image.save(process)
    return process.image.url
