def check_video(event, context):
    # model ID here
    model_id = 'projects/428720216022/locations/us-central1/models/VCN7553930755844341760'
    if event['contentType'] == 'text/csv':
        bucket = "gs://"+event['bucket']
        input_uri = bucket+event['name']
        output_uri = bucket+"/output/"
        get_prediction(model_id, input_uri, output_uri)


def get_prediction(model_id, input_uri, output_uri_prefix):
    from google.cloud import automl_v1beta1
    prediction_client = automl_v1beta1.PredictionServiceClient()
    # Input configuration.
    input_config = dict(gcs_source={'input_uris': [input_uri]})
    # Output configration.
    output_config = dict(gcs_destination={'output_uri_prefix': 'gs://gdgwaw1'})
    # Launch long-running batch prediction operation.
    operation = prediction_client.batch_predict(model_id, input_config, output_config)
    print('Batch predict operation started: ', operation)
