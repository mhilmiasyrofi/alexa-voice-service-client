import argparse
import io
import time
import os

from pydub import AudioSegment
from pydub.playback import play
import pyaudio

from alexa_client import AlexaClient

from alexa_client.alexa_client import constants


def main(client_id, secret, refresh_token):
    alexa_client = AlexaClient(
        client_id=client_id,
        secret=secret,
        refresh_token=refresh_token,
        base_url=constants.BASE_URL_NORTH_AMERICA
    )

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        input_buffer.write(in_data)
        return (in_data, pyaudio.paContinue)

    stream = p.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        stream_callback=callback,
        frames_per_buffer=128,
        start=False
    )

    dialog_request_id = None

    try:
        print('listening. Press CTRL + C to exit.')
        input_buffer = io.BytesIO()
        stream.start_stream()
        print('Say something to Alexa.')
        alexa_client.connect()
        while True:
            directives = alexa_client.send_audio_file(
                input_buffer,
                dialog_request_id=dialog_request_id
            )
            stream.stop_stream()
            if directives:
                dialog_request_id = None
                print('Alexa\'s turn.')
                for directive in directives:
                    if directive.name == 'ExpectSpeech':
                        dialog_request_id = directive.dialog_request_id
                    if directive.name in ['Speak', 'Play']:
                        output_buffer = io.BytesIO(directive.audio_attachment)
                        track = AudioSegment.from_mp3(output_buffer)
                        play(track)
                input_buffer = io.BytesIO()
            stream.start_stream()
            print('Your turn. Say something.')
            time.sleep(1)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")
    main(
        client_id=client_id,
        secret=client_secret,
        refresh_token=refresh_token,
    )
