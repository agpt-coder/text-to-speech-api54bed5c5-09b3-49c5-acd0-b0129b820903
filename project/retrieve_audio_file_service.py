import prisma
import prisma.models
from pydantic import BaseModel


class RetrieveAudioFileResponse(BaseModel):
    """
    A response model containing the audio file streamed back to the user.
    """

    audio_file: bytes
    file_name: str
    content_type: str


async def retrieve_audio_file(fileID: str) -> RetrieveAudioFileResponse:
    """
    Serves the generated audio file for user download.

    This function queries the database for the specified audio file using its unique ID.
    If the file exists, it retrieves the file's binary data and returns a response model containing the audio file data alongside its metadata.

    Args:
        fileID (str): The unique identifier for the requested audio file.

    Returns:
        RetrieveAudioFileResponse: A response model containing the audio file streamed back to the user.

    Raises:
        ValueError: If no audio file is found with the provided ID.

    Example:
        fileID = 'some-unique-file-id'
        response = await retrieve_audio_file(fileID)
        # response now contains the binary data of the audio file, its name, and the MIME type
    """
    audio_file_record = await prisma.models.TextConversionJob.prisma().find_unique(
        where={"id": fileID}
    )
    if not audio_file_record or not audio_file_record.audioFileUrl:
        raise ValueError("File not found or URL is missing.")
    try:
        with open(audio_file_record.audioFileUrl, "rb") as file:
            audio_content = file.read()
    except FileNotFoundError:
        raise ValueError("Audio file does not exist.")
    return RetrieveAudioFileResponse(
        audio_file=audio_content, file_name=f"{fileID}.mp3", content_type="audio/mpeg"
    )
