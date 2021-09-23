from pafy.backend_shared import BasePafy

from YTDownloader.Exceptions.general_exception import NotFoundException
from YTDownloader.Library.title_slugify import TitleSlugify


class MediaFile:
    def __init__(self, pafy_obj: BasePafy):
        if pafy_obj is None:
            raise NotFoundException("Pafy object can not be none")
        self._title = pafy_obj.title
        self._audio_obj = pafy_obj.getbestaudio(preftype='m4a')
        self._author = pafy_obj.author
        self._thumbnail_small = pafy_obj.thumb
        self._thumbnail_big = pafy_obj.bigthumb
        self._thumbnail_hd = pafy_obj.bigthumbhd
        self._title_slugify = TitleSlugify()

    def get_title(self):
        if self._title is None:
            raise NotFoundException("Media Title not found")
        return self._title_slugify.slugify_for_windows(self._title)

    def get_audio_obj(self):
        if self._audio_obj is None:
            raise NotFoundException("Audio Stream Not Found")
        return self._audio_obj

    @property
    def get_author(self):
        return self._author

    @property
    def get_thumbnail_small(self):
        return self._thumbnail_small

    @property
    def get_thumbnail_big(self):
        return self._thumbnail_big

    @property
    def get_thumbnail_hd(self):
        return self._thumbnail_hd

    def get_audio_extension(self):
        if self._audio_obj is None:
            raise NotFoundException("Audio Object Not Found")
        return self._audio_obj.extension

    def get_audio_title(self):
        return self.get_title() + "." + self.get_audio_extension()

    def get_mp3_title(self):
        return self.get_title() + "." + ".mp3"
