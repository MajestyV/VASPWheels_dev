import cv2
import numpy as np

def generate_poly(image, n, area_thresh):
    """
    随机生成凸包
    :param image: 二值图
    :param n: 顶点个数
    :param area_thresh: 删除小于此面积阈值的凸包
    :return: 凸包图
    """
    row, col = np.where(image[:, :, 0] == 255)  # 行,列
    point_set = np.zeros((n, 1, 2), dtype=int)
    for j in range(n):
        index = np.random.randint(0, len(row))
        point_set[j, 0, 0] = col[index]
        point_set[j, 0, 1] = row[index]
    hull = []
    hull.append(cv2.convexHull(point_set, False))
    drawing_board = np.zeros(image.shape, dtype=np.uint8)
    cv2.drawContours(drawing_board, hull, -1, (255, 255, 255), -1)
    cv2.namedWindow('drawing_board', 0), cv2.imshow('drawing_board', drawing_board), cv2.waitKey()

    # 如果生成面积过小，重新生成
    if cv2.contourArea(hull[0]) < area_thresh:
        drawing_board = generate_poly(image, n, area_thresh)

    # 如果生成洞，重新生成
    is_hole = image[drawing_board == 255] == 255
    if is_hole.all() == True:  # 洞，则drawing_board所有为255的地方，image也是255，all()即为所有位置
        drawing_board = generate_poly(image, n, area_thresh)
    return drawing_board


img = np.zeros((256, 256, 3), np.uint8)
cv2.circle(img, (100, 100), 50, (255, 255, 255), -1)
cv2.namedWindow('img', 0), cv2.imshow('img', img), cv2.waitKey()

img_hull = generate_poly(img, 8, 100)
cv2.namedWindow('img_hull', 0), cv2.imshow('img_hull', img_hull), cv2.waitKey()