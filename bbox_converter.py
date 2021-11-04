""" 
Converts coordinates as BoundingBox from GPS coorodinates (latitude/longitude - epsg:4326) from geojson file to any chosen epsg projection  
and saving these new coordinates to the new geojson file (new_file)
"""

import json
import geojson
import rasterio
from rasterio import warp
from use_functions import generate_polygon, pol_to_bounding_box

def bbox_converter(file, new_file, epsg):
    # Loading coordinates lat/long
    with open(file) as f:
        gj = geojson.load(f)
    
    cord = gj['features'][0]['geometry']['coordinates']

    k = 0
    cord_list = [[0] for i in range(len(cord[0]))]
    for i in range(len(cord)):
        for j in range(len(cord[0])):
            cord_list[k] = cord[i][j]
            k += 1

    bbox = pol_to_bounding_box(cord_list)
    
    bounds_trans = warp.transform_bounds({'init': 'epsg:4326'},"epsg:"+str(epsg),*bbox)
    pol_bounds_trans = generate_polygon(bounds_trans)
    
    k = 0
    n = 1
    m = len(pol_bounds_trans)
    matrix_coord = [[0]*m for i in range(n)]
    for cor in pol_bounds_trans:
        matrix_coord[0][k] = pol_bounds_trans[k]
        k += 1
    
    with open(file, 'r') as f:
        data = json.load(f)

    data['features'][0]['geometry']['coordinates'] = matrix_coord
    
    with open(new_file, 'w+') as f:
        json.dump(data, f)
    
    print("The file {} has been saved!".format(new_file))