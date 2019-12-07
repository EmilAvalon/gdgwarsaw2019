from google.cloud import storage
from tornado.escape import url_unescape
import random
import argparse
import sys


def addtype(data, type):
    for i in range(int(len(data))):
        data[i] = [type, data[i][0], data[i][1]]
        print(data[i])
    return data


def createData(projectId):
    tag1 = "cat"
    tag2 = "dog"
    storage_client = storage.Client()
    inputbucket = projectId+"-vcm"
    random.seed(273)
    data = []
    bucket = storage_client.get_bucket(inputbucket)
    blobs = bucket.list_blobs()
    for file in blobs:
        name = url_unescape(file.path).rsplit("/", 1)[-1]
        if name.find("jpg") > -1:
            if name.find(tag1) > -1:
                type = tag1
            elif name.find(tag2) > -1:
                type = tag2
            bucket_name = "gs://"+inputbucket+"/"+str(name)
            data.append([bucket_name, type])
    random.shuffle(data)
    data_len = int(len(data))
    train = int(data_len*.8)
    valid = int(data_len*.9)
    train_data = addtype(data[:train], 'TRAIN')
    valid_data = addtype(data[train:valid], 'VALIDATION')
    test_data = addtype(data[valid:], 'TEST')
    full_data = train_data + valid_data + test_data
    str_data = ''
    for i in full_data:
        str_data = str_data+str(i[0])+","+str(i[1])+","+str(i[2])+'\n'
    return str_data


def upload_data_to_gcs(projectId, data):
    csvdestination = "cats-dogs.csv"
    bucket_name = projectId+"-vcm"
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        bucket.blob(csvdestination).upload_from_string(data)
    except Exception as e:
        print(e)


def getValues():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("projectID",
                            help="add project ID",
                            type=str)
    #    args = parser.parse_args()
    #    print sys.argv
        return sys.argv[1]
    #    print args
    except:
        e = sys.exc_info()[0]
        print e


def startCreate():
    projectId = getValues()
#    print projectID
    data = createData(projectId)
    upload_data_to_gcs(projectId, data)


startCreate()
