# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

from lib.reports import *
from lib.utils.file_utils import FileUtils

import time
import sys


class PlainTextReport(FileBaseReport):
    def addPath(self, path, status, response):
        try:
            contentLength = int(response.headers["content-length"])
        except (KeyError, ValueError):
            contentLength = len(response.body)

        try:
            location = response.headers["location"]
        except (KeyError, ValueError):
            location = None

        self.storeData((path, status, contentLength, location))

    def generate(self):
        result = "# Dirsearch started {0} as: {1}\n\n".format(time.ctime(), ' '.join(sys.argv))

        for path, status, contentLength, location in self.pathList:
            result += "{0}  ".format(status)
            result += "{0}  ".format(FileUtils.size_human(contentLength).rjust(6, " "))
            result += "{0}://{1}:{2}/".format(self.protocol, self.host, self.port)
            result += (
                "{0}".format(path)
                if self.basePath == ""
                else "{0}/{1}".format(self.basePath, path)
            )
            if location:
                result += "    -> REDIRECTS TO: {0}".format(location)

            result += "\n"

        return result
