import cv2
import numpy as np
import torch

# Load model
from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.datasets import LoadImages
from utils.general import check_img_size, increment_path, non_max_suppression, scale_coords
from utils.plots import Annotator
from utils.torch_utils import select_device

# Load model
device = select_device('0')
model = DetectMultiBackend('weights/best.pt', device=device, dnn=False, data='data/dnf.yaml', fp16=False)
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size((640, 640), s=stride)  # check image size

# Load image
img0 = cv2.imread("data/images/dnf.png")
img0 = cv2.cvtColor(img0, cv2.COLOR_BGRA2BGR)
# Padded resize
img = letterbox(img0, new_shape=640)[0]
# Convert
img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
img = np.ascontiguousarray(img)
im = torch.from_numpy(img).to(device)
im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
im /= 255  # 0 - 255 to 0.0 - 1.0

# Inference
visualize = False
pred = model(im, augment=None, visualize=visualize)

# NMS
pred = non_max_suppression(pred, 0.25, 0.45, ['monster'], None, max_det=1000)


# Process predictions
for i, det in enumerate(pred):  # per image
    # seen += 1
    # if webcam:  # batch_size >= 1
    #     p, im0, frame = path[i], im0s[i].copy(), dataset.count
    #     s += f'{i}: '
    # else:
    #     p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
    #
    # p = Path(p)  # to Path
    # save_path = str(save_dir / p.name)  # im.jpg
    # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
    # s += '%gx%g ' % im.shape[2:]  # print string
    gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
    imc = im0.copy() # if save_crop else im0  # for save_crop
    annotator = Annotator(im0, line_width=3, example=str(names))
    if len(det):
        # Rescale boxes from img_size to im0 size
        det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

        # # Print results
        # for c in det[:, -1].unique():
        #     n = (det[:, -1] == c).sum()  # detections per class
        #     s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
        #
        # # Write results
        # for *xyxy, conf, cls in reversed(det):
        #     if save_txt:  # Write to file
        #         xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
        #         line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
        #         with open(txt_path + '.txt', 'a') as f:
        #             f.write(('%g ' * len(line)).rstrip() % line + '\n')
        #
        #     if save_img or save_crop or view_img:  # Add bbox to image
        #         c = int(cls)  # integer class
        #         label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
        #         annotator.box_label(xyxy, label, color=colors(c, True))
        #         if save_crop:
        #             save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

    # Stream results
    im0 = annotator.result()
    if True:
        cv2.imshow('detect', im0)
        cv2.waitKey(10000)  # 1 millisecond
