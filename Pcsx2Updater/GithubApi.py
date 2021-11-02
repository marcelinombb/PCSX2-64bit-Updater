import requests
import re
from requests.models import Response
import Pcsx2Updater.Contants as const

class GithubActionsApi:
    def __init__(self) -> None:
        pass

    def get(self,route) ->Response:
        response = requests.get(f'{const.BASE_URL}/{route}', headers=const.HEADERS)
        return response
    
    def getLastWorkflowRunInfo(self):
        run = self.get(const.WINDOWS_WORFLOW)
        data = run.json()
        return {
            "id": str(data["workflow_runs"][0]["id"]), 
            "created_at": data["workflow_runs"][0]["created_at"]
            }
    
    def getRunArtifacts(self):
        workflow = self.getLastWorkflowRunInfo()
        route = const.ARTIFACTS.replace("{id}", workflow['id'])
        artifacts = self.get(route)
        artifact = {
            "artifacts": self.filterAtifacts(artifacts.json()["artifacts"]), 
            "workflowInfo" : workflow
            }
        return artifact
    
    def is64Bit(self,name) ->bool:
        if re.search("64bit",name,flags=re.IGNORECASE) is None:
           return False
        return True
    
    def filterAtifacts(self,artifacts):
        filteredArtifacts = []

        for artifact in artifacts:
            if self.is64Bit(artifact["name"]):
                filteredArtifacts.append({
                    "id":artifact["id"],
                    "name": artifact["name"],
                    "download_url": artifact["archive_download_url"],
                    "size_in_bytes": int(artifact["size_in_bytes"])
                })

        return filteredArtifacts

    


