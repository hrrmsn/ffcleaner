#!/usr/bin/env python

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
->[unknown] (should be sorted by extension and be moved to the different dirs)
'''

import os
import sys
import time
import stat
import ctypes
import shutil
import zipfile
import platform
import traceback

from datetime import datetime

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

DECODED_SENDER_EMAIL = ENCODED_SENDER_EMAIL.decode(ENCODING_SCHEME)
DECODED_SUPPORT_EMAIL = ENCODED_SUPPORT_EMAIL.decode(ENCODING_SCHEME)

SYSPRINT_NUMBER_OF_SPACES = 100
SYSPRINT_MAX_LENGTH_OF_FILENAME = 30

COPYBYTES_DEFAULT_BUFFER_SIZE = 1000000
COPYBYTES_MIN_FILE_SIZE = 1000000

BYTES_IN_TERABYTE = {'metric': 1000**4, 'binary': 1024**4}
BYTES_IN_GIGABYTE = {'metric': 1000**3, 'binary': 1024**3}
BYTES_IN_MEGABYTE = {'metric': 1000**2, 'binary': 1024**2}
BYTES_IN_KILOBYTE = {'metric': 1000, 'binary': 1024}

BYTE_UNITS = [(BYTES_IN_TERABYTE, 'TB'), (BYTES_IN_GIGABYTE, 'GB'), (BYTES_IN_MEGABYTE, 'MB'), 
  (BYTES_IN_KILOBYTE, 'kB')]


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


def filetype(filepath, ext_to_filetype, unknown_exts):
  ext = os.path.splitext(filepath)[1].lower()
  if ext in ext_to_filetype:
    return ext_to_filetype[ext]
  if ext != '':
    unknown_exts.add(ext)
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


def sysprint(text=''):
  sys.stdout.write(' ' * SYSPRINT_NUMBER_OF_SPACES + '\r')
  sys.stdout.write(text)
  sys.stdout.flush()


def cutstr(mystr):
  if len(mystr) > SYSPRINT_MAX_LENGTH_OF_FILENAME:
    return '...' + mystr[-SYSPRINT_MAX_LENGTH_OF_FILENAME:]
  return mystr


'''
TODO: do not use global variables!
I should pass variables as function parameters whenever it's possible.
'''
def update_progress(cleandir_size, filepath, processed_files_size):
  global progress

  new_progress = int('{:.0f}'.format(processed_files_size / float(cleandir_size) * 100))
  if progress != new_progress:
    progress = new_progress
    cutted_basename = cutstr(os.path.basename(filepath))
    log(msg='{:d}% complete (copying \'{}\')'.format(progress, cutted_basename))
    sysprint('{:d}% complete (copying \'{}\')\r'.format(progress, cutted_basename))
  

def copybytes(copyfrom, copyto, cleandir_size, copybytes_buffer_size):
  global processed_files_size

  copyfrom_size = os.path.getsize(copyfrom)
  try:
    with open(copyfrom, 'rb') as src:
      with open(copyto, 'wb') as dst:
        datablock = src.read(copybytes_buffer_size)
        while datablock:
          dst.write(datablock)

          if copyfrom_size > copybytes_buffer_size:
            processed_files_size += copybytes_buffer_size
            copyfrom_size -= copybytes_buffer_size
          else:
            processed_files_size += copyfrom_size
            copyfrom_size = 0

          update_progress(cleandir_size, copyfrom, processed_files_size)
          datablock = src.read(copybytes_buffer_size)
    shutil.copystat(copyfrom, copyto)
  except IOError:
    inform('Error when copying file: \'' + copyfrom + '\'.')
    log(msg=traceback.format_exc())
    sys_exit(1, error='IOError', send_log=True)


def cleanfile(filepath, todir, ftype, filenames_storage, cleandir_size, copybytes_buffer_size):
  global processed_files_size

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
    inform('Error when creating destination path to file: \'' + filepath + '\'.')
    log(msg='The file path before cleaning: \'' + filepath + '\'.')
    log(msg='The expected file path after cleaning: \'' + destination + '\'.')
    log(msg=traceback.format_exc())
    sys_exit(1, error='OSError', send_log=True)

  fulldest = full_destination(destination, filepath, filenames_storage)
  
  if os.path.getsize(filepath) > COPYBYTES_MIN_FILE_SIZE:
    copybytes(filepath, fulldest, cleandir_size, copybytes_buffer_size)
  else:
    shutil.copy2(filepath, fulldest)
    processed_files_size += os.path.getsize(filepath)
    update_progress(cleandir_size, filepath, processed_files_size)
  

def inform(info):
  print info
  log(msg=info)  


processed_files_number = 0
unknown_files_number = 0
processed_files_size = 0
progress = 0

def plungedir(path, todir, cleandir_files_number, cleandir_size, ext_to_filetype, filenames_storage, unknown_exts, 
    copybytes_buffer_size):
  global processed_files_number
  global unknown_files_number

  for subpath in os.listdir(path):
    fullpath = os.path.join(path, subpath)
    if os.path.isdir(fullpath):
      plungedir(fullpath, todir, cleandir_files_number, cleandir_size, ext_to_filetype, filenames_storage, unknown_exts,
        copybytes_buffer_size)
    else:
      ftype = filetype(fullpath, ext_to_filetype, unknown_exts)

      cleanfile(fullpath, todir, ftype, filenames_storage, cleandir_size, copybytes_buffer_size)

      processed_files_number += 1
      if ftype == 'unknown':
        unknown_files_number += 1
      

def logdir():
  appname = 'ffcleaner'
  appauthor = 'hrrmsn'
  logpath = appdirs.user_log_dir(appname, appauthor)
  try:
    if not os.path.exists(logpath):
      os.makedirs(logpath)
  except OSError:
    inform('Error when creating path to log file: \'' + logpath + '\'.')
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
    with open(LOGFILE, 'a') as fopen:
      fopen.write(msg + '\n')
  except IOError:
    print 'Error when writing to log file. \nSending email with error...'
    errmsg = 'Error when writing to log file. Full stack trace is below. \n' + traceback.format_exc()
    sendmail(DECODED_SENDER_EMAIL, DECODED_SUPPORT_EMAIL, 'IOError (writing to log)', errmsg, [])
    sys.exit(1)


def remove_file(filepath, file_title):
  try:
    print 'Removing ' + file_title + '...'
    os.remove(filepath)
  except OSError:
    print 'Error when removing ' + file_title + '. \nSending email with error...'
    errmsg = 'Error when removing'  + file_title + '. Full stack trace is below. \n' + traceback.format_exc()
    sendmail(DECODED_SENDER_EMAIL, DECODED_SUPPORT_EMAIL, 'OSError (removing file)', errmsg, [])
  else:
    print 'Ok.'


def archive_file(filepath):
  basename = os.path.basename(filepath)
  basename_ext_cutted = os.path.splitext(basename)[0]
  archive_name = 'zipped_' + basename_ext_cutted + '.zip'

  basedir = os.path.dirname(filepath)
  archive_fullname = os.path.join(basedir, archive_name)

  try:
    with zipfile.ZipFile(archive_fullname, mode='w') as zfile:
      zfile.write(filepath, compress_type=zipfile.ZIP_DEFLATED)
  except (RuntimeError, IOError) as exception:
    print 'Error when processing zip file. \nSending email without attachments...'
    errmsg = 'Error when processing zip file. Full stack trace is below. \n' + traceback.format_exc()
    sendmail(DECODED_SENDER_EMAIL, DECODED_SUPPORT_EMAIL, type(exception).__name__ + ' (processing zip archive)', 
      errmsg, [])
    sys.exit(1)
  return archive_fullname    


def sys_exit(code, error='', send_log=False):
  if send_log:
    inform('Creating archive with the log file...')
    log(act='end')

    archive_path = archive_file(LOGFILE)
    print 'Ok. \nSending archive via email...'
    
    errmsg = 'Details are inside the log file.'
    if sendmail(DECODED_SENDER_EMAIL, DECODED_SUPPORT_EMAIL, error, errmsg, [archive_path]):
      remove_file(LOGFILE, 'log file')
      remove_file(archive_path, 'archive with log')
  else:
    log(act='end')
  sys.exit(code)


def sendpost(mailfrom, mailto, subject, message, attachments):
  try:
    response = requests.post(
      ENCODED_API_BASE_URL.decode(ENCODING_SCHEME), 
      auth=('api', ENCODED_API_KEY.decode(ENCODING_SCHEME)), 
      files=attachments, 
      data={'from': mailfrom, 'to': [mailto], 'subject': subject, 'text': message})
    if response.status_code != requests.codes.ok:
      response.raise_for_status()
  except requests.ConnectionError:
    print 'Warning: some problems with internet connection. Email wasn\'t sent.'
    return False
  except requests.code.HTTPError:
    print 'Failed to send email. (Status: ' + str(response.status_code) + ' ' + response.reason + '.)'
    return False
  else:
    print 'Ok.'
    return True
  finally:
    for attachment in attachments:
      attached_file = attachment[1]
      attached_file.close()


def sendmail(mailfrom, mailto, subject, message, attached_files):
  attachments = []
  for filepath in attached_files:
    try:
      fopen = open(filepath, 'rb')
      attachments.append(('attachment', fopen))
    except IOError:
      print 'Error when preparing attachments for sending via email. \nSending email without attachments...'
      errmsg = 'Couldn\'t prepare attachments for sending via email. Full stack trace is below. \n'
      errmsg += traceback.format_exc()
      sendpost(mailfrom, mailto, 'IOError (problems with attachments)', errmsg, [])
      sys.exit(1)
  return sendpost(mailfrom, mailto, subject, message, attachments)  


def check_arguments(args):
  if not args:
    inform('Usage: [--todir dir] dir.')
    inform('Usage: --logpath.')
    sys_exit(0)

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
  
  
def remove_readonly(func, path, exc_info):
  os.chmod(path, stat.S_IWRITE)
  func(path)


def overwrite(path):
  answer = raw_input('Dir to output already exists. Do you want to overwrite it? (y/n) ')
  answer = answer.lower()
  log(msg='Dir to output already exists. Do you want to overwrite it? (y/n) ' + answer)
  if answer in ['y', 'yes']:
    inform('Removing \'' + path + '\'...')
    try:
      shutil.rmtree(path, onerror=remove_readonly)
    except OSError:
      inform('Error when removing directory: \'' + path + '\'.')
      log(msg=traceback.format_exc())
      sys_exit(1, error='OSError', send_log=True)
    else:
      inform('Ok.')
  elif answer in ['n', 'no']:
    path = raw_input('Enter new dir to output: ')
    log(msg='Enter new dir to output: \'' + path + '\'.')
  else:
    inform('Error: incorrect answer was typed.')
    sys_exit(1)
  return path


def print_bytes(bytes):
  order = 'metric'
  if system_name() == 'Windows':
    order = 'binary'
  for unit_and_symbol in BYTE_UNITS:
    unit_symbol = unit_and_symbol[1]
    units_by_order = unit_and_symbol[0]
    bytes_in_unit = units_by_order[order]
    if bytes >= bytes_in_unit:
      return '{:.1f}'.format(bytes / float(bytes_in_unit)) + ' ' + unit_symbol
  return str(bytes) + ' bytes'


def dirsize(dirpath):
  total_size = 0
  for root, dirs, filenames in os.walk(dirpath):
    for filename in filenames:
      total_size += os.path.getsize(os.path.join(root, filename))
  return total_size


def check_input(todir, cleandir):
  if todir == cleandir:
    inform('Error: dir to clean and dir to output should be different.')
    sys_exit(1)

  if not os.path.exists(cleandir):
    inform('Error: dir to clean doesn\'t exist.')
    sys_exit(1)

  inform('Counting files to clean...')
  files_numbers_in_subfolders = [len(filenames) for dirpath, dirnames, filenames in os.walk(cleandir)]  
  cleandir_files_number = sum(files_numbers_in_subfolders)

  if cleandir_files_number == 0:
    inform('Error: dir to clean is empty or doesn\'t contain any files.')
    sys_exit(1)

  cleandir_size = dirsize(cleandir)

  inform(str(cleandir_files_number) + ' files found. (' + print_bytes(cleandir_size) + ')')

  while os.path.exists(todir) and os.listdir(todir) != []:
    todir = overwrite(todir)
  return todir, cleandir_files_number, cleandir_size


def system_name():
  if sys.platform.startswith('linux'):
    return 'Linux'
  elif sys.platform.startswith('win'):
    return 'Windows'
  elif sys.platform.startswith('darwin'):
    return 'Mac OS'
  return 'rare OS type'
  
  
def check_unknown_files(unknown_files_number, processed_files_number, unknown_exts):
  if unknown_files_number == 0:
    inform('Unknown files are not found.')
  else:
    inform('Unknown files: ' + '{:.2f}%'.format(unknown_files_number / float(processed_files_number) * 100) + '.')
    if unknown_exts:
      log(msg='List of unknown extensions: [\'' + '\', \''.join(unknown_exts) + '\'].')
    else:
      log(msg='Unknown extensions are not found.')


def print_seconds(seconds):
  if seconds == 0:
    return '0 sec'
  splitted_seconds = []
  for time_unit in TIME_UNITS:
    if seconds >= time_unit[1]:
      unit_value = seconds / time_unit[1]
      seconds %= time_unit[1]
      splitted_seconds.append(str(unit_value) + ' ' + time_unit[0])
  return ' '.join(splitted_seconds)
  
  
def get_free_space(path):
  if system_name() == 'Windows':
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value
  st = os.statvfs(path)
  return st.f_bavail * st.f_frsize
  

def main():
  log(act='start')
  log(msg='OS is ' + system_name() + '.')
  log(msg='Platform info: ' + platform.platform() + '.')
  log(msg='Launch command: ' + ' '.join(sys.argv) + '.')

  copybytes_buffer_size = COPYBYTES_DEFAULT_BUFFER_SIZE
  if len(sys.argv) > 4:
    copybytes_buffer_size = int(sys.argv[4])
    del sys.argv[4]  

  todir, cleandir = check_arguments(sys.argv[1:])
    
  inform('Dir to output: \'' + todir + '\'.')
  inform('Dir to clean: \'' + cleandir + '\'.')

  todir, cleandir_files_number, cleandir_size = check_input(todir, cleandir)
  exts_types = extensions_types()
  ext_to_filetype = extension_to_filetype(exts_types)

  inform('Started cleaning. (b_size is ' + print_bytes(copybytes_buffer_size) + ')')

  unknown_exts = set()
  timestart = time.time()
  try:
    plungedir(cleandir, todir, cleandir_files_number, cleandir_size, ext_to_filetype, {}, unknown_exts, 
      copybytes_buffer_size)
    sysprint()
  except (OSError, IOError) as exception:
    inform('Error when cleaning directory: \'' + cleandir + '\'.')
    log(msg=traceback.format_exc())
    sys_exit(1, error=type(exception).__name__, send_log=True)

  inform('Cleaning was done successfully.')
  inform('Processed files: ' + str(processed_files_number) + '. (' + print_bytes(processed_files_size) + ')')
  
  check_unknown_files(unknown_files_number, processed_files_number, unknown_exts)
  timedelta = int('{:.0f}'.format(time.time() - timestart))
    
  inform('Cleaned in ' + print_seconds(timedelta) + '.')
  log(act='end')


if __name__ == '__main__':
  main()
