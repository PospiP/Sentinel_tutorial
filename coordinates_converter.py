""" 
Converts coordinates from GPS coorodinates (latitude/longitude - epsg:4326) from geojson file to any chosen epsg projection  
and saving these new coordinates to the new geojson file (new_file)
"""

import pyproj
import geojson
import json

def coor_converter(file, new_file, epsg):
    # Transformation from GPS coordinates to desired epsg projection
    transformer = pyproj.Transformer.from_crs("epsg:4326","epsg:"+str(epsg))
    
    # Open geojson file with GPS coordinates
    with open(file) as f:
        gj = geojson.load(f)
    
    # Load coordinates from geojson file
    cdnts = gj['features'][0]['geometry']['coordinates']
    
    # Transformation of coordinates
    k = 0
    n = len(cdnts)
    m = len(cdnts[0])
    trans_coord = [[0]*m for i in range(n)]
    for i in range(len(cdnts)):
        for j in range(len(cdnts[0])):
            [x1, y1] = cdnts[i][j]
            trans_coord[0][k] = transformer.transform(y1, x1)
            k += 1
    
    with open(file, 'r') as f:
        data = json.load(f)

    data['features'][0]['geometry']['coordinates'] = trans_coord
    
    with open(new_file, 'w+') as f:
        json.dump(data, f)
    
    print("The file {} has been saved!".format(new_file))
  