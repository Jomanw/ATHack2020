# This is a temporary file for testing methods of applying image contrast
from PIL import Image, ImageEnhance, ImageOps

# For visualization
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
from numpy import *

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
    enhanced_im.save("enhanced.sample1.png")
    return enhanced_im

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

def histeq(im,nbr_bins=256):
  """  Histogram equalization of a grayscale image. """
  # get image histogram
  imhist,bins = np.histogram(im.flatten(),nbr_bins,normed=True)
  cdf = imhist.cumsum() # cumulative distribution function
  cdf = 255 * cdf / cdf[-1] # normalize

  # use linear interpolation of cdf to find new pixel values
  im2 = np.interp(im.flatten(),bins[:-1],cdf)

  return im2.reshape(im.shape), cdf

if __name__ == '__main__':
    PIL_contrast("test_imgs/4.jpg", 2)
    image_visualization("test_imgs/4.jpg", .5)
