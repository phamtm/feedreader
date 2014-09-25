#!~/Environments/feedreader/bin/python
# -*- coding: utf-8 -*-u
import re


class VietnameseStemmer(object):

    def _char_to_ascii(self, ch):
        """Convert a Vietnamese character into an ASCII character.
        Ignore all punctuation mark. The rest is converted to lower
        case character.
        """

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


    def _lower(self, ch):
        """Convert a Vietnamese character into an ASCII character.
        Ignore all punctuation mark. The rest is converted to lower
        case character.
        """

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
            return ch


    def stem(self, input_string):
        """Convert a Vietnamese input string into an ASCII string."""

        ascii_string = map(self._char_to_ascii, input_string)
        ascii_string_no_punc = ' '.join(re.findall(r"[\w']+", ''.join(ascii_string)))

        return ascii_string_no_punc
