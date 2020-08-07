from photo_downloader.file_system_utils import FileSystemUtils
from photo_downloader.io_utils import confirm_validity


def main():
    fsu = FileSystemUtils()
    fsu.list_file_types()
    print("These media files will be imported to current folder.")
    if confirm_validity():
        fsu.copy_files_to_target_folders()
    return 0


if __name__ == '__main__':
    main()
