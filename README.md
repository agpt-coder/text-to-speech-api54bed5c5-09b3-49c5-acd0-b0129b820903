---
date: 2024-04-16T16:44:11.268732
author: AutoGPT <info@agpt.co>
---

# Text-to-Speech API

To accomplish the task of accepting plain text input from a user, converting this text to natural-sounding speech audio using a popular Python package, and returning the generated audio file within a FastAPI application, the following steps and technologies will be integrated based on the information gathered so far:

1. **Text-to-Speech Conversion**: The gTTS (Google Text-to-Speech) library, or alternatively pyttsx3 for offline capabilities, will be used for converting the provided text to speech. Given the user's preference for a female voice in the text-to-speech conversion, gTTS allows for specifying the voice type, and pyttsx3 provides controls over voice properties including gender.

2. **FastAPI Endpoint Setup**: A FastAPI endpoint will be created to accept plain text input from the user. This can be achieved by defining a POST endpoint which accepts a JSON payload containing the text to be converted.

3. **Handling File Upload and Response**: The application will convert the input text to audio, save the audio file temporarily on the server, and then return the audio file to the user. The FastAPI tutorial for handling file uploads and responses provides the necessary guidance on implementing file handling, specifically using `File` and `UploadFile` for asynchronous operations.

4. **Saving Audio Files**: Although the project requirement focuses on returning the generated audio file rather than saving it, the capability to save audio files in PostgreSQL using the BYTEA data type or the Large Object functionality has been explored. This information could be useful for potential future requirements regarding audio file storage.

5. **Database Management with Prisma**: The integration of Prisma with FastAPI for database management has been researched. While not directly applicable to the current task focused on text-to-speech conversion and file handling, this knowledge is critical for broader application functionality concerning database operations.

In summary, the application will leverage either the gTTS or pyttsx3 library for text-to-speech conversion, with a preference for a female voice as indicated by the user. The FastAPI framework will be utilized to create an endpoint for handling the text input and audio file return process, incorporating lessons from the explored tutorial. While database storage for audio files has been considered, the immediate task will concentrate on the conversion and direct return of the audio file to the user.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Text-to-Speech API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
