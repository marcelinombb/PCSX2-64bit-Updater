import requests
import os
import re
import io
from zipfile import ZipFile
import Pcsx2Updater.Contants as const
from Pcsx2Updater.GithubApi import GithubActionsApi

class Pcsx2Updater:
    
    def __init__(self,rootPath) -> None:
        self.rootPath = rootPath
        self.listDownloads()

    def download(self,artifact):
        file = requests.get(artifact['download_url'],headers=const.HEADERS)
        genericName = self.getGenericName(artifact["name"])
        #print(file.content)
        self.writeFile(genericName,file.content)
        ##return file

    def getGenericName(self,name):
        if re.search("AVX2", name, flags=re.IGNORECASE) is None:
            return const.SSE4
        return const.AVX2
    
    def listDownloads(self):

        artifacts = GithubActionsApi().getRunArtifacts()
        print(artifacts["workflowInfo"])
        count = 1 

        for artifact in artifacts["artifacts"]:
            name = artifact["name"]
            print(f'{count}: {self.getGenericName(name)} - {name}')
            count+=1

        artifactId = int(input("Digite o numero da versão que deseja baixar: "))
        self.download(artifacts['artifacts'][artifactId - 1])
    
    def writeFile(self, fileName, fileContent):

        file = open(f'{self.rootPath}/{fileName}.zip', "wb")

        file.write(fileContent)

        file.close()
    
    def extractFile(self,fileName):
        with ZipFile(f'{self.rootPath}/{fileName}','r') as zip:
            zip.extractall(f'{self.rootPath}/{fileName}')


