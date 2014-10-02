import hashlib
data = open('survey.su', 'r').read()

checksum = 'bae469cbf7dd51529ef42f5e83dc33eadaef1be6c4d3f74af066c7de'

if str(hashlib.sha224(data).hexdigest()) == checksum:
	print "Pass!"
else:
	print "fail :-("
