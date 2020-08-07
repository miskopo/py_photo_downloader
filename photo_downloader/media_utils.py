from datetime import datetime as dt
from typing import BinaryIO

from exifread import process_file

from photo_downloader import logger


class MediaUtils:
    @staticmethod
    def obtain_capture_date(file: BinaryIO) -> dt.date:
        tags = process_file(file)
        date: dt.date = None
        try:
            date_str: str = str(tags['Image DateTimeOriginal']).split(' ')[0]
            date = dt.strptime(date_str, "%Y:%m:%d").date()
        except KeyError:
            logger.error("Date attribute not found")
            raise
        except ValueError:
            logger.error("Invalid date format")
            raise
        return date
