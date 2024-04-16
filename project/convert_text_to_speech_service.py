import tempfile
import uuid

from gtts import gTTS
from pydantic import BaseModel


class TextToSpeechResponse(BaseModel):
    """
    Response model for text-to-speech conversion, providing the generated audio file.
    """

    audio_file_url: str
    status: str
    message: str


def convert_text_to_speech(
    text: str,
    language: str = "en",
    voice_gender: str = "female",
    speech_rate: float = 1.0,
    pitch: float = 1.0,
) -> TextToSpeechResponse:
    """
    Converts provided text to speech audio, returning the audio file.

    Utilizes the Google Text-to-Speech library (gTTS) for conversion, taking into account specified language,
    voice gender (ignored in gTTS, included for compatibility), speech rate, and pitch (both ignored in gTTS,
    included for compatibility).

    Args:
        text (str): The user's input text to be converted to speech.
        language (str, optional): Language code for the speech conversion. Defaults to 'en'.
        voice_gender (str, optional): Preference for the voice gender. Defaults to 'female'.
        speech_rate (float, optional): Speech rate for the conversion. Defaults to 1.0.
        pitch (float, optional): Pitch level for the speech. Defaults to 1.0.

    Returns:
        TextToSpeechResponse: Response model for text-to-speech conversion, providing the generated audio file.
    """
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
            tts.save(temp_filename)
            audio_file_url = f"https://example.com/audio/{uuid.uuid4()}.mp3"
            response = TextToSpeechResponse(
                audio_file_url=audio_file_url,
                status="COMPLETED",
                message="Text-to-speech conversion successful.",
            )
            return response
    except Exception as e:
        return TextToSpeechResponse(
            audio_file_url="",
            status="FAILED",
            message=f"An error occurred during conversion: {str(e)}",
        )
