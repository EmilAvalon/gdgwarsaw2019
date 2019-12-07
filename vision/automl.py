def check_image(event, context):
    from google.cloud import storage
    # project ID here
    project_id = ''
    # model ID here
    model_id = ''
    file = event
    if event['contentType'] == "image/jpeg":
        client = storage.Client()
        fileName = file['name']
        folderName = file['bucket']
        content = client.bucket(folderName).get_blob(fileName)
        content = content.download_as_string()
        value = get_prediction(content, project_id, model_id)
        to_store = ""
        for data in value.payload:
            to_store = to_store+str(data)+"\n"
        output_file = "output/"+fileName+".txt"
        blob = client.bucket(folderName).blob(output_file)
        blob.upload_from_string(to_store, content_type="text/plain")


def get_prediction(content, project_id, model_id):
    from google.cloud import automl_v1beta1
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content}}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned
