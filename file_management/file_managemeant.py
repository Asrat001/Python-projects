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

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

#helper functions
def make_unique_name(dist,name):
    filename,extension=splitext(name)
    count=1
    while exists(f"{dist}/{name}"):
           name=f"{filename}({str(count)}){extension}"
           count+=1

    return name       
def move_file(dest,name,entry): 
    if exists(f"{dest}/{name}"):
        unique_name=make_unique_name(dest,name) 
        old_name=join(dest,name)
        new_name=join(dest,unique_name)
        rename(old_name,new_name)    
    move(entry,dest)


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