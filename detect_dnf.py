import time
import os
import sys
from pathlib import Path

import numpy as np
import pyautogui
import torch
from torch import Tensor

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import (check_img_size, cv2,
                           non_max_suppression, scale_coords)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device


@torch.no_grad()
def detect(weights=ROOT / 'weights/best.pt', data=ROOT / 'data/dnf.yaml', view_img=False):
    imgsz = (1376, 832)
    # Load model
    device = select_device('0' if torch.cuda.is_available() else 'cpu')
    model = DetectMultiBackend(weights, device=device, dnn=False, data=data, fp16=False)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    bs = 1  # batch_size

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup

    img0 = pyautogui.screenshot(region=[0, 0, 1376, 832])
    img0 = cv2.cvtColor(np.asarray(img0), cv2.COLOR_RGB2BGR)
    # img0 = cv2.imread('data/images/dnf.png')  # BGR
    # Padded resize
    img = letterbox(img0, 640, stride=stride, auto=pt)[0]

    # Convert
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)
    im = torch.from_numpy(img).to(device)
    im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim

    # Inference
    pred = model(im, augment=False, visualize=False)

    # NMS
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=10)

    # Process predictions
    for i, det in enumerate(pred):  # per image
        im0 = img0.copy()
        annotator = Annotator(im0, line_width=3, example=str(names))
        if len(det):
            # ?????????????????????
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
            # Write results
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)  # integer class
                label = f'{names[c]} {conf:.2f}'
                annotator.box_label(xyxy, label, color=colors(c, True))
        if view_img:
            im0 = annotator.result()
            cv2.imshow('str(p)', im0)
            cv2.waitKey(1)  # 1 millisecond

    return pred, names


def detect_lion_entry(weights=ROOT / 'weights/last.pt', data=ROOT / 'data/dnf_close.yaml', view_img=False):
    return detect(weights=weights, data=data, view_img=view_img)


if __name__ == "__main__":
    while True:
        pred, names = detect_lion_entry(view_img=True)
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *xyxy, conf, cls in reversed(det):
                x, y = (int(xyxy[0]), int(xyxy[1]))
                if names[int(cls)] == 'close' and float(f'{conf:.2f}') > 0.5:
                    print("?????????????????????????????????????????????", (x, y))
