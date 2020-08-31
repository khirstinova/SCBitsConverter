from openpyxl import Workbook, load_workbook
from pathlib import Path
from zipfile import ZipFile
import os
import sys
import tempfile
from lxml import etree as XMLTree

class SCBitsConverterManager:

    def __init__(self, files):
        self.files_to_convert = files
        self.file_map = dict()
        for f in self.files_to_convert:
            t = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
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
                converter = SCBitsConverter(self.file_map[f.name].name, f.name)
                filename = converter.convert()
                zipFile.write(filename)
            zipFile.close()
            file = open(zipFile, "rb")
            bytes = file.read()
            file.close()
            return 'SCBitsXML.zip', bytes
        else:
            converter = SCBitsConverter(self.file_map[self.files_to_convert[0].name].name)
            return_bytes = converter.convert()
            return Path(self.files_to_convert[0].name).stem + '.xml', return_bytes


class SCBitsConverter:

    # define the XML namespaces for the document
    root_ns_map = {
        None: "http://specifications.silverchair.com/xsd/1/25/SCBITS-book.xsd",
        "mml": "http://www.w3.org/1998/Math/MathML",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi":"http://www.w3.org/2001/XMLSchema-instance",
        "ali": "http://www.niso.org/schemas/ali/1.0/"
    }

    def __init__(self, filename):
        self.file_to_convert = filename
        self.xml_document_root = XMLTree.Element('book', nsmap=self.root_ns_map)
        self.xml_document_root.set('book-type', 'book')

        # set the default language
        attr = self.xml_document_root.attrib
        attr['{http://specifications.silverchair.com/xsd/1/25/SCBITS-book.xsd}lang'] = "en"
        self.book_meta_root = None

        self.sheet_index_handler = {
            0: self.handle_book_sheet,
            1: self.handle_front_matter_sheet
        }

        self.cell_handler_map = {
            "publisher:": self.handle_publisher_cell,
            "doi:": self.handle_doi_cell
        }

    def convert(self):
        index = 0
        workbook = load_workbook(self.file_to_convert)
        for sheet in workbook:
            if index in self.sheet_index_handler.keys():
                self.sheet_index_handler[index](sheet, index)
            else:
                self.handle_chapter_sheet(sheet, index)
            index += 1
        xml_data = XMLTree.tostring(self.xml_document_root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return xml_data

    def handle_book_sheet(self, sheet, index):
        self.book_meta_root = XMLTree.SubElement(self.xml_document_root, 'book-meta')
        for row in sheet.iter_rows():
            cell_header = None
            for cell in row:
                if cell.value is not None and cell_header is None:
                    cell_header = cell.value.lower().strip()
                elif cell.value is not None and cell_header is not None:
                    if cell_header in self.cell_handler_map.keys():
                        self.cell_handler_map[cell_header](self.book_meta_root, cell.value)
                    else:
                        error_element = XMLTree.SubElement(self.xml_document_root, "error")
                        error_element.text = "XML conversion error: Unexpected cell header (" + cell_header \
                                             + ") in sheet " + str(index)
        return

    def handle_front_matter_sheet(self, sheet, index):
        return None

    def handle_chapter_sheet(self, sheet, index):
        return None

    def handle_publisher_cell(self, element, publisher):
        publisher_element = XMLTree.SubElement(element, 'book-id')
        publisher_element.set('book-id-type', 'publisher-id')
        publisher_element.text = publisher

    def handle_doi_cell(self, element, DOI):
        doi_element = XMLTree.SubElement(element, 'book-id')
        doi_element.set('book-id-type', 'doi')
        doi_element.text = DOI
