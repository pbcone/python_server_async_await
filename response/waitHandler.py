import time
import asyncio

class MockWait():
    def wait(self):
        return "waited 5 seconds"


class WaitHandler():

    def __init__(self):
        self.contentType = ""
        self.contents = MockWait()

    def getContents(self):
        return self.contents.wait()

    async def wait(self):
        self.setStatus(200)
        print('waiting.....')
        await asyncio.sleep(5)
        print('finished')
        return 

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getContentType(self):
        return self.contentType 

    def getType(self):
        return 'static'