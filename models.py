from dataclasses import dataclass, field
from typing import List

@dataclass
class Problem:
    platform: str  # Ex: "Codeforces", "AtCoder"
    contest_id: str
    index: str
    name: str
    rating: str | int = "Sem Rating"
    tags: List[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        if self.platform == "Codeforces":
            return f"https://codeforces.com/contest/{self.contest_id}/problem/{self.index}"
        elif self.platform == "AtCoder":
            return f"https://atcoder.jp/contests/{self.contest_id}/tasks/{self.index}"
        return "#"

    @property
    def full_id(self) -> str:
        return f"{self.platform}-{self.contest_id}-{self.index}"

@dataclass
class Submission:
    id: int
    creation_time_seconds: int
    problem: Problem
    programming_language: str
    verdict: str = "UNKNOWN"
    passed_test_count: int = 0
    time_consumed_millis: int = 0
    memory_consumed_bytes: int = 0