#!/usr/bin/env python
#encoding: utf-8

from A import nciic_check
if __name__ == "__main__":
	dict_data = {'id_number':'130534198809273131', 'name': '李献明'}
	res = nciic_check(dict_data)
   	print 'res:'+res;