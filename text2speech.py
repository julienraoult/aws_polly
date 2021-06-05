import boto3
from contextlib import closing
from typing import Optional

class ApiConsumer:
    def __init__(self):
        self.polly = boto3.client('polly', region_name='eu-west-3')
        
    def synthesize(self, voice_id: str, text: str):
        return self.polly.synthesize_speech(
            VoiceId = voice_id,
            Text = text,
            OutputFormat='mp3'
        )

ApiConsumer().synthesize(voice_id='Lea', text='Bonjour Julien')

def save_stream_from_response(response: dict):
    from botocore.response import StreamingBody
    audio_stream: Optional[StreamingBody] = (
        response.get('AudioStream', None)
    )
    if audio_stream is None:
        raise Exception("audio_stream is none !")
    with closing(audio_stream) as stream:
        stream_bytes = stream.read()
        with open("./aws_voice.mp3", "wb") as file:
            file.write(stream_bytes)

    import os
#    os.startfile("./aws_voice.mp3")
#    os.system("audiodg ./aws_voice.mp3")

save_stream_from_response(
    ApiConsumer().synthesize(
        voice_id = 'Lea',
        text="Bonjour Julien, comment allez-vous ?"
    )
)
