import vlc
import win32gui
import time
from config import VIDEO_WIDTH,VIDEO_HEIGHT

class VideoPlayer:

    def __init__(self, video_path):

        self.video_path = str(video_path)
        self.instance=vlc.Instance()
        self.player = None

    def play(self):

        if self.is_playing():
            return
        self.finished = False

        self.player=self.instance.media_player_new()

        # Load video
        media = self.instance.media_new(self.video_path)
        self.player.set_media(media)

        # Play video
        self.player.play()

        # Waiting for VLC
        time.sleep(0.5)

        hwnd = self.player.get_hwnd()

        if hwnd:
            win32gui.SetWindowPos(
                hwnd,
                0,
                0,
                0,
                VIDEO_WIDTH,
                VIDEO_HEIGHT,
                0x0004
            )

    def is_playing(self):

        if self.player is None:
            return False

        state = self.player.get_state()

        return state in [
            vlc.State.Opening,
            vlc.State.Playing,
            vlc.State.Buffering,
        ]
    
    def has_finished(self):

        if self.player is None:
            return False

        state = self.player.get_state()

        return state == vlc.State.Ended

    def update(self):

        """
        Check whether the video has finished.
        """

        if self.player is None:
            return

        if self.has_finished():
            self.close()


    def close(self):

        if self.player is not None:

            try:
                self.player.stop()
            except Exception:
                pass

            try:
                self.player.release()
            except Exception:
                pass

            self.player = None

