import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import os
import cv2

# 本地 YOLOv5 模型路径
MODEL_PATH = "/app/yolov5"

def initialize_model():
    """初始化 YOLO 模型"""
    # 如果模型路径不存在，则克隆 YOLOv5 仓库
    if not os.path.exists(MODEL_PATH):
        os.system(f"git clone https://github.com/ultralytics/yolov5 {MODEL_PATH}")
    # 加载本地 YOLOv5 模型
    model = torch.hub.load(MODEL_PATH, "yolov5s", source="local", pretrained=True)
    return model

# 加载模型
model = initialize_model()

def run_yolo_inference(image_path):
    """
    运行 YOLO 推理
    :param image_path: 输入图片的路径
    :return: 检测结果和保存后的图片文件名
    """
    try:
        # YOLO 推理
        results = model(image_path)

        # 获取原始文件名
        original_filename = os.path.basename(image_path)

        # 覆盖保存处理后的图片
        results.render()
        for img in results.ims:
            cv2.imwrite(image_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

        # 返回检测结果
        return results.pandas().xyxy[0].to_dict(orient="records"), original_filename

    except Exception as e:
        print(f"Error during YOLO inference: {e}")
        return [], ""

# Example usage (仅供测试)
if __name__ == "__main__":
    test_image = "./test_image.jpg"
    detections, saved_image = run_yolo_inference(test_image)
    print("Detections:", detections)
    print("Saved image:", saved_image)
