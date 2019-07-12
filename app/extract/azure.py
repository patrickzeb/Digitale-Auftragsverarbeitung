from requests import post as http_post


def recognizeForm(file):
    base_url = r"https://westeurope.api.cognitive.microsoft.com" + "/formrecognizer/v1.0-preview/custom"
    file_path = file
    model_id = "02c68594-7bd5-4ddf-a708-e7f2fbe9058c"
    headers = {
        # Request headers
        'Content-Type': 'application/pdf',
        'Ocp-Apim-Subscription-Key': 'b079c21c61f5413cb496315a7a1d2c9e',
    }

    try:
        url = base_url + "/models/" + model_id + "/analyze"
        with open(file_path, "rb") as f:
            data_bytes = f.read()
            resp = http_post(url=url, data=data_bytes, headers=headers)
        # print("Response status code: %d" % resp.status_code)
        # print("Response body:\n%s" % resp.json())
    except Exception as e:
        print(str(e))

    return resp.json()