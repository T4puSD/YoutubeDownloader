import pafy
import time
import enum
from YTDownloader.Configuration.debugger import logging


class FormatType(enum.Enum):
    AUDIO = 1
    VIDEO = 2


def _get_pafy_stream_obj(url, format_type=None, only_video=False):
    try:
        obj = pafy.new(url)
        # returning only the pafy obj if format is not given
        if format_type is None:
            return obj

        stream_obj = None
        # returning format specified in the parameter
        if format_type == FormatType.AUDIO:
            logging.debug("Getting audio pafy stream_object")
            stream_obj = obj.getbestaudio(preftype='m4a')
        if format_type == FormatType.VIDEO:
            if only_video:
                # get only video at 1080p
                # stream_obj = obj.getbestvideo(preftype='mp4')

                ## iterating from backward as best streams are there and
                ## slecting best 1920x1080p mp4 stream
                logging.debug("Getting HQ video pafy stream_object")
                for stream in obj.videostreams[::-1]:
                    if stream.extension == 'mp4':
                        if stream.dimensions[0] == 1920 and stream.dimensions[1] == 1080:
                            stream_obj = stream
                            break
            else:
                # get best will return both audio and obj normally at 640p
                logging.debug("Getting normal-video pafy stream_object")
                stream_obj = obj.getbest(preftype='mp4')
        return stream_obj

    except OSError as e:
        logging.debug("OSError in new pafy")
        logging.debug(e)
        raise OSError
    except Exception as e:
        logging.debug("Error occured in new pafy")
        logging.debug(e)
        return None


def get_pafy_obj(url, file_format_type=None, only_video=False):
    # trying to get stream obj from pafy
    # until the object is received without an error
    # the while loop keeps requesting pafy
    # if video is not available in youtube
    # gives OSError and breaks the loop
    timeout = 5
    pafy_obj = None
    while pafy_obj is None and timeout > 0:
        try:
            pafy_obj = _get_pafy_stream_obj(url, file_format_type, only_video)
            time.sleep(1)
            timeout -= 1
        except OSError:
            logging.debug("Video is not available in Youtube.")
            logging.debug("Link: " + url)
            break
        except Exception as e:
            logging.debug("Error occurred in pafy")
            logging.debug(e)

    return pafy_obj
