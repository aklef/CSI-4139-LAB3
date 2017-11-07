import os, mmap
from mmap import mmap

print("System is starting...\n")

VDfile = open('Signature.DAT', "r+b")
VirusDefinitions = VDfile.readlines()
VDfile.close()

print("Virus definitions loaded!\n")

def scan(file):
   print(file)
   infections = 0
   for i,vd in enumerate(VirusDefinitions):
      with open(cwdf, "r+b") as candidate:
         mm = mmap(candidate.fileno(), 0)
         offset = mm.find(vd)
         if offset>=0:
            infections += 1
            neutralize(file, offset)
         mm.close()
   return infections

def quarantine(virus, vd):
   print('')
   os.rename(virus, )

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

for cf in os.listdir(directory):
   cwdf = directory + '/' + cf
   infections = scan(cwdf)
   if infections>0:
      # quarantine(cf)
      print('>Found {} infections! File quarantined'.format(infections))
   else:
      print('>The file is clean!')
