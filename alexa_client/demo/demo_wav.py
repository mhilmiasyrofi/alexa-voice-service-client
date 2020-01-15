from alexa_client import AlexaClient
from alexa_client.alexa_client import constants
from alexa_client.alexa_client import helpers

import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
refresh_token = os.getenv("REFRESH_TOKEN")

client = AlexaClient(
    client_id=client_id,
    secret=client_secret,
    refresh_token=refresh_token,
    base_url = constants.BASE_URL_NORTH_AMERICA
)

client.connect()  # authenticate and other handshaking steps
# with open('../../tests/resources/alexa_what_time_is_it.wav', 'rb') as f:
dialog_request_id = helpers.generate_unique_id()
audio_one = open('alexa_open_this_test.wav', 'rb')
directives_one = client.send_audio_file(
    audio_one, dialog_request_id=dialog_request_id)
audio_two = open('record_this_please_turn_on_the_light.wav', 'rb')
directives_two = client.send_audio_file(
    audio_two, dialog_request_id=dialog_request_id)


for i, directive in enumerate(directives_one):
    if directive.name in ['Speak', 'Play']:
        with open(f'./output_1_{i}.mp3', 'wb') as f:
            f.write(directive.audio_attachment)
    elif directive.name == 'RenderTemplate' :
        print(directive.payload['textField'])

for i, directive in enumerate(directives_two):
    if directive.name in ['Speak', 'Play']:
        with open(f'./output_2_{i}.mp3', 'wb') as f:
            f.write(directive.audio_attachment)
    elif directive.name == 'RenderTemplate':
        print(directive.payload['textField'])
