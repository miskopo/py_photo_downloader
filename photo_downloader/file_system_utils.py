from psutil import disk_partitions
from pyudev import Context, Device

from photo_downloader.user_input_utils import numerical_choice


class FileSystemUtils:
    @staticmethod
    def _create_folder(path: str) -> None:
        pass

    @staticmethod
    def find_memory_card() -> str:
        context : Context = Context()
        devices: [Device] = context.list_devices(subsystem="block", DEVTYPE='partition')
        print("Choose a device to import from:")
        for i, device in enumerate(devices):
            print(f"{i+1}. {device.get('ID_FS_LABEL') if device.get('ID_FS_LABEL') else 'Internal'}: {device.device_node} ({device.get('ID_FS_TYPE')}) - {device.get('ID_MODEL')}")
        choice: int = numerical_choice(min=1, max=len(list(devices)), prompt="Your choice?")
        for p in disk_partitions():
            if p.device == list(devices)[choice-1].device_node:
                return p.mountpoint

    @staticmethod
    def list_media_on_memory_card() -> None:
        pass