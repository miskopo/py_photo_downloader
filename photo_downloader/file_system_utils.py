import os
import shutil
from collections import deque
from io import BufferedReader
from os import scandir

import click as click
from magic import from_file
from psutil import disk_partitions
from pyudev import Context, Device

from photo_downloader import logger
from photo_downloader.io_utils import numerical_choice, DIVIDER
from photo_downloader.media_utils import MediaUtils


class FileSystemUtils:
    __slots__ = ["device_mount_point", "sorted_files"]

    def __init__(self):
        self.device_mount_point: str
        self.sorted_files: dict = {"raw": None, "processed": None, "video": ""}
        self._choose_import_source()

    def _choose_import_source(self):
        context: Context = Context()
        devices: [Device] = context.list_devices(subsystem="block", DEVTYPE='partition')
        print("Choose a device to import from:")
        for i, device in enumerate(devices):
            print(
                f"{i + 1}. {device.get('ID_FS_LABEL') if device.get('ID_FS_LABEL') else 'Internal'}: "
                f"{device.device_node} ({device.get('ID_FS_TYPE')}) - {device.get('ID_MODEL')}")
        choice: int = numerical_choice(min_value=1, max_value=len(list(devices)), prompt="Your choice?")
        for p in disk_partitions():
            if p.device == list(devices)[choice - 1].device_node:
                self.device_mount_point = p.mountpoint

    def _find_media_on_import_source(self) -> [str]:
        subfolders = []
        perm_error_flag = False

        def _fast_scandir(subfolder):
            subdirs = [f.path for f in scandir(subfolder) if f.is_dir()]
            for subfolder in list(subdirs):
                subdirs.extend(_fast_scandir(subfolder))
            return subdirs

        files: [str] = deque()
        try:
            subfolders = _fast_scandir(self.device_mount_point)
        except PermissionError:
            perm_error_flag = True
        if not subfolders:
            subfolders = [self.device_mount_point]
        for folder in subfolders:
            try:
                files.extend(list([file.path for file in scandir(folder) if not file.is_dir()]))
            except PermissionError:
                perm_error_flag = True

        if perm_error_flag:
            logger.error("Some files were skipped due the permission errors.")
        return files

    def _sort_files_by_mimetype(self, files: deque):
        """
        Sort found files into categories raw, processed and video files.
        :param files: list of paths of found files from import source
        :return: dictionary with fields raw, processed and video and respective lists of paths
        """
        raw_image_files: deque = deque([file for file in files if from_file(file, mime=True) == 'image/tiff'])
        processed_image_files: deque = deque([file for file in files if from_file(file, mime=True) == 'image/jpeg'])
        video_files: [str] = deque([file for file in files if from_file(file, mime=True).startswith("video")])

        self.sorted_files = {
            "raw": raw_image_files,
            "processed": processed_image_files,
            "video": video_files
        }

    @staticmethod
    def _create_folder(path: str) -> str:
        try:
            os.makedirs(path, exist_ok=True)
            return path
        except PermissionError as e:
            logger.error(f"Unable to create folder {path}: {str(e)}, exiting.")
            exit(4)     # TODO: Note 4 means permission error

    def list_file_types(self):
        self._sort_files_by_mimetype(self._find_media_on_import_source())
        print(DIVIDER)
        print("Following file types were found on selected device: ")
        for key in self.sorted_files.keys():
            print(f"{key}: {len(self.sorted_files[key])}")

    def copy_files_to_target_folders(self):
        continue_copying = True
        for type in ["raw", "processed", "video"]:
            with click.progressbar(self.sorted_files[type], show_pos=True, label=f"Importing {type} files") as bar:
                for file_path in bar:
                    try:
                        if continue_copying:
                            logger.debug(file_path)
                            with open(file_path, 'rb') as file:
                                date = MediaUtils.obtain_capture_date(file)
                            # Folder format currently hardcoded to YYYY/MM/DD
                            dest = self._create_folder(f"{date.year}/{date.month}/{date.day}")
                            shutil.copy2(file_path, dest)
                        else:
                            break
                    except KeyboardInterrupt:
                        print("Closing copy/paste stream")
                        continue_copying = False
                        continue
