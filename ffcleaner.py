#!/usr/bin/python -tt

'''
Tool should be create a follow structure:
->[images]
->[code]
->[document]
->[ebooks]
->[video]
->[audio]
->[presentation]
->[system]
->[compressed]
->[executable]
->[disk_image]
->[spreadsheets]
->[font]
->[database]
->[settings]
->[backup]
->[cad]
->[partially_downloaded]
->[calendar]
->[installer]
->[torrent]
->[empty]
  ->[images]
  ->[code]
  ->[document]
  ...
  ->[torrent]
->[unknown] (should be sorted by extension and moved to the different dirs)
'''

import sys
import os
import shutil

IMAGES_EXTS = ['image', '.jpg', '.jpeg', '.jpe', '.jp2', '.bmp', '.bmp2', '.bmp3', '.gif', '.png', '.png8', '.png24', 
'.png32', '.tiff', '.tif', '.ptif', '.tiff64', '.psd', '.xcf', '.ico', '.icon', '.svg', '.svgz', '.msvgz', '.eps', 
'.eps2', '.eps3', '.epsf', '.ai', '.nef', '.cr2', '.crw', '.dcr', '.kdc', '.k25', '.x3f', '.arw', '.sr2', '.srf', 
'.mrw', '.erf', '.raf', '.pct', '.pict', '.dds', '.dng', '.pex', '.3fr', '.ppm', '.orf', '.pef', '.aai', '.exr', 
'.hdr', '.dcm', '.dicom', '.psb', '.pbm', '.jpf', '.iff', '.sct', '.tga', '.fit', '.fits', '.fts', '.mng', '.pgm', 
'.pnm', '.pam', '.ps', '.ps2', '.ps3', '.sgi', '.xpm', '.xbm', '.bitmap', '.xwd', '.pcx', '.pcc', '.cur']

CODE_EXTS = ['code', '.as', '.actionscript', '.sh', '.cf', '.cfm', '.cs', '.c', '.h', '.cc', '.cp', '.cpp', '.md', 
'.markdown', '.m', '.css', '.pas', '.diff', '.patch', '.erl', '.groovy', '.js', '.java', '.pl', '.perl', '.php', 
'.ps1', '.py', '.python', '.rb', '.ruby', '.scala', '.sql', '.vb', '.xhtml', '.xslt', '.htm', '.html', '.rss', '.atom', 
'.xml']

DOCUMENT_EXTS = ['document', '.pages', '.docx', '.doc', '.rtf', '.odt', '.wpd', '.wps', '.jtd', '.jtt', '.pdf', 
'.epdf', '.tex', '.mml', '.uof', '.uot', '.sdw', '.sxw', '.ps', '.ps2', '.ps3', '.djvu', '.txt', '.text']

EBOOKS_EXTS = ['ebook', '.azw', '.azw4', '.chm', '.cbz', '.djvu', '.epub', '.fb2', '.htmlz', '.lit', '.lrf', '.lrs', 
'.mobi', '.pml', '.recipe', '.snb', '.tcr', '.cbr', '.prc', '.tpz', '.pmlz']

VIDEO_EXTS = ['video', '.mp4', '.mov', '.m4v', '.m2v', '.avi', '.wmv', '.rm', '.mpeg', '.mpg', '.ogv', '.3gp', '.3g2', 
'.vob', '.flv', '.webm', '.mkv']

AUDIO_EXTS = ['audio', '.mp3', '.mp2', '.wma', '.wav', '.ogg', '.aac', '.flac', '.au', '.aif', '.aiff', '.gsm', '.ra', 
'.mid', '.amr', '.m4a']

PRESENTATION_EXTS = ['presentation', '.odp', '.otp', '.pot', '.pps', '.ppsx', '.ppt', '.pptx', '.sdd', '.sti', '.sx', 
'.uop', '.sxi']

SYSTEM_EXTS = ['system', '.cab', '.cpl', '.cur', '.deskthemepack', '.dll', '.dmp', '.drv', '.icns', '.ico', '.lnk', 
'.sys']

