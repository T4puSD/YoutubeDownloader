import ffmpeg
from YTDownloader.debugger import logging


def convert_to_audio(input_file_path, output_file_path):
    logging.info("Converting To Audio")
    stream = ffmpeg.input(input_file_path)
    stream = ffmpeg.output(stream.audio, output_file_path)
    ffmpeg.run(stream)
    logging.info("Conversion Completed!")
