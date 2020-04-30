# -*- coding:UTF-8 -*-
from mitmproxy.tools._main import mitmweb
mitmweb(args=['-s', './httpproxy.py', '-p', '8080', '--web-port', '9020'])