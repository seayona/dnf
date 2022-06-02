import cv2
import numpy as np

from .tamplate_matching import TemplateMatching
from .capture import capture


def match(image, target, imshow=False):
    """
    模板匹配
    :param image: 原图，例如屏幕截图
    :param target: 模板图片，例如一个图标
    :return: <相似度,标记后的图片,位置坐标,位置坐标>
    """
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    template = cv2.imread(target, cv2.IMREAD_UNCHANGED)
    # 取出Alpha通道fxx
    alpha = template[:, :, 3]
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = top_left[0] + w, top_left[1] + h

    if imshow:
        # 在窗口截图中匹配位置画红色方框
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imshow('Match Template', image)
        cv2.waitKey(1)

    return max_val, image, top_left, bottom_right


# def match(image, target, imshow=False, rgb=True):
#     # 识别目标区域: 点序:左上->左下->右下->右上, 左上(min,min)右x下(max,max)
#     # rectangle = (left_top_pos, left_bottom_pos, right_bottom_pos, right_top_pos)
#     result = TemplateMatching(
#         cv2.imdecode(np.fromfile(target, dtype=np.uint8), cv2.IMREAD_COLOR),
#         image,
#         threshold=0.8,
#         rgb=rgb
#     ).find_best_result()
#     if imshow and result is not None:
#         # 在窗口截图中匹配位置画红色方框
#         cv2.rectangle(image, result['rectangle'][0], result['rectangle'][2], (0, 0, 255), 2)
#         cv2.imshow('Match Template', image)
#         cv2.waitKey(1)
#     return result['confidence'], image, result['rectangle'][0], result['rectangle'][2]
