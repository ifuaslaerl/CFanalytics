from abc import ABC, abstractmethod
from typing import List
import requests
from models import Problem, Submission

class PlatformAPI(ABC):
    """Contrato que toda plataforma de CP deve seguir."""
    
    @abstractmethod
    def get_user_submissions(self, handle: str) -> List[Submission]:
        pass

class CodeforcesAPI(PlatformAPI):
    BASE_URL = "https://codeforces.com/api"

    def get_user_submissions(self, handle: str) -> List[Submission]:
        url = f"{self.BASE_URL}/user.status?handle={handle}"
        try:
            response = requests.get(url, timeout=10).json()
        except requests.exceptions.RequestException:
            return []
        
        if response.get("status") != "OK":
            return []

        submissions = []
        for sub in response["result"]:
            prob_data = sub.get("problem", {})
            if "contestId" not in prob_data:
                continue

            problem = Problem(
                platform="Codeforces",
                contest_id=str(prob_data["contestId"]),
                index=prob_data["index"],
                name=prob_data.get("name", "Desconhecido"),
                rating=prob_data.get("rating", "Sem Rating"),
                tags=prob_data.get("tags", [])
            )
            
            submissions.append(Submission(
                id=sub["id"],
                creation_time_seconds=sub["creationTimeSeconds"],
                problem=problem,
                programming_language=sub["programmingLanguage"],
                verdict=sub.get("verdict", "UNKNOWN")
            ))
        return submissions

class AtCoderAPI(PlatformAPI):
    BASE_URL = "https://kenkoooo.com/atcoder/atcoder-api/v3"

    def get_user_submissions(self, handle: str) -> List[Submission]:
        url = f"{self.BASE_URL}/user/submissions?user={handle}&epoch_second=0"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException:
            return []

        submissions = []
        verdict_map = {"AC": "OK", "WA": "WRONG_ANSWER", "TLE": "TIME_LIMIT_EXCEEDED"}
        
        for sub in data:
            mapped_verdict = verdict_map.get(sub["result"], sub["result"])
            problem = Problem(
                platform="AtCoder",
                contest_id=sub["contest_id"],
                index=sub["problem_id"],
                name=sub["problem_id"].upper(),
                rating="Sem Rating"
            )

            submissions.append(Submission(
                id=sub["id"],
                creation_time_seconds=sub["epoch_second"],
                problem=problem,
                programming_language=sub["language"],
                verdict=mapped_verdict
            ))
        return submissions