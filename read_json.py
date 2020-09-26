import json
import cv2
import numpy as np

images = []
masks = []

def get_points(raw_data):
    point = []
    points = []
    count = 1
    for i in raw_data:
        point.append(i)
        if count % 2 == 0:
            points.append(point)
            point = []
        count += 1
    return np.array(points, dtype = np.int32)

with open('dataset.json', 'r') as json_file:
    json_data = [json.loads(line) for line in json_file]
    for data in json_data:
        
        image_path = data['image_path']
        image_path = image_path[:6] + '/annotated_images' + image_path[6:]
    
        image = cv2.imread(image_path)
        image = np.mean(image, axis = 2).astype(np.uint8)
        mask = np.zeros_like(image)

        line = data['lines']
        line = get_points(line)
        # mask olustumak icin
        mask = cv2.fillPoly(mask, [line], (255, 255, 255))
        
        print(mask.shape)
        print(image.shape)

        # image ve maskı istediğiniz şekile kullanabilirsiniz.

