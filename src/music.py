import subprocess


def shoop():
    omx_instructions = [
        "aplay",
        "/home/pi/Music/Shoop.mp3",
    ]
    print(" ".join(omx_instructions))
    subprocess.call(omx_instructions, stdin=subprocess.PIPE)
