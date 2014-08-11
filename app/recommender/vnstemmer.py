#!~/Environments/feedreader/bin/python
# -*- coding: utf-8 -*-u
import re


# Return the ascii character equivalent of a vietnamese character
def vnchar_to_ascii(ch):
	ch = unicode(ch)
	if ch in u'aAáÁàÀảẢãÃạẠăĂắẮằẰẳẲẵẴặẶâÂấẤầẦẩẨẫẪậẬ':
		return 'a'

	elif ch in u'eEéÉèÈẻẺẽẼẹẸêÊếẾềỀểỂễỄệỆ':
		return 'e'

	elif ch in u'iIíÍìÌỉỈĩĨịỊ':
		return 'i'

	elif ch in u'oOóÓòÒỏỎõÕọỌôÔốỐồỒổỔỗỖộỘơƠớỚờỜởỞỡỠợỢ':
		return 'o'

	elif ch in u'uUúÚùÙủỦũŨụỤưƯứỨừỪửỬữỮựỰ':
		return 'u'

	elif ch in u'yYýÝỳỲỷỶỹỸỵ':
		return 'y'

	elif ch in u'dDđĐ':
		return 'd'

	elif ch in '\'`~!@#$%^&*()_+-=[];,./<>?:"{}\\|"':
		return ''

	else:
		# Assume that we only have to deal with Vietnamese and English character
		return ch.lower()


def vnstring_to_ascii(input_string):
	ascii_string = map(vnchar_to_ascii, input_string)
	ascii_string_no_punc = ' '.join(re.findall(r"[\w']+", ''.join(ascii_string)))
	return ascii_string_no_punc