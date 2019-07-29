from google.cloud import automl_v1beta1 as automl
# TODO(developer): Uncomment and set the following variables
project_id = 'psyched-silicon-182807'
compute_region = 'us-central1'
model_id = 'TEN3911015636557365248'
file_path = 'app/data/grundbuchauszug_text.txt'


def grundbuchtext_ml():

    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Read the file content for prediction.
    with open(file_path, "rb") as content_file:
        snippet = content_file.read()

    # Set the payload by giving the content and type of the file.
    payload = {"text_snippet": {"content": snippet, "mime_type": "text/plain"}}

    # params is additional domain-specific parameters.
    # currently there is no additional parameters supported.
    params = {}
    response = prediction_client.predict(model_full_id, payload, params)
    #print("Prediction results:")
    #for result in response.payload:
        #print("Predicted entity label: {}".format(result.display_name))
        #print("Predicted confidence score: {}".format(result.text_extraction.score))
        #print("Predicted text segment: {}".format(result.text_extraction.text_segment.content))
        #print("Predicted text segment start offset: {}".format(result.text_extraction.text_segment.start_offset))
        #print("Predicted text segment end offset : {}".format(result.text_extraction.text_segment.end_offset))
        #print("\n")