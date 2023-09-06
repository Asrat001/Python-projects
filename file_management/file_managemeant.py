import os
source_dir ="/home/asrat/Downloads" 
dist_dir_img ="/home/asrat/Downloads/images"
dist_dir_pdf="/home/asrat/Downloads/pdfs"
dist_dir_music="/home/asrat/Downloads/musics"
dist_dir_video="/home/asrat/Downloads/videos"

with os.scandir(source_dir) as enteries:
        for entry in enteries:
                print(entry)


