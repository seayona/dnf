import torch

if __name__ == '__main__':
    # Model
    model = torch.hub.load('seayona/dnf', 'dnf', force_reload=True)  # or yolov5n - yolov5x6, custom

    # Images
    img = 'datasets/dnf/images/001.png'  # or file, Path, PIL, OpenCV, numpy, list

    # Inference
    results = model(img)

    # Results
    results.show()  # or .show(), .save(), .crop(), .pandas(), etc.