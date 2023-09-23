# -*- coding: utf-8 -*-
import cv2
import numpy as np


def uniform_random(left, right, size=None):
    """
    generate uniformly distributed random numbers in [left, right)

    Parameters:
    -----------
    left: a number
        left border of random range
    right: a number
        right border of random range
    size: a number or a list/tuple of numbers
        size of output

    Returns:
    --------
    rand_nums: ndarray
        uniformly distributed random numbers
    """
    rand_nums = (right - left) * np.random.random(size) + left
    return rand_nums


def random_polygon(edge_num, center, radius_range):
    """
    generate points to construct a random polygon

    Parameters:
    -----------
    edge_num: a number
        edge numbers of polygon
    center: a list/tuple contain two numbers
        center of polygon
    radius_range: a list/tuple containing two numbers
        range of distances from center to polygon vertices

    Returns:
    --------
    points: ndarray
        points that can construct a random polygon
    """
    angles = uniform_random(0, 2 * np.pi, edge_num)
    angles = np.sort(angles)
    random_radius = uniform_random(radius_range[0], radius_range[1], edge_num)
    x = np.cos(angles) * random_radius
    y = np.sin(angles) * random_radius
    x = np.expand_dims(x, 1)
    y = np.expand_dims(y, 1)
    points = np.concatenate([x, y], axis=1)
    points += np.array(center)
    points = np.round(points).astype(np.int32)
    return points


def draw_polygon(image_size, points, color):
    """
    draw polygon(s) on a image

    Parameters:
    -----------
    image_size: a list/tuple of numbers
        image size = [image_height, image_width, image_channel]
    points: 2D ndarray or a list of 2D ndarray
        points that can construct a random polygon, also can be a list of
        points that can construct random polygons
    color: a list/tuple of numbers, whose length is same as image channel
        color of polygon

    Returns:
    --------
    image: ndarray
        image with polygon(s) on it
    """
    image = np.zeros(image_size, dtype=np.uint8)
    if type(points) is np.ndarray and points.ndim == 2:
        image = cv2.fillPoly(image, [points], color)
    else:
        image = cv2.fillPoly(image, points, color)
    return image


if __name__ == '__main__':
    points1 = random_polygon(10, [80, 80], [20, 50])
    points2 = random_polygon(10, [80, 180], [20, 50])
    points3 = random_polygon(3, [180, 80], [20, 50])
    points4 = random_polygon(5, [180, 180], [20, 50])

    pts = [points1, points2, points3, points4]

    # image1 = draw_polygon((256, 256, 3), points1, (255, 255, 255))
    image2 = draw_polygon((256, 256, 3), pts, (255, 255, 255))
    # cv2.imshow('a', image1)
    cv2.imshow('b', image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
