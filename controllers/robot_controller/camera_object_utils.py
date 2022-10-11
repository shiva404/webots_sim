from controller import CameraRecognitionObject
from typing import List
import json


# https://cyberbotics.com/doc/reference/camera?tab-language=java#camera-recognition-object
def save_recognized_objects(recognized_objects: List[CameraRecognitionObject], file_path):
    result = []
    for recognized_object in recognized_objects:
        id = recognized_object.getId()
        position: List[float] = recognized_object.getPosition()
        orientation: List[float] = recognized_object.getOrientation()
        size: List[float] = recognized_object.getSize()
        position_on_image: List[int] = recognized_object.getPositionOnImage()
        size_on_image: List[int] = recognized_object.getSizeOnImage()
        number_of_colors: int = recognized_object.getNumberOfColors()
        colors: List[float] = recognized_object.getColors()
        model: str = recognized_object.getModel()

        rec_obj = {
            'id': id,
            'position': position,
            'orientation': orientation,
            'size': size,
            'position_on_image': position_on_image,
            'size_on_image': size_on_image,
            'number_of_colors': number_of_colors,
            'colors': colors,
            'model': str(model)
        }
        result.append(rec_obj)

    json_data = json.dumps({'recognized_objects': result})
    with open(file_path, 'w') as file:
        file.write(json_data)

