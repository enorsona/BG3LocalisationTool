import os
import re
import tomllib
import xml.dom.minidom

import xmltodict


class Initializer:

    def __init__(self):
        self.middleDict = None
        self.doneDict = None
        self.configPath = './configs/settings.toml'
        self.configs = None
        self.localisation = None
        self.encode = None
        self.hasConfigFound = os.path.exists(self.configPath)
        self.rawXML = None
        self.rawDict = None
        self.rawText = None
        self.doneText = None
        if self.hasConfigFound:
            self.loadConfig()

    def loadConfig(self):
        with open(self.configPath, mode='r', encoding='utf-8') as binaries:
            raw = tomllib.loads(binaries.read())
            self.configs = raw['Configuration']
            self.localisation = raw[self.configs['application']['language']]
            self.encode = self.configs['application']['encode']

    def processOriginalFile(self, filePath):
        with open(filePath, encoding=self.encode) as binaries:
            self.rawXML = xmltodict.parse(binaries.read())
            processing = self.rawXML['contentList']['content']
            plainText = ''
            for item in processing:
                currentRow = re.sub(r'\n+', '', item['#text'])
                plainText = plainText + currentRow + '\n'
                item['#text'] = currentRow
            self.rawText = plainText.rstrip('\n')
            self.rawDict = processing

    def prepareExportFile(self, filePath):
        unparsed = xmltodict.unparse(self.doneDict)
        XML = xml.dom.minidom.parseString(unparsed)
        processedXML = XML.toprettyxml(indent="    ", encoding=self.encode)
        exportFilename = './resource/' + os.path.basename(filePath).lower().replace('.xml', '') + '_processed.xml'
        with open(exportFilename, mode='wb') as file:
            file.write(processedXML)

    def checkLengthPassed(self):
        backup = self.rawDict
        self.middleDict = self.doneText.split('\n')
        for i in range(len(backup)):
            item = backup[i]
            item['#text'] = self.middleDict[i].rstrip('\n')
        self.doneDict = {
            'contentList': {
                'content': backup
            }
        }
        return len(self.rawDict) == len(backup)
