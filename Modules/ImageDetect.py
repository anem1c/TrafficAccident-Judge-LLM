import cv2
import numpy as np
from typing import List, Tuple

# 클래스 한글 매핑 (영어 -> 한글)
class_mapping = {
    'damaged door': '손상된 문짝',
    'damaged window': '손상된 창문',
    'damaged headlight': '손상된 헤드라이트',
    'damaged mirror': '손상된 사이드 미러',
    'dent': '덴트',
    'damaged hood': '손상된 후드',
    'damaged bumper': '손상된 범퍼',
    'damaged wind shield': '손상된 윈드쉴드'
}

# Detection 클래스 정의 (FastAPI 서버 없이 직접 실행)
class Detection:
    def __init__(self, model_path: str, classes: List[str]):
        self.model_path = model_path
        self.classes = classes
        self.model = self.__load_model()

    def __load_model(self) -> cv2.dnn_Net:
        net = cv2.dnn.readNet(self.model_path)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # CPU에서 실행
        return net

    def __extract_output(self, preds: np.ndarray, image_shape: Tuple[int, int], input_shape: Tuple[int, int],
                         score: float = 0.1, nms: float = 0.0, confidence: float = 0.0) -> dict:
        class_ids, confs, boxes = [], [], []

        image_height, image_width = image_shape
        input_height, input_width = input_shape
        x_factor = image_width / input_width
        y_factor = image_height / input_height

        rows = preds[0].shape[0]
        for i in range(rows):
            row = preds[0][i]
            conf = row[4]

            classes_score = row[4:]
            _, _, _, max_idx = cv2.minMaxLoc(classes_score)
            class_id = max_idx[1]

            if classes_score[class_id] > score:
                confs.append(conf)
                label = self.classes[int(class_id)]
                class_ids.append(label)

                # Extract boxes
                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

        r_class_ids, r_confs, r_boxes = [], [], []
        indexes = cv2.dnn.NMSBoxes(boxes, confs, confidence, nms)
        for i in indexes:
            r_class_ids.append(class_ids[i])
            r_confs.append(confs[i] * 100)
            r_boxes.append(boxes[i].tolist())

        return {'boxes': r_boxes, 'confidences': r_confs, 'classes': r_class_ids}

    def __call__(self, image: np.ndarray, width: int = 640, height: int = 640, score: float = 0.1,
                 nms: float = 0.0, confidence: float = 0.0) -> dict:
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (width, height), swapRB=True, crop=False)
        self.model.setInput(blob)
        preds = self.model.forward()
        preds = preds.transpose((0, 2, 1))

        results = self.__extract_output(preds=preds, image_shape=image.shape[:2], input_shape=(height, width),
                                        score=score, nms=nms, confidence=confidence)
        return results

# 모델 경로 및 클래스 정의 (영문)
detection = Detection(
    model_path='best.onnx',
    classes=['damaged door', 'damaged window', 'damaged headlight', 'damaged mirror', 'dent', 'damaged hood', 'damaged bumper', 'damaged wind shield']
)