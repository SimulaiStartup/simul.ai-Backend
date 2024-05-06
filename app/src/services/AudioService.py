import os
from dotenv import load_dotenv
import logging, verboselogs

from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    PrerecordedOptions,
)

load_dotenv()

def speech_to_text(URL):
    audioURL = {
        "url": URL
    }
    deepgram: DeepgramClient = DeepgramClient("", ClientOptionsFromEnv())

    options: PrerecordedOptions = PrerecordedOptions(
        language="pt-BR",
        model="nova-2",
        smart_format=True,
    )
    url_response = deepgram.listen.prerecorded.v("1").transcribe_url(
        audioURL, options
    )

    return url_response.results.channels[0].alternatives[0]['transcript']

def main():
    url = "https://www2.cs.uic.edu/~i101/SoundFiles/preamble.wav"

    print(speech_to_text(url))

if __name__ == "__main__":
    main()