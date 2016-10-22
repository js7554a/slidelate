'''
Returns label from picture file.
Run the script on an image to get a label, E.g.:

 $   gcv.py <path-to-image>

Before running, make sure you have set up application default credentials as described here:
https://cloud.google.com/vision/docs/common/auth#using-api-manager

And then run:
$ export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json

Install dependencies using:
$ pip install --upgrade google-api-python-client
$ pip install Pillow

'''


import argparse
import base64
import httplib2
import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.cloud import translate

def gt(text, api_key, dest_lang, print_output = False):
    """
    Translates text to dest_lang using Google Translate API.
    """

    # Instantiates a client
    translate_client = translate.Client(api_key)
    text_clean = text.replace('\n', ' ')
    # translates with client
    translation = translate_client.translate(text_clean, target_language=dest_lang)
    translated_text = translation['translatedText']

    return translated_text

def gnl(text, print_output = False):
    """
    Connect to Google Natural Language API; fetch named entities and translate (if dest_lang does not match language of text).
    See Google sample scripts here for more information: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/language/ocr_nl/main.py

    :param text:
    :param print_output:
    """
    response_out = None
    entities = None
    entities_dict = None
    lang = None
    
    # get credentials and connect to GNL API
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    service = discovery.build('language', 'v1beta1', http=http)

    # fetch named entities
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encodingType': 'UTF8',
    }
    entities = []
    try:
        request = service.documents().analyzeEntities(body=body)
        response = request.execute()
        entities = response['entities']
        entities_dict = {e.get('name'): e.get('type') for e in entities}
        wikipedia_dict = {e.get('name'): e.get('metadata').get('wikipedia_url') for e in entities
                          if e.get('metadata').get('wikipedia_url')}
        lang = response.get('language')
    # except errors.HttpError as e:
    #     #TODO
    #     pass
    except KeyError as e2:
        #TODO
        pass

    # construct JSON response and return

    response_out_gnl = {
        'status': 'success',
        'data': {
            'entities': entities_dict,
            'wikipedia': wikipedia_dict,
            'lang': lang
        },
        'message': None
    }

    return response_out_gnl


def fetch_image_data(photo_file, print_output = False, nlab = 10, nlogo = 10, return_type = 'json',
             translate =
None, dest_lang = None, api_key = None):
    """
    Fetch data for photo_file using Google Cloud Vision API, Google Natural Language API,
    and Google Translate API.

    :param photo_file: path to photo file. Supports the following image formats:
    https://cloud.google.com/vision/docs/best-practices
    :param print_output: logical; if set to true, JSON output will be pretty-printed to terminal.
    :param nlab: maximum number of labels to fetch for image.
    :param nlogo: maximum number of logos to fetch for image.
    :param translate: language to translate text to (if text is already in this language,
    returns untranslated text).
    :return: JSON file with

    """
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    # initialize output variables
    full_text = None
    labels = None
    logos = None
    gt_translation = None

    # get initial image data from Google Cloud Vision API (labels, text, and logos)
    
    image_content = photo_file
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [
            {
                'type': 'LABEL_DETECTION',
                'maxResults': nlab
            },
            {
                'type': 'TEXT_DETECTION',
                'maxResults': 1
            },
            {
                'type': 'LOGO_DETECTION',
                'maxResults': nlogo
            }
            ]
        }]
    })
    gcv_response = service_request.execute()

    # check if error in GCV response; if so, return a response with the error message
    if 'error' in gcv_response['responses']:
        response_out = {
            'status': 'error',
            'data': None,
            'message': response['error']['message']
        }
        return response_out

    # extract relevant data from gcv response
    try:
        full_text = gcv_response['responses'][0]['textAnnotations'][0]['description']
    except KeyError:
        pass
    try:
        labels = [x['description'] for x in gcv_response['responses'][0]['labelAnnotations']]
    except KeyError:
        pass
    try:
        logos = [x['description'] for x in gcv_response['responses'][0]['logoAnnotations']]
    except KeyError:
        pass

    response_gnl = None
    # using text from GCV response, get named entitites and translate text, if requested
    if full_text:
        clean_text = full_text.replace('\n', ' ')
        response_gnl = gnl(full_text, print_output=True)
        text_lang = response_gnl['data']['lang']
        if dest_lang != text_lang:
            gt_translation = gt(clean_text, api_key, dest_lang)

    lang = None
    entities = None
    wikipedia = None
    
    if response_gnl:
        lang = response_gnl.get('data').get('lang')
        entities = response_gnl.get('data').get('entities')
        wikipedia = response_gnl.get('data').get('wikipedia')

    # construct JSEND-compliant JSON response
    response_out = {
        'status': 'success',
        'data': {
            'full_text': full_text,
            'labels': labels,
            'logos': logos,
            'lang': lang,
            'entities': entities,
            'wikipedia': wikipedia,
            'dest_lang': dest_lang,
            'translation': gt_translation
        },
        'message': None
    }

    # print output; if requested
    if print_output:
        print('IMAGE_RESULTS: \n\n')
        pprint.pprint(response_out)

    return response_out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    parser.add_argument('-nla', help='The number of labels you\'d like returned', default = 10)
    parser.add_argument('-nlo', help='The number of logos you\'d like returned', default = 10)
    parser.add_argument('-r', help='The return type; currently only json is supported', default=
    'json')
    parser.add_argument('-d', help='Destination language')
    parser.add_argument('-k', help = 'Google Translate API Key', required = True)
    args = parser.parse_args()
    response_out = fetch_image_data(args.image_file, print_output=True,nlab = args.nla,
                                     nlogo = args.nlo, return_type = args.r, dest_lang=args.d,
                       api_key = args.k)

