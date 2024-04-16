import io
import logging
from contextlib import asynccontextmanager

import prisma
import project.convert_text_to_speech_service
import project.retrieve_audio_file_service
import project.status_check_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, StreamingResponse
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Text-to-Speech API",
    lifespan=lifespan,
    description="""To accomplish the task of accepting plain text input from a user, converting this text to natural-sounding speech audio using a popular Python package, and returning the generated audio file within a FastAPI application, the following steps and technologies will be integrated based on the information gathered so far:

1. **Text-to-Speech Conversion**: The gTTS (Google Text-to-Speech) library, or alternatively pyttsx3 for offline capabilities, will be used for converting the provided text to speech. Given the user's preference for a female voice in the text-to-speech conversion, gTTS allows for specifying the voice type, and pyttsx3 provides controls over voice properties including gender.

2. **FastAPI Endpoint Setup**: A FastAPI endpoint will be created to accept plain text input from the user. This can be achieved by defining a POST endpoint which accepts a JSON payload containing the text to be converted.

3. **Handling File Upload and Response**: The application will convert the input text to audio, save the audio file temporarily on the server, and then return the audio file to the user. The FastAPI tutorial for handling file uploads and responses provides the necessary guidance on implementing file handling, specifically using `File` and `UploadFile` for asynchronous operations.

4. **Saving Audio Files**: Although the project requirement focuses on returning the generated audio file rather than saving it, the capability to save audio files in PostgreSQL using the BYTEA data type or the Large Object functionality has been explored. This information could be useful for potential future requirements regarding audio file storage.

5. **Database Management with Prisma**: The integration of Prisma with FastAPI for database management has been researched. While not directly applicable to the current task focused on text-to-speech conversion and file handling, this knowledge is critical for broader application functionality concerning database operations.

In summary, the application will leverage either the gTTS or pyttsx3 library for text-to-speech conversion, with a preference for a female voice as indicated by the user. The FastAPI framework will be utilized to create an endpoint for handling the text input and audio file return process, incorporating lessons from the explored tutorial. While database storage for audio files has been considered, the immediate task will concentrate on the conversion and direct return of the audio file to the user.""",
)


@app.post(
    "/convert",
    response_model=project.convert_text_to_speech_service.TextToSpeechResponse,
)
async def api_post_convert_text_to_speech(
    text: str, language: str, voice_gender: str, speech_rate: float, pitch: float
) -> project.convert_text_to_speech_service.TextToSpeechResponse | Response:
    """
    Converts provided text to speech audio, returning the audio file.
    """
    try:
        res = project.convert_text_to_speech_service.convert_text_to_speech(
            text, language, voice_gender, speech_rate, pitch
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/audio/{fileID}")
async def api_get_retrieve_audio_file(fileID: str) -> StreamingResponse:
    """
    Serves the generated audio file for user download.
    """
    try:
        res = await project.retrieve_audio_file_service.retrieve_audio_file(fileID)

        headers = {"Content-Disposition": f"attachment; filename={res.file_name}"}

        return StreamingResponse(
            content=res.data, media_type=res.media_type, headers=headers
        )

    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/status", response_model=project.status_check_service.StatusCheckResponse)
async def api_get_status_check() -> project.status_check_service.StatusCheckResponse | Response:
    """
    Provides status check for API health and availability.
    """
    try:
        res = await project.status_check_service.status_check()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
