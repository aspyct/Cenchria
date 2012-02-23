# Copyright (c) 2012 Antoine d'Otreppe de Bouvette
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import server as cserver

class HttpRequest(object):
    def __init__(self):
        self.headers = {}
        self.body = None
        self.tmp = ""
        self.firstLine = None
    
    def addData(self, data):
        tmp = self.tmp + data
        
        eol = tmp.find("\n")
        while eol >= 0:
            start = eol
            if tmp[start - 1] == "\r":
                start -= 1
            
            headerLine = tmp[:start]
            
            if headerLine:
                if self.firstLine is None:
                    self.firstLine = headerLine
                    print("First line: %s" % headerLine)
                else:
                    print("Received header: %s" % repr(headerLine))
            else:
                print("End of headers")
            
            tmp = tmp[eol + 1:]
            
            eol = tmp.find("\n")
        
        self.tmp = tmp

class HttpClient(cserver.Client):
    def __init__(self):
        cserver.Client.__init__(self)
        self.currentRequest = HttpRequest()
    
    def handleIncomingData(self, data):
        self.currentRequest.addData(data)

if __name__ == '__main__':
    runner = cserver.CommandLineRunner()
    runner.server.clientManager.makeClient = HttpClient
    runner.run()
