#!/usr/bin/python -tt

'''
Tool should be create a follow structure:
->images
->audio
->video
->font
->document
->ebooks
->presentation
->code
->spreadsheets
->cad
->[empty]
  ->[images]
  ->[audio]
  ...
  ->[cad]
->[unknown]
'''

import sys
import os

IMAGES_EXTS = ['.jpg', '.jpeg', '.jpe', '.jp2', '.bmp', '.bmp2', '.bmp3', '.gif', '.png', '.png8', '.png24', '.png32', 
'.tiff', '.tif', '.ptif', '.tiff64', '.psd', '.xcf', '.ico', '.icon', '.svg', '.svgz', '.msvgz', '.eps', '.eps2', 
'.eps3', '.epsf', '.ai', '.nef', '.cr2', '.crw', '.dcr', '.kdc', '.k25', '.x3f', '.arw', '.sr2', '.srf', '.mrw', 
'.erf', '.raf', '.pct', '.pict', '.dds', '.dng', '.pex', '.3fr', '.ppm', '.orf', '.pef', '.aai', '.exr', '.hdr', 
'.dcm', '.dicom', '.psb', '.pbm', '.jpf', '.iff', '.sct', '.tga', '.fit', '.fits', '.fts', '.mng', '.pgm', '.pnm', 
'.pam', '.ps', '.ps2', '.ps3', '.sgi', '.xpm', '.xbm', '.bitmap', '.xwd', '.pcx', '.pcc', '.cur']

CODE_EXTS = ['.as', '.actionscript', '.sh', '.cf', '.cfm', '.cs', '.c', '.h', '.cc', '.cp', '.cpp', '.md', '.markdown', 
'.m', '.css', '.pas', '.diff', '.patch', '.erl', '.groovy', '.js', '.java', '.pl', '.perl', '.php', '.ps1', '.py', 
'.python', '.rb', '.ruby', '.scala', '.sql', '.vb', '.xhtml', '.xslt', '.htm', '.html', '.rss', '.atom', '.xml']

DOCUMENT_EXTS = ['.pages', '.docx', '.doc', '.rtf', '.odt', '.wpd', '.wps', '.jtd', '.jtt', '.pdf', '.epdf', '.tex', 
'.mml', '.uof', '.uot', '.sdw', '.sxw', '.ps', '.ps2', '.ps3', '.djvu', '.txt', '.text']

EBOOKS_EXTS = ['.azw', '.azw4', '.chm', '.cbz', '.djvu', '.epub', '.fb2', '.htmlz', '.lit', '.lrf', '.lrs', '.mobi', 
'.pml', '.recipe', '.snb', '.tcr', '.cbr', '.prc', '.tpz', '.pmlz']

VIDEO_EXTS = ['.mp4', '.mov', '.m4v', '.m2v', '.avi', '.wmv', '.rm', '.mpeg', '.mpg', '.ogv', '.3gp', '.3g2', '.vob', 
'.flv', '.webm', '.mkv']

AUDIO_EXTS = ['.mp3', '.mp2', '.wma', '.wav', '.ogg', '.aac', '.flac', '.au', '.aif', '.aiff', '.gsm', '.ra', '.mid', 
'.amr', '.m4a']

PRESENTATION_EXTS = ['.odp', '.otp', '.pot', '.pps', '.ppsx', '.ppt', '.pptx', '.sdd', '.sti', '.sx', '.uop', '.sxi']
SYSTEM_EXTS = ['.cab', '.cpl', '.cur', '.deskthemepack', '.dll', '.dmp', '.drv', '.icns', '.ico', '.lnk', '.sys']
COMPRESSED_EXTS = ['.7z', '.cbr', '.deb', '.gz', '.pkg', '.rar', '.rpm', '.sitx', '.zip', '.zipx']
EXECUTABLE_EXTS = ['.apk', '.app', '.bat', '.cgi', '.com', '.exe', '.gadget', '.jar', '.wsf']
DISK_IMAGE_EXTS = ['.bin', '.cue', '.dmg', '.iso', '.mdf', '.toast', '.vcd']
SPREADSHEETS_EXTS = ['.xls', '.xlsx', '.xlsb', '.xlsm', '.ods', '.csv']
FONT_EXTS = ['.ttf', '.otf', '.woff', '.ttc', '.dfont', '.sfd']
DATABASE_EXTS = ['.accdb', '.db', '.dbf', '.mdb', '.pdb']
SETTINGS_EXTS = ['.cfg', '.ini', '.prf']
BACKUP_EXTS = ['.bak', '.tmp']
CAD_EXTS = ['.dwg', '.dxf']
PLUGIN_EXTS = ['.crx', '.plugin']
PARTIALLY_DOWNLOADED_EXTS = ['.crdownload', '.part']
CALENDAR_EXTS = ['.ics']
INSTALLER_EXTS = ['.msi']
TORRENT_EXTS = ['.torrent']


