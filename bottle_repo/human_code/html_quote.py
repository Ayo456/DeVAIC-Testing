def html_quote(string):
    return '"%s"' % html_escape(string).replace('\n','&#10;')\
                    .replace('\r','&#13;').replace('\t','&#9;')