#!/usr/bin/python -tt

'''
Script should be create a follow structure:
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
->[unknown] (should be sorted by extension and moved to the different dirs)
'''

import os
import sys
import time
import shutil
import zipfile
import platform
import traceback

from datetime import datetime
from time import strftime

import appdirs
import requests

IMAGE_EXTS = ['image', '.jpg', '.jpeg', '.jpe', '.jp2', '.bmp', '.bmp2', '.bmp3', '.gif', '.png', '.png8', '.png24', 
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

SECONDS_IN_DAY = 24 * 60 * 60
SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_MINUTE = 60
TIME_UNITS = [('d', SECONDS_IN_DAY), ('h', SECONDS_IN_HOUR), ('min', SECONDS_IN_MINUTE), ('sec', 1)]

ENCODED_API_BASE_URL = 'aHR0cHM6Ly9hcGkubWFpbGd1bi5uZXQvdjMvc2FuZGJveDk0OGJjMWJkNzQ5MjRkMjU5MGFiNzFlYzI5MTYzNTM5Lm1haW\
  xndW4ub3JnL21lc3NhZ2Vz'
ENCODED_SENDER_EMAIL = 'ZmZjbGVhbmVyIDxtYWlsZ3VuQHNhbmRib3g5NDhiYzFiZDc0OTI0ZDI1OTBhYjcxZWMyOTE2MzUzOS5tYWlsZ3VuLm9yZz\
  4='
ENCODED_API_KEY = 'a2V5LTM0M2Y1MGYxZjAzOTNiOGUyYTA1NDAyMGQxZmIyNjI1'
ENCODED_SUPPORT_EMAIL = 'aHJybXNuQHlhbmRleC5ydQ=='
ENCODING_SCHEME = 'base64'


def extensions_types():
  exts_types = []
  exts_types.append(IMAGE_EXTS)
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


def extension_to_filetype(exts_types):
  ext_to_filetype = {}
  for exts_type in exts_types:
    ftype = exts_type.pop(0)
    for ext in exts_type:
      ext_to_filetype[ext] = ftype
  return ext_to_filetype


# make an unknown_exts a set?
def filetype(filepath, ext_to_filetype, unknown_exts):
  ext = os.path.splitext(filepath)[1].lower()
  if ext in ext_to_filetype:
    return ext_to_filetype[ext]
  if not ext in unknown_exts:
    unknown_exts.append(ext)
  return 'unknown'


def full_destination(not_fulldest, filepath, filenames_storage):
  basename = os.path.basename(filepath)
  filename = basename

  if not basename in filenames_storage:
    filenames_storage[basename] = 0
  else:
    filenames_storage[basename] += 1
    filename, ext = os.path.splitext(basename)
    filename += '(' + str(filenames_storage[basename]) + ')' + ext

  fulldest = os.path.join(not_fulldest, filename)
  return fulldest


def cleanfile(filepath, todir, ftype, filenames_storage):
  destination = os.path.join(todir, ftype)
  ext = os.path.splitext(filepath)[1].lower()
  ext = ext.strip('.')
  if ext == '':
    ext = '[no_extension]'
  destination = os.path.join(destination, ext)

  try:
    if not os.path.exists(destination):
      os.makedirs(destination)
  except OSError:
    inform('Error when creating destination path to file: ' + filepath + '.')
    log(msg=traceback.format_exc())
    sys_exit(error='OSError', send_log=True)

  fulldest = full_destination(destination, filepath, filenames_storage)
  shutil.copy2(filepath, fulldest)


def inform(info):
  print info
  log(msg=info)  


total_files_number = 0
unknown_files_number = 0
progress = 0

def plungedir(path, todir, cleandir_files_number, ext_to_filetype, filenames_storage, unknown_exts):
  global total_files_number
  global unknown_files_number
  global progress

  for subpath in os.listdir(path):
    fullpath = os.path.join(path, subpath)
    if os.path.isdir(fullpath):
      plungedir(fullpath, todir, cleandir_files_number, ext_to_filetype, filenames_storage, unknown_exts)
    else:
      total_files_number += 1
      new_progress = int('{:.0f}'.format(total_files_number * 100.0 / cleandir_files_number))
      if progress != new_progress:
        progress = new_progress
        inform(str(progress) + '% complete')

      ftype = filetype(fullpath, ext_to_filetype, unknown_exts)
      if ftype == 'unknown':
        unknown_files_number += 1
      cleanfile(fullpath, todir, ftype, filenames_storage)


def split_seconds(seconds):
  seconds = int(seconds)
  if seconds == 0:
    return '0 sec'
  splitted_seconds = []
  for time_unit in TIME_UNITS:
    if seconds >= time_unit[1]:
      unit_value = seconds / time_unit[1]
      seconds %= time_unit[1]
      splitted_seconds.append(str(unit_value) + ' ' + time_unit[0])
  return ' '.join(splitted_seconds)


def logdir():
  appname = 'ffcleaner'
  appauthor = 'hrrmsn'
  logpath = appdirs.user_log_dir(appname, appauthor)
  try:
    if not os.path.exists(logpath):
      os.makedirs(logpath)
  except OSError:
    inform('Error when creating path to log file: ' + logpath + '.')
    log(msg=traceback.format_exc())
    sys_exit(1, error='OSError', send_log=True)
  return logpath

LOGFILE = os.path.join(logdir(), 'log.txt')


#act={'start', 'log', 'end'}
def log(act='log', msg=''):
  timestamp = '[' + datetime.now().strftime('%Y-%d-%m %H:%M:%S') + ']'
  if act == 'start':
    msg = timestamp + ' Start logging.'
  elif act == 'log':
    msg = timestamp + ' ' + msg
  elif act == 'end':
    msg = timestamp + ' End logging.\n'

  try:
    f = open(LOGFILE, 'a')
    f.write(msg + '\n')
  except IOError:
    print 'Error when writing to log file.'
    sys_exit(1, error='IOError (writing to log)', send_log=True)
  finally:
    f.close()


def remove_file(filepath, file_title):
  try:
    print 'Removing ' + file_title + '.'
    os.remove(filepath)
  except OSError as exception:
    print 'Error when removing ' + file_title + '. \nSending email with error.'
    errmsg = 'Error when removing ' + file_title + '. Full stack trace is below. \n' + traceback.format_exc()
    sendmail(ENCODED_SENDER_EMAIL.decode(ENCODING_SCHEME), ENCODED_SUPPORT_EMAIL.decode(ENCODING_SCHEME), 
      type(exception).__name__ + ' (removing file)', errmsg, [])
  else:
    print file_title[:1].upper() + file_title[1:] + ' was removed successfully.'


def sys_exit(code, error='', send_log=False):
  if send_log:
    inform('Creating archive with the log file.')
    log(act='end')
    archive_path = archive_file(LOGFILE)
    print 'Archive was created successfully. \nSending archive via email.'
    sendmail(ENCODED_SENDER_EMAIL.decode(ENCODING_SCHEME), ENCODED_SUPPORT_EMAIL.decode(ENCODING_SCHEME), error, 
      'Details are inside the log file.', [archive_path])

    remove_file(LOGFILE, 'log file')
    remove_file(archive_path, 'archive with log')
  else:
    log(act='end')
  sys.exit(code)


def check_arguments(args):
  if not args:
    inform('Usage: [--todir dir] dir.')
    inform('Usage: --logpath.')
    sys_exit(1)

  if len(args) == 1 and args[0].lower() == '--logpath':
    inform(LOGFILE)
    sys_exit(0)

  todir = ''
  if args[0].startswith('--'):
    if args[0].lower() != '--todir':
      inform('Error: unsupported option.')
      sys_exit(1)
    if len(args) == 1:
      inform('Error: must specify target dir.')
      sys_exit(1)
    todir = args[1]
    del args[:2]

  if not args:
    inform('Error: must specify dir to clean.')
    sys_exit(1)
  elif len(args) > 1:
    if '--todir' in ''.join(args):
      inform('Error: todir option must be the first.')
      sys_exit(1)
    inform('Error: must specify only one dir to clean.')
    sys_exit(1)
  
  cleandir = args[0]
  return todir, cleandir


def overwrite(path):
  answer = raw_input('Dir to output already exists. Do you want to overwrite it? (y/n) ')
  answer = answer.lower()
  log(msg='Dir to output already exists. Do you want to overwrite it? (y/n) ' + answer)
  if answer in ['y', 'yes']:
    inform('Removing: ' + path + '.')
    try:
      shutil.rmtree(path)
    except OSError:
      inform('Error when removing directory (' + path + '): \n' + traceback.format_exc())
      sys_exit(1, error='OSError', send_log=True)
    else:
      inform('Removed successfully.')
  elif answer in ['n', 'no']:
    path = raw_input('Enter new dir to output: ')
    log(msg='Enter new dir to output: ' + path + '.')
  else:
    inform('Error: incorrect answer was typed.')
    sys_exit(1)
  return path


def check_input(todir, cleandir):
  if todir == cleandir:
    inform('Error: dir to clean and dir to output should be different.')
    sys_exit(1)

  if not os.path.exists(cleandir):
    inform('Error: dir to clean doesn\'t exist.')
    sys_exit(1)

  files_number_in_subfolders = [len(filenames) for dirpath, dirnames, filenames in os.walk(cleandir)]
  cleandir_files_number = sum(files_number_in_subfolders)
  if cleandir_files_number == 0:
    inform('Error: dir to clean is empty or doesn\'t contain any files.')
    sys_exit(1)

  while os.path.exists(todir) and os.listdir(todir) != []:
    todir = overwrite(todir)
  return todir, cleandir_files_number


def archive_file(filepath):
  basename = os.path.basename(filepath)
  basename_ext_cutted = os.path.splitext(basename)[0]
  archive_name = 'zipped_' + basename_ext_cutted + '.zip'

  basedir = os.path.dirname(filepath)
  archive_fullname = os.path.join(basedir, archive_name)

  try:
    zfile = zipfile.ZipFile(archive_fullname, mode='w')
    zfile.write(filepath, compress_type=zipfile.ZIP_DEFLATED)
  except (RuntimeError, IOError) as exception:
    print 'Error when processing zip file. \nSending email without attachments.'
    errmsg = 'Error when processing zip file. Full stack trace is below. \n' + traceback.format_exc()
    sendmail(ENCODED_SENDER_EMAIL.decode(ENCODING_SCHEME), ENCODED_SUPPORT_EMAIL.decode(ENCODING_SCHEME), 
      type(exception).__name__ + ' (processing zip archive)', errmsg, [])
    sys.exit(1)
  finally:
    zfile.close()
  return archive_fullname


def system_name():
  if sys.platform.startswith('linux'):
    return 'Linux'
  elif sys.platform.startswith('win'):
    return 'Windows'
  elif sys.platform.startswith('darwin'):
    return 'Mac OS'
  return 'rare OS type'


def sendpost(mailfrom, mailto, subject, message, attachments):
  try:
    response = requests.post(
      ENCODED_API_BASE_URL.decode(ENCODING_SCHEME), 
      auth=('api', ENCODED_API_KEY.decode(ENCODING_SCHEME)), 
      files=attachments, 
      data={'from': mailfrom, 'to': [mailto], 'subject': subject, 'text': message})
    if response.status_code != requests.codes.ok:
      response.raise_for_status()
    print 'Email was sent successfully.'
  except requests.ConnectionError:
    print 'Warning: some problems with internet connection. Email wasn\'t sent.'
  except requests.code.HTTPError:
    print 'Failed to send email. (Status: ' + str(response.status_code) + ' ' + response.reason + '.)'
  finally:
    for attachment in attachments:
      attached_file = attachment[1]
      attached_file.close()


def sendmail(mailfrom, mailto, subject, message, attached_files):
  attachments = []
  for filepath in attached_files:
    try:
      fopen = open(filepath)
      attachments.append(('attachment', fopen))
    except IOError:
      print 'Error when preparing attachments for sending via email. \nSending email without attachments.'
      errmsg = 'Couldn\'t prepare attachments for sending via email. Full stack trace is below. \n'\
        + traceback.format_exc()
      sendpost(mailfrom, mailto, 'IOError (problems with attachments)', errmsg, [])
      sys.exit(1)
  sendpost(mailfrom, mailto, subject, message, attachments)


# TODO: delete log file after sending via email
def main():
  log(act='start')
  log(msg='OS is ' + system_name() + '.')
  log(msg='Platform info: ' + platform.platform() + '.')
  log(msg='Launch command: ' + ' '.join(sys.argv) + '.')

  todir, cleandir = check_arguments(sys.argv[1:])
    
  inform('Dir to output: ' + todir + '.')
  inform('Dir to clean: ' + cleandir + '.')

  todir, cleandir_files_number = check_input(todir, cleandir)
  exts_types = extensions_types()
  ext_to_filetype = extension_to_filetype(exts_types)

  inform('Started cleaning.')

  timestart = time.time()
  unknown_exts = []
  try:
    plungedir(cleandir, todir, cleandir_files_number, ext_to_filetype, {}, unknown_exts)
  except (OSError, IOError) as exception:
    inform('Error when cleaning directory (' + cleandir + '): \n' + traceback.format_exc())
    sys_exit(1, error=type(exception).__name__, send_log=True)

  inform('Processed files: ' + str(total_files_number) + '.')
  inform('Unknown files: ' + '{:.2f}%'.format(unknown_files_number / float(total_files_number) * 100) + '.')
  log(msg='List of unknown extensions: [\'' + '\', \''.join(unknown_exts) + '\'].')

  timedelta = '{:.0f}'.format(time.time() - timestart)
    
  inform('Cleaned in ' + split_seconds(timedelta) + '.')
  log(act='end')


if __name__ == '__main__':
  main()
