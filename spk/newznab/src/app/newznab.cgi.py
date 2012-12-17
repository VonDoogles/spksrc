#!/usr/local/newznab/env/bin/python
import os
import configobj

config = configobj.ConfigObj('/usr/local/newznab/var/config.ini')
protocol = 'https' if int(config['misc']['enable_https']) else 'http'

print 'Location: %s://%s/newznab/www' % (protocol, os.environ['SERVER_NAME'])
print
