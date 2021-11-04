
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from pathlib import Path
from rasterio.enums import Resampling
from rasterio.plot import adjust_band

def load_sentinel_image(img_folder, bands):
    image = {}
    path = Path(img_folder)
    for band in bands:
        file = img_folder + band + ".tif" 
        #print(f'Opening file {file}')
        ds = rasterio.open(file)
        image.update({band: ds.read(1)})

    return image

def display_rgb(img, b_r, b_g, b_b, alpha=1., figsize=(10, 10)):
    rgb = np.stack([img[b_r], img[b_g], img[b_b]], axis=-1)
    rgb = rgb/rgb.max() * alpha
    plt.figure(figsize=figsize)
    plt.imshow(rgb)
    plt.axis("off")
    
def image_rgb(img, b_r, b_g, b_b, alpha=1.):
    rgb = np.stack([img[b_r], img[b_g], img[b_b]], axis=-1)
    rgb = adjust_band(rgb)
    rgb = rgb/rgb.max() * alpha
    return rgb

def resampling_20(folder, file, new_folder):
    upscale_factor = 2
    
    with rasterio.open(folder + file) as dataset:
        # resample data to target shape
        data = dataset.read(out_shape=(dataset.count,
                                       int(dataset.height * upscale_factor),
                                       int(dataset.width * upscale_factor)
                                      ),
                            resampling=Resampling.cubic)
    # scale image transform
    transform = dataset.transform * dataset.transform.scale(
        (dataset.width / data.shape[-1]),
        (dataset.height / data.shape[-2])
    )
    
    resample = data.reshape(data.shape[0]*(data.shape[1], data.shape[0]*data.shape[2]))
    res_del = np.delete(resample,0,1)
    
    new_array = np.asarray(res_del).reshape(1,res_del.shape[0], res_del.shape[1])
    
    meta = dataset.meta.copy()
    
    meta.update({ "transform": transform, "height":new_array.shape[1],"width":new_array.shape[2]})
    
    with rasterio.open(new_folder+file, 'w+', **meta) as dst:
            dst.write(new_array)
    
    return new_array 

def resampling_60(folder, file, new_folder):
    upscale_factor = 6
    
    with rasterio.open(folder + file) as dataset:
        # resample data to target shape
        data = dataset.read(out_shape=(dataset.count,
                                       int(dataset.height * upscale_factor),
                                       int(dataset.width * upscale_factor)
                                      ),
                            resampling=Resampling.cubic)
    # scale image transform
    transform = dataset.transform * dataset.transform.scale(
        (dataset.width / data.shape[-1]),
        (dataset.height / data.shape[-2])
    )
    
    resample = data.reshape(data.shape[0]*(data.shape[1], data.shape[0]*data.shape[2]))
    res_del = np.delete(resample,range(0,4),0)
    res_del = np.delete(res_del,range(0,7),1)
    
    new_array = np.asarray(res_del).reshape(1,res_del.shape[0], res_del.shape[1])
    
    meta = dataset.meta.copy()
    
    meta.update({ "transform": transform, "height":new_array.shape[1],"width":new_array.shape[2]})
    
    with rasterio.open(new_folder+file, 'w+', **meta) as dst:
            dst.write(new_array)
    
    return new_array 

def normalized_difference(img, b1, b2, eps=0.0001):
    band1 = np.where((img[b1]==0) & (img[b2]==0), np.nan, img[b1])
    band2 = np.where((img[b1]==0) & (img[b2]==0), np.nan, img[b2])
    
    return (band1 - band2) / (band1 + band2)

def plot_masked_rgb(red, green, blue, mask, color_mask=(1, 0, 0), transparency=0.5, brightness=2):
    
    # to improve our visualization, we will increase the brightness of our values
    red = red / red.max() * brightness
    green = green / green.max() * brightness
    blue = blue / blue.max() * brightness
    
    red = np.where(mask==True, red*transparency+color_mask[0]*(1-transparency), red)
    green = np.where(mask==True, green*transparency+color_mask[1]*(1-transparency), green)
    blue = np.where(mask==True, blue*transparency+color_mask[2]*(1-transparency), blue)
    
    rgb = np.stack([red, green, blue], axis=2)
    
    return rgb