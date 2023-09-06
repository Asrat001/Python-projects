from os import scandir ,rename
from os.path import exists , splitext, join
from  shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
source_dir ="/home/asrat/Downloads" 
dist_dir_img ="/home/asrat/Downloads/images"
dist_dir_pdf="/home/asrat/Downloads/pdfs"
dist_dir_music="/home/asrat/Downloads/musics"
dist_dir_video="/home/asrat/Downloads/videos"



class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("heyee")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()