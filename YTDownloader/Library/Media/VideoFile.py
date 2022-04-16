from pafy.backend_shared import BasePafy
from pafy.backend_youtube_dl import YtdlStream

from YTDownloader.Enums import VideoQuality
from YTDownloader.Exceptions.general_exception import NotFoundException, IllegalArgumentException
from YTDownloader.Library.Media.MediaFile import _MediaFile


def _get_video_pafy_obj(pafy_obj: BasePafy, video_quality: VideoQuality):
    stream_obj = None
    if video_quality is VideoQuality.Q360P:
        stream_obj = pafy_obj.getbest(preftype='mp4')

    if video_quality is VideoQuality.Q1080P:
        for stream in pafy_obj.videostreams[::-1]:
            if stream.extension == 'mp4':
                if stream.dimensions[0] == 1920 and stream.dimensions[1] == 1080:
                    stream_obj = stream
                    break

    if stream_obj is None:
        raise NotFoundException("Video Stream Not Found")

    return stream_obj


class VideoFile(_MediaFile):
    def __init__(self, pafy_obj: BasePafy, video_quality: VideoQuality):
        if video_quality is None:
            raise IllegalArgumentException("Video quality can not be None")

        super().__init__(pafy_obj)
        self._video_quality = video_quality
        self._video_obj = _get_video_pafy_obj(pafy_obj, video_quality)

    def get_pafy_stream(self) -> YtdlStream:
        if self._video_obj is None:
            raise NotFoundException("Unable to find pafy stream for download! \
            Try again later or Try updating 'youtube-dl' dependency")

        return self._video_obj

    def get_media_type_extension(self) -> str:
        return "mp4"

    def get_download_dir(self) -> str:
        return self.get_config().get_download_dir_video

    @property
    def get_video_quality(self):
        return self._video_quality

    def start_download(self) -> None:
        pafy_stream = self.get_pafy_stream()
        # Preparing download directory
        self._prepare_download_dir()
        # Check if file already exists
        self._check_if_file_already_exist()
        # Download
        pafy_stream.download(self.get_download_path())

