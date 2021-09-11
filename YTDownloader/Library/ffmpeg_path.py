import platform
import os

class FfmpegPath:
    def getFFmpegExecutablePath():
        if platform.system() == 'Linux':
            return 'ffmpeg'
        if platform.system() == 'Windows':
            return 'plugins' + os.sep + 'ffmpeg.exe'


if __name__ == '__main__':
    ffmpeg_path = FfmpegPath.getFFmpegExecutablePath()
    print(ffmpeg_path)
