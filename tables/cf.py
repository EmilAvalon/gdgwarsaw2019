def predict(inputs):
    # put there project_id
    project_id = ''
    compute_region = 'us-central1'
    model_display_name = 'tables'
    from google.cloud import automl_v1beta1 as automl
    client = automl.TablesClient(project=project_id,
                                 region=compute_region)
    response = client.predict(model_display_name=model_display_name,
                              inputs=inputs)
    return response.payload


def checkint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def run(request):
    req = {}
    for i in request.args:
        if checkint(request.args[i]):
            req[i] = int(request.args[i])
        else:
            req[i] = request.args[i]
    return str(predict(req))
