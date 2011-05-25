# Just a simple script for testing out XSP.

import sys
import xsp

XML_INFILE = 'users.xml'
XML_OUTFILE = 'new_users.xml'

PARSE_VOCABULARY = {
	'user': {
		'id': int,
		'name': str,
		'surname': str
	},
	'group': {
		'id': int,
		'name': str,
		None: {
			'member': {
				'user': int
			}
		}
	}
}
WRITE_VOCABULARY = {
	'users': {
		'host': 'localhost',
		'domain': 'localdomain',
		None: {
			'user': [
				{'id': 1000, 'name': 'Mike', 'surname': 'Smith'},
				{'id': 1001, 'name': 'John', 'surname': 'McDonald'},
				{'id': 1002, 'name': 'Wendy', 'surname': 'Harvey'}
			],
			'group': [
				{
					'id': 9999, 
					'name': 'people', 
					None: {
						'member': [
							{'id': 1000},
							{'id': 1001},
							{'id': 1002}
						]
					}
				}
			]
		}
	}
}

print 'Testing xsp.parse:'
print xsp.parse(XML_INFILE, PARSE_VOCABULARY)

print '\nTesting xsp.write:'
outfile = open(XML_OUTFILE, 'w')
xsp.write(outfile, WRITE_VOCABULARY)
outfile.close()
