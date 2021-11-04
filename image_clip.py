"""
This function clipped all images in specified folder according to the geojson file and save output to specified folder
"""


import os
import fiona
import rasterio
from rasterio.mask import mask

def clipper(image_path, geojson, new_folder):
    file_list = os.listdir(image_path)
    file_list.sort()

    # use fiona to open our map ROI GeoJSON
    with fiona.open(geojson) as f:
        aoi = [feature["geometry"] for feature in f]
    
    # Load every image from the list
    k = 0
    for image in file_list:
        with rasterio.open(image_path + image) as img:
            clipped, transform = mask(img, aoi, crop=True)
    
        meta = img.meta.copy()
    
        meta.update({"driver": "GTiff", "transform": transform,"height":clipped.shape[1],"width":clipped.shape[2]})
    
        # Save clipped images in the file
        new_fold = new_folder + file_list[k][file_list[k].rfind('_')+1:file_list[k].rfind('.')] + '.tif'
    
        with rasterio.open(new_fold, 'w', **meta) as dst:
            dst.write(clipped)
    
        k += 1
    
    print("All clipped images are saved in {} folder!".format(new_folder))