from pafy.backend_shared import BasePafy

from YTDownloader.Model.MediaFile import MediaFile


class AudioFile(MediaFile):
    def __init__(self, pafy_obj: BasePafy):
        super().__init__(pafy_obj)
        self._audio_obj = pafy_obj.getbestaudio(preftype='m4a')

    def get_pafy_stream(self):
        return self._audio_obj

    def get_media_type_extension(self) -> str:
        return "mp3"

