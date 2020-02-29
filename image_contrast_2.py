# This is a temporary file for testing methods of applying image contrast
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

# For visualization
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
from numpy import *
from skimage import exposure
import cv2

def PIL_contrast(image_name, scale):
    """
    Converts image to BW then Contrasts the image
    params:
        image_name  filepath of an image
        scale: factor of enhancement
    For contrast, an enhancement factor of 0.0 gives a solid grey image.
    A factor of 1.0 gives the original image.
    Factor of > 1.0 gives a more contrasted image
    docs: https://pillow.readthedocs.io/en/3.0.x/reference/ImageEnhance.html
    """
    # Change input here
    im = Image.open(image_name)
    # Convert image to BW
    bw_im = im.convert('LA')
    # contrast the image
    enhancer = ImageEnhance.Contrast(bw_im)
    enhanced_im = enhancer.enhance(scale)
    enhanced_im.save("contrasted.png")
    return enhanced_im

def PIL_sharpen(image_name):
    # Change input here
    im = Image.open(image_name)
    # Convert image to BW
    bw_im = im.convert('LA')
    # Apply sharp filter
    sharpened1 = bw_im.filter(ImageFilter.SHARPEN);
    sharpened2 = sharpened1.filter(ImageFilter.SHARPEN);
    sharpened2.save("sharpened.png")
    return sharpened2

def normalize(image_name):
    """
    Guide: https://machinelearningmastery.com/how-to-manually-scale-image-pixel-data-for-deep-learning/
    """
    # Change input here
    im = Image.open(image_name)
    # Convert image to np array
    pixels = np.array(im)
    # convert from integers to floats
    pixels = pixels.astype(float)
    # normalization
    pixels *= 255.0/pixels.max()
    # convert from np array to image and save
    pixels = pixels.astype(np.uint8)
    new_im = Image.fromarray(pixels)
    bw_im = new_im.convert('LA')
    bw_im.save("normalized.png")
    return bw_im

def image_visualization(image_name, step):
    fig = plt.figure(figsize=(20., 10.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(2, 5),  # creates 2x2 grid of axes
                 axes_pad=0.1,  # pad between axes in inch.
                 )
    scale = 1.0
    # Iterating over the grid returns the Axes.
    for ax in grid:
        im = PIL_contrast(image_name, scale)
        ax.imshow(im)
        scale += step
    plt.show()
    plt.savefig('sweep.png')

def Scikit_transforms(image_name):
    # Change input here
    im = Image.open(image_name)
    bw_im = im.convert('LA')
    # Convert image to np array
    arr = np.array(bw_im)
    # convert from integers to floats
    arr = arr.astype(float)
    # Contrast stretching
    p2, p98 = np.percentile(arr, (2, 98))
    img_rescale = exposure.rescale_intensity(arr, in_range=(p2, p98))
    # convert from np array to image and save
    img_rescale = Image.fromarray(img_rescale.astype(np.uint8))
    img_rescale.save("rescale_intensity.png")

    # Equalization
    img_eq = exposure.equalize_hist(arr)

    # Adaptive Equalization
    img_adapteq = exposure.equalize_adapthist(arr, clip_limit=0.03)

def CV_resize(image_name):
    img = cv2.imread(image_name,0)
    # (h, w) = image.shape[:2]
    #  # resize the image
    # resized = cv2.resize(image, dim, interpolation = inter)

    scale = 45
    #get the webcam size
    height, width = img.shape

    #prepare the crop
    centerX,centerY=int(height/2),int(width/2)
    radiusX,radiusY= int(scale*height/100),int(scale*width/100)

    minX,maxX=centerX-radiusX,centerX+radiusX
    minY,maxY=centerY-radiusY,centerY+radiusY

    cropped = img[minX:maxX, minY:maxY]
    resized = cv2.resize(cropped, (width, height))

    new_im = Image.fromarray(resized)
    bw_im = new_im.convert('LA')
    bw_im.save("cv_resized_45.png")

if __name__ == '__main__':
    normalize("test_imgs/projected.jpg")
    PIL_contrast("normalized.png", 2)
    PIL_sharpen("contrasted.png")
    CV_resize("test_imgs/projected.jpg")
    # image_visualization("test_imgs/4.jpg", .5)
