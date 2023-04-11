import signal
import sys
import textwrap
import threading
import tkinter as tk
import soundfile as sf
from queue import Queue
from utils.subtitle import *

# Position of Subtitle, offset from bottom middle of screen
OFFSET_X = 0
OFFSET_Y = -200

# The font size of subtitle text
SUBTITLE_FONT_SIZE = 35

# The color of subtitle text
SUBTITLE_COLOR = "white"

# The background color of your subtitles
SUBTITLE_BG_COLOR = "black"

# The color that will be considered transparent
# Put the same value as SUBTITLE_BG_COLOR so background of subtitles will be transparent as well
# Putting the same value as SUBTITLE_COLOR will cause your subtitles to be invisible
SACRIFICIAL_COLOR = "black"


def subtitle_updater(root, queue, label):
    # Check if there is something new in the queue to display.
    while not queue.empty():
        # destroy old label since new message inbound
        label.destroy()
        if root.wm_state() == "withdrawn":
            # show root window
            root.deiconify()

        # create subtitle based on message in queue
        msg = queue.get()
        label = tk.Label(
            text=textwrap.fill(msg, 64),
            font=("Comic Sans MS", SUBTITLE_FONT_SIZE, "bold italic"),
            fg=SUBTITLE_COLOR,
            bg=SUBTITLE_BG_COLOR,
        )

        duration = get_tts_duration() + 500

        # hide root and destroy label after tts duration ends
        label.after(duration, root.withdraw)
        label.after(duration, label.destroy)

        # place subtitle at bottom middle of screen
        label.pack(side="bottom", anchor="s")
        root.update_idletasks()

    # run every 0.5s
    root.after(50, lambda: subtitle_updater(root, queue, label))


def get_tts_duration():
    f = sf.SoundFile("output.wav")
    return int(f.frames / f.samplerate * 1000)


def setup_overlay():
    # set tkinter gui to be topmost without window
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(
        f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+{OFFSET_X}+{OFFSET_Y}"
    )
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)

    # Sacrifice random color for transparency
    root.wm_attributes("-transparentcolor", SACRIFICIAL_COLOR)
    root.config(bg=SACRIFICIAL_COLOR)

    # hide initial window
    root.withdraw()

    return root


def close_app(*_):
    print("Closing subtitle overlay")
    sys.exit(0)


def start_app():
    # catch keyboard interrupt to stop main thread
    signal.signal(signal.SIGINT, close_app)

    overlay = setup_overlay()
    subtitle = tk.Label()
    subtitle_queue = Queue()

    # thread to listen and translate audio
    threading.Thread(
        target=enqueue_subtitle, args=[subtitle_queue], daemon=True
    ).start()

    # updates subtitles every 0.5s by checking queue
    subtitle_updater(overlay, subtitle_queue, subtitle)

    # set full-screen applications to borderless window for subtitles to appear over it
    overlay.mainloop()


if __name__ == "__main__":
    start_app()