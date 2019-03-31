import os,errno
import sys
from PIL import Image

resize_images = True

def compressMeReturn(file, outfile, maxDim, verbose=False):
    if not resize_images:
        return False
    filepath = os.path.join(os.getcwd(), file)
    oldsize = os.stat(filepath).st_size
    #print(filepath)
    picture = Image.open(filepath)
    dim = picture.size

    if dim[0]>maxDim:
        #ratio = (maxDim/dim[0],maxDim/dim[1])
        ratio = dim[0]/dim[1]
        picture.thumbnail((maxDim,maxDim*ratio), Image.ANTIALIAS)
    compressed_filepath = os.path.join(os.getcwd(), outfile)
    picture.save(compressed_filepath,"JPEG",optimize=True,quality=85)

    newsize = os.stat(compressed_filepath).st_size
    percent = (oldsize-newsize)/float(oldsize)*100
    if (verbose):
        print("File compressed from {0} to {1} or {2}%".format(oldsize,newsize,percent))
    return int(percent)

def make_way(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

folder = 'printing_progress'
out_folder = os.path.join(folder, 'compressed')
make_way(out_folder)
for file in os.listdir(folder):
    if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
        in_path = os.path.join(folder,file)
        print(in_path)
        out_path = os.path.join(out_folder, file)
        print(out_path)
        thumb_path = os.path.join(out_folder, file)
        thumb_path = thumb_path.split('.')
        thumb_path[-2] += '-thumb'
        thumb_path = '.'.join(thumb_path)
        print(thumb_path)
        print(compressMeReturn(in_path, out_path, 1600))
        print(compressMeReturn(in_path, thumb_path, 400))