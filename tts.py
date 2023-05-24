"""Getting Started Example for Python 2.7+/3.3+"""
from typing import Optional
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import uuid

# import sys

# import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="polly-api", region_name="ap-south-1")
polly = session.client("polly")


def generate_audio(text: str) -> Optional[str]:
    try:
        # Request speech synthesis
        # response = polly.synthesize_speech(
        #     Text=text, OutputFormat="mp3", VoiceId="Ruth", Engine="neural"
        # )
        response = polly.synthesize_speech(
            Text=text, OutputFormat="mp3", VoiceId="Joanna"
        )
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        return None

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), f"{uuid.uuid4()}-speech.mp3")

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                return output
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                return None

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        return None
