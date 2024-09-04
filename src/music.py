import subprocess


def shoop():
    omx_instructions = [
        "omxplayer",
        "-o",
        "local",
        "--vol",
        "-1500",
        "/home/pi/Music/Shoop.mp3",
    ]
    print(" ".join(omx_instructions))
    subprocess.call(omx_instructions, stdin=subprocess.PIPE)
