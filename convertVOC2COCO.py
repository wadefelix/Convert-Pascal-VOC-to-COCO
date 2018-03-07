#! python
import os
import xml.etree.ElementTree as ET
import json
from collections import OrderedDict


CATEGORIES = [{"supercategory":"none","id":1,"name":"aeroplane"},
              {"supercategory":"none","id":2,"name":"bicycle"},
              {"supercategory":"none","id":3,"name":"bird"},
              {"supercategory":"none","id":4,"name":"boat"},
              {"supercategory":"none","id":5,"name":"bottle"},
              {"supercategory":"none","id":6,"name":"bus"},
              {"supercategory":"none","id":7,"name":"car"},
              {"supercategory":"none","id":8,"name":"cat"},
              {"supercategory":"none","id":9,"name":"chair"},
              {"supercategory":"none","id":10,"name":"cow"},
              {"supercategory":"none","id":11,"name":"diningtable"},
              {"supercategory":"none","id":12,"name":"dog"},
              {"supercategory":"none","id":13,"name":"horse"},
              {"supercategory":"none","id":14,"name":"motorbike"},
              {"supercategory":"none","id":15,"name":"person"},
              {"supercategory":"none","id":16,"name":"pottedplant"},
              {"supercategory":"none","id":17,"name":"sheep"},
              {"supercategory":"none","id":18,"name":"sofa"},
              {"supercategory":"none","id":19,"name":"train"},
              {"supercategory":"none","id":20,"name":"tvmonitor"}]

def generateVOC2Json(rootDir,testXMLFiles):
    attrDict = dict()
    attrDict["categories"] = CATEGORIES
    images = list()
    annotations = list()
    for rootdir, dirs, files in os.walk(rootDir):
        for file in testXMLFiles:
            if file in files:
                annotation_path = os.path.join(rootdir, file)
                
                tree = ET.parse(annotation_path)
                root = tree.getroot()
                image = dict()
                image['file_name'] = root.find('filename').text
                image['height'] = int(root.find('size').find('height').text)
                image['width'] = int(root.find('size').find('width').text)

                image['id'] = image['file_name'].split('.jpg')[0]
                images.append(image)
                objs = tree.findall('object')
                id1 = 1
                for obj in objs:
                        for value in attrDict["categories"]:
                            annotation = dict()
                            if obj.find('name').text in value["name"]:
                                annotation["segmentation"] = []
                                annotation["iscrowd"] = 0
                                annotation["image_id"] = image['id']
                                bbox = obj.find('bndbox')
                                x1 = int(bbox.find("xmin").text) - 1
                                y1 = int(bbox.find("ymin").text) - 1
                                x2 = int(bbox.find("xmax").text) - x1
                                y2 = int(bbox.find("ymax").text) - y1
                                annotation["bbox"] = [x1, y1, x2, y2]
                                annotation["area"] = int(x2 * y2)
                                annotation["category_id"] = value["id"]
                                annotation["ignore"] = 0
                                annotation["id"] = id1
                                id1 +=1

                                annotations.append(annotation)

    attrDict["images"] = images    
    attrDict["annotations"] = annotations
    attrDict["type"] = "instances"

    jsonString = json.dumps(attrDict)
    with open("voc_2012_train.json", "w") as f:
        f.write(jsonString)

trainFile = os.path.expanduser("~/data/VOCdevkit/VOC2012/ImageSets/Main/train.txt")
trainXMLFiles = list()
with open(trainFile, "rb") as f:
    for line in f:
        fileName = line.strip()
        print fileName
        trainXMLFiles.append(fileName + ".xml")


rootDir = os.path.expanduser("~/home/merge/data/VOCdevkit/VOC2012/Annotations/")
generateVOC2Json(rootDir, trainXMLFiles)

