import base64

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import numpy as np
from PIL import Image
import json
import time

def predict_image_classification_sample(
    project: str,
    endpoint_id: str,
    filename: str,
    location: str,
    api_endpoint: str = "asia-southeast1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
        mime_type='image/jpeg'
    ).to_value()
    #instances=[{'b64': encoded_content}]
    #print('instance ', instance)
    #instances = [instance]
    #serving_input = list(loaded.signatures["serving_default"].structured_input_signature[1].keys())[0]
    #instances = [{ serving_input : {'b64': encoded_content}}]
    #print('serving_input', loaded.signatures)
    im = Image.open(filename)
    im = im.resize((200,200))
    im = np.array(im)
    im = im.reshape((1,)+ im.shape)
    x_test = im.astype(np.float32).tolist()
    
    # Writing to sample.json
    json_object = json.dumps({'instances':x_test})
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    #im = np.array(im).reshape(-1, 200 * 200)
    #im = im.convert('L')
    #print('im ', im.shape)
    #im = np.array(im).reshape(-1, 28 * 28)/255.0
   
    #x_test = im.astype(np.uint8).tolist()
    #print('x_test length', len(x_test))
    instances = x_test
    #instances = { "signature_name": "serving_default", "instances2" : [x_test]}
    #print('instances ', instances)
    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    #parameters = predict.params.ImageClassificationPredictionParams(
    #    confidence_threshold=0.5, max_predictions=5,
    #).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    #print('endpoint ', endpoint)
    #response = client.predict(
    #    endpoint=endpoint, instances=instances, parameters=parameters
    #)
    starttime = time.time()
    response = client.predict(
        endpoint=endpoint, instances=instances
    )
    latency = time.time() - starttime
    #print("response2", response)
    #print("deployed_model_id:", response.deployed_model_id)
    #print("latency :", latency)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    #for prediction in response.predictions:
    #print("prediction:", response.predictions[0])
    return response.predictions[0]


#predict_image_classification_sample(
#    project="320940575449",
#    endpoint_id="7790119047630159872",
#	filename='garbage.jpg',
#    location="asia-southeast1"
#)
