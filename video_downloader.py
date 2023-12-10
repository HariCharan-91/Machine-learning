# video_downloader.py
import streamlit as st
import yt_dlp
import os
import subprocess
import tempfile
import api_commu

from audio import main as audio_main # Importing the main function from audio.py
# from summrzn import summarize_text

def display_success_message():
    st.success("Process completed successfully!")


def download_and_convert_media(media_input, output_path="."):
    options = {
        'format': 'best',
        'outtmpl': f"{output_path}/%(title)s.%(ext)s",
    }

    info_dict = {}  # Initialize info_dict as an empty dictionary

    with yt_dlp.YoutubeDL(options) as ydl:
        # If the input is a valid URL, download it
        if isinstance(media_input, str) and media_input.startswith("http"):
            info_dict = ydl.extract_info(media_input, download=True)
            media_path = ydl.prepare_filename(info_dict)
        elif media_input:
            # If it's a local file, save it to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(media_input.read())
                media_path = temp_file.name
        else:
            st.error("Invalid media input.")
            return None, None

        # Replace special characters in the title with underscores
        sanitized_title = "".join(c if c.isalnum() or c in [' ', '.'] else '_' for c in info_dict.get('title', ''))

        # Extract the audio from the video
        audio_path = os.path.join(output_path, f"{sanitized_title}.wav")
        audio_command = f'ffmpeg -i "{media_path}" -ab 160k -ar 44100 -vn "{audio_path}"'
        subprocess.run(audio_command, shell=True)

        return media_path, audio_path, sanitized_title

def display_success_message():
    st.header("Transcription Result")
    st.success("Text generation is successful!")


def main():
    st.title("Media Converter")

    media_input = st.text_input("Enter YouTube Video URL or Local Video File:")
    media_file = st.file_uploader("Upload a Local Video File:", type=["mp4", "webm"])

    if media_input:
        st.write(f"Media Input: {media_input}")
    elif media_file:
        st.write(f"Uploaded File: {media_file.name}")

    if st.button("Convert"):
        progress_bar = st.progress(0)

        if media_input or media_file:
            with st.spinner("Converting..."):
                media_path, audio_path, sanitized_title = download_and_convert_media(media_input or media_file, "downloads")

            if media_path and audio_path:
                st.success("Conversion completed successfully!")

                st.audio(audio_path, format="audio/wav")

                video_path = media_path.replace(".webm", ".mp4")
                if os.path.exists(video_path):
                    st.video(video_path, format="video/mp4")

                # Call the audio conversion and transcription
                audio_main(os.path.join("downloads", f"{sanitized_title}.wav"))
                # pdf_file_path = os.path.join("downloads", f"{sanitized_title}.pdf")
                # convert_text_to_pdf(text_file_path, pdf_file_path)

                # Perform text summarization
                
                

                # Display the text summarization result
                # st.header("Text Summarization Result")
                # st.success(text_result)

                # Display success message
                display_success_message()
                print(sanitized_title)
        

if __name__ == "__main__":
    main()