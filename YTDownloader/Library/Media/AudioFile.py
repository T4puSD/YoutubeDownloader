import os

from pafy.backend_shared import BasePafy
from pafy.backend_youtube_dl import YtdlStream

from YTDownloader.Exceptions.general_exception import NotFoundException
from YTDownloader.Library.Media.MediaFile import _MediaFile
from YTDownloader.Library.Media.MetaDataEditor import add_title, add_picture
from YTDownloader.Library.Media.Converter import convert_to_audio


class AudioFile(_MediaFile):
    def __init__(self, pafy_obj: BasePafy):
        super().__init__(pafy_obj)
        self._audio_obj = pafy_obj.getbestaudio(preftype='m4a')

    def get_pafy_stream(self) -> YtdlStream:
        return self._audio_obj

    def get_media_type_extension(self) -> str:
        return "mp3"

    def get_download_dir(self) -> str:
        return self.get_config().get_download_dir_audio

    def start_download(self) -> None:
        pafy_stream = self.get_pafy_stream()
        if pafy_stream is None:
            raise NotFoundException("Unable to find pafy stream for download! \
            Try again later or Try updating 'youtube-dl' dependency")

        # Preparing download directory
        self._prepare_download_dir()
        # Check if file already exists
        self._check_if_file_already_exist()
        # Download
        pafy_stream.download(self.get_download_path())
        # Convert
        convert_to_audio(self.get_download_path(), self.get_conversion_output_path())
        # Remove m4a file
        os.remove(self.get_download_path())
        # Add MetaData
        add_title(self.get_conversion_output_path(), self._title)
        add_picture(self.get_conversion_output_path(), self.get_thumbnail())
