from os import scandir

from magic import from_file
from psutil import disk_partitions
from pyudev import Context, Device

from photo_downloader.user_input_utils import numerical_choice


class FileSystemUtils:

    @staticmethod
    def _choose_import_source() -> str:
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
                return p.mountpoint

    @staticmethod
    def _find_media_on_import_source() -> [str]:

        def _fast_scandir(subfolder):
            subdirs = [f.path for f in scandir(subfolder) if f.is_dir()]
            for subfolder in list(subdirs):
                subdirs.extend(_fast_scandir(subfolder))
            return subdirs

        mmc_path: str = FileSystemUtils._choose_import_source()
        files: [str] = []
        subfolders = _fast_scandir(mmc_path)
        if not subfolders:
            subfolders = [mmc_path]
        for folder in subfolders:
            files.extend(list([file.path for file in scandir(folder) if not file.is_dir()]))

        return files

    @staticmethod
    def _sort_files_by_mimetype(files: [str]) -> dict:
        """
        Sort found files into categories raw, processed and video files.
        :param files: list of paths of found files from import source
        :return: dictionary with fields raw, processed and video and respective lists of paths
        """
        raw_image_files: [str] = [file for file in files if from_file(file, mime=True) == 'image/tiff']
        processed_image_files: [str] = [file for file in files if from_file(file, mime=True) == 'image/jpeg']
        video_files: [str] = [file for file in files if from_file(file, mime=True).startswith("video")]

        return {
            "raw": raw_image_files,
            "processed": processed_image_files,
            "video": video_files
        }

    @staticmethod
    def _create_folder(path: str) -> None:
        pass
