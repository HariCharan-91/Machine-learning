# audio.py

import sys
from api_commu import *

def main(filename):
    audio_url = upload(filename)
    save_transcript(audio_url, filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audio.py <filename>")
        sys.exit(1)

    main(sys.argv[1])
