from enum import Enum


class DownloadMode(Enum):
    SINGLE = 0
    PLAYLIST = 1


class MediaType(Enum):
    AUDIO = 0,
    VIDEO = 0


class VideoQuality(Enum):
    Q360P = 0
    Q480P = 1,
    Q1080P = 2
