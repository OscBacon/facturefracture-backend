import requests
import time
import json


def process_total_string(total_string):
    # cleans up a number before converting to a float
    stripped_string = total_string.strip().replace(' ', '')
    result_string = ""
    for character in stripped_string:
        if character.isdigit() or character == '.':
            result_string += character

    total_float = -1
    try:
        total_float = float(result_string)
    except ValueError:
        print('error converting total string')
    return total_float


def scan_image(url):
    # ---Setting up the connection---
    # Keys
    endpoint = 'https://canadacentral.api.cognitive.microsoft.com/vision/v1.0/recognizeText'

    # Replace this with your API key!!!
    api_key = 'c8342bac09f7489eab4deb29727fff9c'

    # HTTP request to send to the API
    # Look at the RecognizeText function from Microsoft
    headers = {
        # Request headers.
        # Another valid content type is "application/octet-stream".
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': api_key,
    }

    # Gets the first argument as the url of the picture to process
    body = {'url': url}

    # If you set the handwriting param to be false, it will use OCR on the text instead (NOT good for handwritten text).
    params = {'handwriting': 'true'}

    # ---Handwriting analysis---
    # Send the image to the CV API
    response = requests.request('POST ', endpoint, json=body, data=None, headers=headers, params=params)

    # 202 is the success status code
    if response.status_code != 202:
        # Display JSON data and exit if the REST API call was not successful.
        parsed = json.loads(response.text)
        print("Error:")
        print(json.dumps(parsed, sort_keys=True, indent=2))
        exit()

    # grab the 'Operation-Location' from the response
    operationLocation = response.headers['Operation-Location']

    # It will take a little bit of time to load so just make the user wait
    # print('\nPicture submitted. Waiting 5 seconds to retrieve the recognized text.\n')
    time.sleep(2)

    # GET the response.
    response = requests.request('GET', operationLocation, json=None, data=None, headers=headers, params=None)

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(response.text)

    # Get the transcribed lines of text
    if 'recognitionResult' in parsed:
        lines = parsed['recognitionResult']['lines']

        total_string = None
        for i in range(len(lines)):

            if lines[i]['text'].strip().replace(':', '').lower() == 'total':

                if i < len(lines) - 1:
                    total_string = lines[i + 1]['text']
        if not total_string:
            return -1

        return process_total_string(total_string)
    else:
        return -1
