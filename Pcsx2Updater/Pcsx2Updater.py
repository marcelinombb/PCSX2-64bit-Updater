import requests, io, re, os
from zipfile import ZipFile
from requests.models import Response
import Pcsx2Updater.Contants as const
from Pcsx2Updater.GithubApi import GithubActionsApi

class Pcsx2Updater:
    
    def __init__(self,rootPath) -> None:
        self.rootPath = rootPath
        self.listDownloads()

    def download(self,artifact):
        return requests.get(artifact['download_url'],headers=const.HEADER_TOKEN,stream=True)

    def update(self,artifact):
        file = self.download(artifact)
        self.writeFile(artifact["name"],file,artifact["size_in_bytes"])
        self.extractFile(artifact["name"])
        os.unlink(f"{artifact['name']}.zip")

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
        self.update(artifacts['artifacts'][artifactId - 1])
    
    def writeFile(self, fileName, fileContent: Response, size_in_bytes):
        print(f"Baixando {fileName}...")
        
        CHUNCK = 1024**2
        
        output_file = io.FileIO(f'{self.rootPath}/{fileName}.zip', "w")

        for chunk in fileContent.iter_content(chunk_size=CHUNCK):
            output_file.write(chunk)

        output_file.close()

    def extractFile(self,fileName):
        print("Extraindo...")
        genericName = self.getGenericName(fileName)
        with ZipFile(f'{self.rootPath}/{fileName}.zip','r') as zip:
            zip.extractall(f'{self.rootPath}/{genericName}')


