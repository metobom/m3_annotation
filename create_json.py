import json

def to_json(lines, image_path):
    data = {}
    data['lines'] = lines
    data['image_path'] = image_path

    with open('dataset.json', 'a') as json_file:
        json.dump(data, json_file)
        json_file.write('\n')


