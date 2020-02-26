from photo_downloader.file_system_utils import FileSystemUtils as fsu

if __name__ == '__main__':
    fsu._sort_files_by_mimetype(fsu._list_media_on_import_source())