COMPRESSED_EXTS = ['compressed', '.7z', '.cbr', '.deb', '.gz', '.pkg', '.rar', '.rpm', '.sitx', '.zip', '.zipx']
EXECUTABLE_EXTS = ['executable', '.apk', '.app', '.bat', '.cgi', '.com', '.exe', '.gadget', '.jar', '.wsf']
DISK_IMAGE_EXTS = ['disk_image', '.bin', '.cue', '.dmg', '.iso', '.mdf', '.toast', '.vcd']
SPREADSHEETS_EXTS = ['spreadsheet', '.xls', '.xlsx', '.xlsb', '.xlsm', '.ods', '.csv']
FONT_EXTS = ['font', '.ttf', '.otf', '.woff', '.ttc', '.dfont', '.sfd']
DATABASE_EXTS = ['database', '.accdb', '.db', '.dbf', '.mdb', '.pdb']
SETTINGS_EXTS = ['settings', '.cfg', '.ini', '.prf']
BACKUP_EXTS = ['backup', '.bak', '.tmp']
CAD_EXTS = ['cad', '.dwg', '.dxf']
PLUGIN_EXTS = ['plugin', '.crx', '.plugin']
PARTIALLY_DOWNLOADED_EXTS = ['partially_downloaded', '.crdownload', '.part']
CALENDAR_EXTS = ['calendar', '.ics']
INSTALLER_EXTS = ['installer', '.msi']
TORRENT_EXTS = ['torrent', '.torrent']


def extensions_types():
  exts_types = []
  exts_types.append(IMAGES_EXTS)
  exts_types.append(CODE_EXTS)
  exts_types.append(DOCUMENT_EXTS)
  exts_types.append(EBOOKS_EXTS)
  exts_types.append(VIDEO_EXTS)
  exts_types.append(AUDIO_EXTS)
  exts_types.append(PRESENTATION_EXTS)
  exts_types.append(SYSTEM_EXTS)
  exts_types.append(COMPRESSED_EXTS)
  exts_types.append(EXECUTABLE_EXTS)
  exts_types.append(DISK_IMAGE_EXTS)
  exts_types.append(SPREADSHEETS_EXTS)
  exts_types.append(FONT_EXTS)
  exts_types.append(DATABASE_EXTS)
  exts_types.append(SETTINGS_EXTS)
  exts_types.append(BACKUP_EXTS)
  exts_types.append(CAD_EXTS)
  exts_types.append(PLUGIN_EXTS)
  exts_types.append(PARTIALLY_DOWNLOADED_EXTS)
  exts_types.append(CALENDAR_EXTS)
  exts_types.append(INSTALLER_EXTS)
  exts_types.append(TORRENT_EXTS)
  return exts_types


def extension_to_filetype():
  exts_types = extensions_types()
  ext_to_filetype = {}
  for exts_type in exts_types:
    filetype = exts_type[0]
    for ext in exts_type[1:]:
      ext_to_filetype[ext] = filetype
  return ext_to_filetype


def filetype(filename):
  ext = os.path.splitext(filename)[1].lower()
  ext_to_filetype = extension_to_filetype()
  if ext in ext_to_filetype:
    return ext_to_filetype[ext]
  elif os.stat(filename).st_size == 0:
    return 'empty'
  return 'unknown'


total_files_number = 0
unknown_files_number = 0

def listdir(path, todir):
  global total_files_number
  global unknown_files_number

  for subpath in os.listdir(path):
    absolute_path = os.path.join(path, subpath)
    if os.path.isdir(absolute_path):
      listdir(absolute_path, todir)
    else:
      total_files_number += 1
      if filetype(absolute_path) == 'unknown':
        unknown_files_number += 1
      print absolute_path + ' -> ' + filetype(absolute_path)
      cleanfile(absolute_path, todir)


def cleanfile(filepath, todir):
  destination = os.path.join(todir, filetype(filepath))
  if not os.path.exists(destination):
    os.makedirs(destination)
  # shutil.copy2(filepath, destination)
  shutil.move(filepath, destination)


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
  
  cleandir = args[0]

  print 'todir=' + todir
  print 'cleandir=' + cleandir + '\n'

  listdir(cleandir, todir)

  print '\n'
  print 'total files: ' + str(total_files_number)
  print 'unknown files: ' + '{:.2f}%'.format(unknown_files_number / float(total_files_number) * 100)  


if __name__ == '__main__':
  main()
