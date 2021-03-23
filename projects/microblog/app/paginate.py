from flask import url_for


def is_pages( items, url, **kwargs ):
	if items.has_next:
		next_url = url_for( url, page = items.next_num, **kwargs )
	else:
		next_url = None

	if items.has_prev:
		prev_url = url_for( url, page = items.prev_num, **kwargs )
	else:
		prev_url = None

	return next_url, prev_url
