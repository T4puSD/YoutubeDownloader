from pafy.backend_shared import BasePafy
from pafy.backend_youtube_dl import YtdlStream

from YTDownloader.Exceptions.general_exception import NotFoundException
from YTDownloader.Library.Media.MediaFile import MediaFile


def _get_video_pafy_obj(pafy_obj: BasePafy):
    stream_obj = None
    for stream in pafy_obj.videostreams[::-1]:
        if stream.extension == 'mp4':
            if stream.dimensions[0] == 1920 and stream.dimensions[1] == 1080:
                stream_obj = stream
                break

    if stream_obj is None:
        raise NotFoundException("Video Stream Not Found")

    return stream_obj


class VideoFile(MediaFile):
    def __init__(self, pafy_obj: BasePafy):
        super().__init__(pafy_obj)
        self._video_obj = _get_video_pafy_obj(pafy_obj)

    def get_pafy_stream(self) -> YtdlStream:
        return self._video_obj

    def get_media_type_extension(self) -> str:
        return "mp4"
