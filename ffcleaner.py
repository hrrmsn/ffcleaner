#!/usr/bin/python -tt
import sys
import re


def main():
	args = sys.argv[1:]
	if not args:
		print 'usage: [--todir dir] dir'
		sys.exit(1)

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
		if '--todir' in ''.join(args):
			print 'error: todir option must be the first'
			sys.exit(1)
		print 'error: must specify only one dir to clean'
		sys.exit(1)
	
	dir_to_clean = args[0]


if __name__ == '__main__':
	main()
	
