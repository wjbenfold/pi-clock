import subprocess


def shoop():
    subprocess.call(["setterm", "--blank", "poke", "> /dev/tty"])
    omx_instructions = [
        "mpg123",
        "/home/pi/Music/Shoop.mp3",
    ]
    print(" ".join(omx_instructions))
    subprocess.call(omx_instructions, stdin=subprocess.PIPE)
