#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# git origin:
# GoogleCloudPlatform/python-docs-samples/vision/cloud-client/quickstart/quickstart.py

def run_quickstart():
    # [START vision_quickstart]
    import io
    import os

    # Imports the Google Cloud client library
    # [START vision_python_migration_import]
    from google.cloud import vision
    from google.cloud.vision import types
    from google.oauth2 import service_account
    # [END vision_python_migration_import]

    # Instantiates a client
    # [START vision_python_migration_client]
    key_file = os.path.expanduser('~/key.json')
    credentials = service_account.Credentials.from_service_account_file(key_file)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    # [END vision_python_migration_client]

    # The name of the image file to annotate
    file_names = ['~/cat.jpg', '~/dog.jpg']

    # Loads the image into memory
    for file_name in file_names:
        file_name = os.path.expanduser(file_name)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels for file '+file_name+':')
        i = 0
        for label in labels:
            i = i + 1
            if (i == 4):
                break
            print(label.description)
        # [END vision_quickstart]


if __name__ == '__main__':
    run_quickstart()
