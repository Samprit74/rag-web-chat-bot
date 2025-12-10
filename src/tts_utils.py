# tts_utils.py

import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))


def speak_text(text: str, filename: str = "answer.mp3") -> str:
    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Default natural voice
        model_id="eleven_multilingual_v2",
        text=text
    )

    with open(filename, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return filename
