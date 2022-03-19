
import csv
import sys
import argparse
import struct

from dbfread import DBF
from io import open
from builtins import str

def __convert(input_file_path, output_file):

	def encode_decode(x):
		"""
		DBF returns a unicode string encoded as args.input_encoding.
		We convert that back into bytes and then decode as args.output_encoding.
		"""
		if not isinstance(x, str):
			# DBF converts columns into non-str like int, float
			x = str(x) if x is not None else ''
		return x.encode('cp850').decode('utf8')

	try:
		input_reader = DBF(input_file_path,
						   encoding='cp850',
						   ignore_missing_memofile=True)

		print(output_file)
		output_writer = csv.DictWriter(output_file,
								   quoting=csv.QUOTE_MINIMAL,
								   escapechar='\\',
								   delimiter=',',
								   fieldnames=[encode_decode(x) for x in input_reader.field_names])

		output_writer.writeheader()
		for record in input_reader:
			row = {encode_decode(k):encode_decode(v) for k,v in record.items()}
			output_writer.writerow(row)
	
	except (UnicodeDecodeError, LookupError):
		log.error('Error: Unknown encoding\n')
		exit(0)
	except UnicodeEncodeError:
		log.error('Error: Can\'t encode to output encoding: {}\n'.format(
			args.to_charset))
		exit(0)
	except struct.error:
		log.error('Error: Bad input file format: {}\n'.format(
			os.path.basename(input_file_path))
		)
		exit(0)

if __name__ == '__main__':

	with open(sys.argv[2], 'w', encoding='utf8') as output_file:
		__convert(sys.argv[1], output_file)