def filetype(filename):
  ext = os.path.splitext(filename)[1].lower()
  if ext in IMAGES_EXTS:
    return 'image'
  elif ext in CODE_EXTS:
    return 'code'
  elif ext in DOCUMENT_EXTS:
    return 'document'
  elif ext in EBOOKS_EXTS:
    return 'ebook'
  elif ext in VIDEO_EXTS:
    return 'video'
  elif ext in AUDIO_EXTS:
    return 'audio'
  elif ext in PRESENTATION_EXTS:
    return 'presentation'
  elif ext in SYSTEM_EXTS:
    return 'system'
  elif ext in COMPRESSED_EXTS:
    return 'compressed'
  elif ext in EXECUTABLE_EXTS:
    return 'executable'
  elif ext in DISK_IMAGE_EXTS:
    return 'disk_image'
  elif ext in SPREADSHEETS_EXTS:
    return 'spreadsheet'
  elif ext in FONT_EXTS:
    return 'font'
  elif ext in DATABASE_EXTS:
    return 'database'
  elif ext in SETTINGS_EXTS:
    return 'settings'
  elif ext in BACKUP_EXTS:
    return 'backup'
  elif ext in CAD_EXTS:
    return 'cad'
  elif ext in PLUGIN_EXTS:
    return 'plugin'
  elif ext in PARTIALLY_DOWNLOADED_EXTS:
    return 'partially_downloaded'
  elif ext in CALENDAR_EXTS:
    return 'calendar'
  elif ext in INSTALLER_EXTS:
    return 'installer'
  elif ext in TORRENT_EXTS:
    return 'torrent'
  elif os.stat(filename).st_size == 0:
    return 'empty'
  return 'unknown'


total_files_number = 0
unknown_files_number = 0

def listdir(path):
  global total_files_number
  global unknown_files_number

  for subpath in os.listdir(path):
    absolute_path = os.path.join(path, subpath)
    if os.path.isdir(absolute_path):
      listdir(absolute_path)
    else:
      total_files_number += 1
      if filetype(absolute_path) == 'unknown':
        unknown_files_number += 1
      print absolute_path + ' -> ' + filetype(absolute_path)


def main():
  args = sys.argv[1:]
  if not args:
    print 'usage: [--todir dir] dir'
    sys.exit(1)

  todir = ''
  if args[0].startswith('--'):
    if args[0] != '--todir':
      print 'error: unsupported option'
      sys.exit(1)
    if len(args) == 1:
      print 'error: must specify target dir'
      sys.exit(1)
    todir = args[1]
    del args[:2]

  if not args:
    print 'error: must specify dir to clean'
    sys.exit(1)
  elif len(args) > 1:
    print 'args: ' + str(args)
    if '--todir' in ''.join(args):
      print 'error: todir option must be the first'
      sys.exit(1)
    print 'error: must specify only one dir to clean'
    sys.exit(1)
  
  dir_to_clean = args[0]

  print 'todir=' + todir
  print 'dir=' + dir_to_clean + '\n'

  listdir(dir_to_clean)

  print '\n'
  print 'total files: ' + str(total_files_number)
  print 'unknown files: ' + '{:.2f}%'.format(unknown_files_number / float(total_files_number) * 100)


if __name__ == '__main__':
  main()
