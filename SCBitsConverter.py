from openpyxl import Workbook
from zipfile import ZipFile
import os
import sys
import tempfile


class SCBitsConverterManager:

    def __init__(self, files):
        self.files_to_convert = files
        self.file_map = dict()
        for f in self.files_to_convert:
            t = tempfile.NamedTemporaryFile(delete=False)
            self.file_map[f.name] = t
            for chunk in f.chunks():
                t.write(chunk)
            t.close()

    def get_mime_type(self):
        if len(self.files_to_convert) > 1:
            return "application/zip"
        else:
            return "application/xml"

    def get_data(self):
        if len(self.files_to_convert) > 1:
            zipFile = ZipFile('SCBitsXML.zip')
            for f in self.files_to_convert:
                converter = SCBitsConverter(self.file_map[f.name].name)
                filename = converter.convert()
                zipFile.write(filename)
            zipFile.close()
            file = open(zipFile, "rb")
            bytes = file.read()
            file.close()
            return 'SCBitsXML.zip', bytes
        else:
            converter = SCBitsConverter(self.file_map[self.files_to_convert[0].name].name)
            filename = converter.convert()
            file = open(filename, "rb")
            bytes = file.read()
            file.close()
            return os.path.basename(filename), bytes


class SCBitsConverter:

    def __init__(self, filename):
        self.file_to_convert = filename

    def convert(self):
        return self.file_to_convert
