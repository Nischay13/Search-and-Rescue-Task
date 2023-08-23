import cv2
import numpy as np

def count_triangles(image, color):
  """Counts the number of triangles in an image of a given color.

  Args:
    image: The image to be processed.
    color: The color of the triangles to be counted.

  Returns:
    The number of triangles in the image of the given color.
  """

  triangles = 0
  contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for contour in contours:
    if cv2.contourArea(contour) > 0:
      if color == "red":
        triangles += 1
      elif color == "blue":
        triangles += 2
  return triangles

def assign_colors(image, green_color, brown_color):
  """Assigns cyan and yellow colors to the green and brown parts of an image, respectively.

  Args:
    image: The image to be processed.
    green_color: The RGB value of the green color.
    brown_color: The RGB value of the brown color.

  Returns:
    The image with the green and brown parts assigned cyan and yellow colors, respectively.
  """

  green_mask = cv2.inRange(image, green_color, green_color)
  brown_mask = cv2.inRange(image, brown_color, brown_color)
  green_area = cv2.countNonZero(green_mask)
  brown_area = cv2.countNonZero(brown_mask)
  image[green_mask > 0] = (0, 255, 255)
  image[brown_mask > 0] = (255, 255, 0)
  return image

def main():
  """The main function."""

  # Read the input images.
  images = [cv2.imread("image1.jpg"), cv2.imread("image2.jpg")]

  # Initialize the variables to store the number of triangles in the green and brown parts of each image,
  # and the "Ratio of Priority" for each image.
  green_triangles = []
  brown_triangles = []
  ratios_of_priority = []

  # Process each image.
  for image in images:
    green_triangles.append(count_triangles(image, "green"))
    brown_triangles.append(count_triangles(image, "brown"))
    ratios_of_priority.append(brown_triangles[-1] / green_triangles[-1])
    image = assign_colors(image, (0, 255, 0), (255, 255, 0))

  # Sort the images in decreasing order of "Ratio of Priority".
  sorted_indices = np.argsort(ratios_of_priority)[::-1]
  images = [images[i] for i in sorted_indices]

  # Save the processed images.
  for i, image in enumerate(images):
    cv2.imwrite("output_image_" + str(i) + ".jpg", image)
    main()

  