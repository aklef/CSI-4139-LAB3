import os, mmap
from mmap import mmap
import re

print("System is starting...\n")

VDfile = open('Signature.DAT', "r+b")
VirusDefinitions = VDfile.readlines()
VDfile.close()

print("Virus definitions loaded!\n")

def scan(file):
    # print(file)
    infections = 0
    for i,vd in enumerate(VirusDefinitions):
        # print (vd)
        vd = vd[0:-1]
        with open(cwdf, "r+b") as candidate:
            # print ("file: {}".format(candidate.fileno()))
            mm = mmap(candidate.fileno(), 0)
            # print("Candidate: {}".format(candidate))
            # print ("vd: {}".format(vd))
            # print (mm.readline())
            offset = mm.find(vd)
            # print ("offset {}".format(offset))
            if offset>=0:
                infections += 1
                neutralize(file, offset)
                mm.close()

    if infections > 0:
        quarantine(file)
    return infections

def quarantine(virus):
    folder_name = 'quarantine'
    file_name = get_file_name(virus)
    destination = '{}/{}'.format(folder_name, file_name)
    if os.path.isdir(folder_name):
        move_file(virus, destination)
    else:
        os.makedirs(folder_name)
        move_file(virus, destination)


def move_file(cur_dest, new_dest):
    print ('Quarantining {}'.format(cur_dest))
    os.rename(cur_dest, new_dest)


def get_file_name(file):
    return re.search('\/.+\..+', file).group(0)[1:]

def neutralize(virus, offset):
    X = bytes('x'*8, 'utf-8')
    overwrite(virus, X, offset)

def overwrite(filename, s, pos):
    f = open(filename, 'r+')
    m = mmap(f.fileno(), os.path.getsize(filename))
    origSize = m.size()

    m[pos:(pos+len(s))] = s
    m.close()
    f.close()

directory = 'Programs'

# print (os.listdir(directory))
ESC_CHAR = '\033'
COLOR_GREEN = '32m'
COLOR_RED = '5;31m'
RESET = '[0m'
for cf in os.listdir(directory):
    cwdf = directory + '/' + cf
    print ("\n=================================")
    print ("Scanning {}".format(cf))
    print ("=================================")
    infections = scan(cwdf)
    # print ( infections )
    if infections>0:
        # quarantine(cf)
        print('{} {}[{}Found {} infections in {}! File quarantined{}{}'.format(
            '☠️',
            ESC_CHAR,
            COLOR_RED,
            infections,
            cf,
            ESC_CHAR,
            RESET
        ))
    else:
        print('{}[{}{} is clean!{}{}'.format(
            ESC_CHAR,
            COLOR_GREEN,
            cf,
            ESC_CHAR,
            RESET
        ))
