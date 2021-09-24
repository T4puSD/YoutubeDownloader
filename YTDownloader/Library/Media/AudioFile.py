from pafy.backend_shared import BasePafy
from pafy.backend_youtube_dl import YtdlStream

from YTDownloader.Exceptions.general_exception import IllegalArgumentException, NotFoundException
from YTDownloader.Library.Media.MediaFile import _MediaFile


class AudioFile(_MediaFile):
    def __init__(self, pafy_obj: BasePafy):
        super().__init__(pafy_obj)
        self._audio_obj = pafy_obj.getbestaudio(preftype='m4a')

    def get_pafy_stream(self) -> YtdlStream:
        return self._audio_obj

    def get_media_type_extension(self) -> str:
        return "mp3"

    def start_download(self, absolute_path: str) -> None:
        if absolute_path is None:
            raise IllegalArgumentException("absolute_path can not be None")

        pafy_stream = self.get_pafy_stream()
        if pafy_stream is None:
            raise NotFoundException("Unable to find pafy stream for download")

        pafy_stream.download(absolute_path)
