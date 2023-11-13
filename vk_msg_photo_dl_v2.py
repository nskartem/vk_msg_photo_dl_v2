import sys
import getopt
import os
from bs4 import BeautifulSoup
import re
# import csv

# Type of processing:
# 1 - process all messages first, then download all files
# 2 - download all files in processed dir after processing it
proc_mode = 2
# Working directory (where your index-messages.html is placed)
wdir = "."
# list of subdirs to process
dirnames = []
# list of subdir files to process
filenames = []
# dicts for saving parsing results
# dict format:
# id, url, timestamp
images = {}
files = {}
videos = {}
voice_msgs = {}
# regex pattern for messageXXXX.html files
fname_regex = re.compile("^messages[0-9]+\.html$")


# get input params from console
def get_args(cli_args):
    global proc_mode
    global wdir
    try:
        opts, args = getopt.getopt(cli_args, "hp:w:", ["pmode=", "workdir="])
    except getopt.GetoptError:
        print('vk_msg_photo_dl_v2.py -p <process_mode> -w <workdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('vk_msg_photo_dl_v2.py -p <process_mode> -w <workdir>')
            sys.exit()
        elif opt in ("-p", "--pmode"):
            proc_mode = arg
        elif opt in ("-w", "--workdir"):
            wdir = arg + '\\'
    print('Processing mode is', proc_mode)
    print('Workdir is', wdir)


# if there are dirs in a workdir, add them to the dirs list
def list_dirs(workdir):
    dirs_list = []
    for dirname in next(os.walk(workdir))[1]:
        # print(dirname);
        dirs_list.append(dirname)
    return dirs_list


# if there are html files with messages.*.html pattern in a workdir, add them to the files list
def list_files(workdir):
    files_list = []
    for filename in next(os.walk(workdir))[2]:
        if fname_regex.match(filename):
            # print(filename)
            files_list.append(filename)
    return files_list


# convert ts from string to timestamp format
def convert_ts(ts):
    print(ts)
    return ts


# sets ts on a file
def set_ts_on_file(file, ts):
    print("NYI")


# export dicts (images, voices_msgs, videos, files) to the *.csv files in a workdir
def export_dicts(workdir):
    print("NYI")


# import dicts (images, voices_msgs, videos, files) from the *.csv files in a workdir
def import_dicts(workdir):
    print("NYI")


# mk subdirs to save downloaded files
def mkdirs(workdir):
    # print(workdir);
    if not os.path.exists(workdir + '\\dl'):
        os.makedirs(workdir + '\\dl')
    if not os.path.exists(workdir + '\\dl' + '\\images'):
        os.makedirs(workdir + '\\dl' + '\\images')
    if not os.path.exists(workdir + '\\dl' + '\\voice_msgs'):
        os.makedirs(workdir + '\\dl' + '\\voice_msgs')
    if not os.path.exists(workdir + '\\dl' + '\\files'):
        os.makedirs(workdir + '\\dl' + '\\files')


# process files from dict (download to dir and set ts)
def process_files(workdir, file_dict):
    print("NYI")


# process all dicts with files
def process_files_from_dir(workdir, mode):
    print("NYI")


# parse messages file data and fill it to dicts
def parse_msg_file(message_file):
    img_id = 0
    ts = ""
    ts_line = ""
    msg_header = ""
    attach_desc = ""
    attach_url = ""
    print("Parsing file " + message_file)

    file = open(message_file, 'r')
    parser = BeautifulSoup(file, features="html.parser")
    items = parser.body.find('div', attrs={'class': 'wrap'}).findChild(attrs={'class': 'wrap_page_content'}).children

    for child in items:
        attach_desc = child.findNext('div', attrs={'class': 'item'})
        if attach_desc is not None:
            attach_desc = attach_desc.findChildren(attrs={'class': 'attachment__description'})
        else:
            break

        for attachment in attach_desc:
            desc = attachment.find_next('div', attrs={'class': 'attachment__description'})
            if desc is not None:
                match desc.text:
                    case 'Photo':
                        img_id += 1
                        attach_url = child.find_next('div', attrs={'class': 'item'}).findChild(attrs={'class': 'attachment__link'}).text
                        print('Found attachment of type "Photo", with URL', attach_url)
                    case 'Video':
                        print('Found attachment of type "Video"')
                    case 'File':
                        attach_url = child.find_next('div', attrs={'class': 'item'}).findChild(attrs={'class': 'attachment__link'}).text
                        print('Found attachment of type "File", with URL', attach_url)
                    case 'Message deleted':
                        continue
                    case 'Audio file':
                        continue
                    case 'Wall post':
                        continue
                    case 'Sticker':
                        continue
                    case 'Link':
                        continue
                    case _:
                        print('Found attachment of type "Unknown"')

#msg_header = parser.body.find('div', attrs={'class': 'item'}).findChild(attrs={'class': 'message__header'}).text


# parse all files in a directory
def parse_directory(workdir, mode):
    filenames = list_files(workdir)
    filenames_len = len(filenames)
    filenames_cnt = 0

    print("Parsing directory " + workdir)

    while (filenames_len - filenames_cnt) >= 1:
        parse_msg_file(workdir + '\\' + filenames[filenames_cnt])
        filenames_cnt = filenames_cnt + 1

    print("Finished parsing directory " + workdir)


def main(argv):
    get_args(argv)

    # parse_msg_file('C:\\Data\\media\\vk_messages_photo_downloader\\messages\\2000000005\\messages1650.html')

    dirnames = list_dirs(wdir)
    dirnames_len = len(dirnames)
    dirnames_cnt = 0
    # print(dirnames);

    while (dirnames_len - dirnames_cnt) >= 1:
        parse_directory(wdir + dirnames[dirnames_cnt], proc_mode)
        mkdirs(wdir + dirnames[dirnames_cnt])
        # if (proc_mode == 2):
            # process_files_from_dir(wdir + dirnames[dirnames_cnt], proc_mode)
        dirnames_cnt = dirnames_cnt + 1

#    if (proc_mode == 1):
#        dirnames_cnt = 0
#        while (dirnames_len - dirnames_cnt) > 1:
#            import_dicts(dirs[dirnames_cnt])
#            process_files_from_dir(dirs[dirnames_cnt])
#            dirnames_cnt = dirnames_cnt + 1


if __name__ == "__main__":
    main(sys.argv[1:])
