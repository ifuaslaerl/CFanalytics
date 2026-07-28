from typing import List, Dict, Set
from models import Problem, Submission
from api import PlatformAPI

class Analytics:
    def __init__(self, apis: List[PlatformAPI], handles: List[str]):
        self.apis = apis
        self.handles = list(set(h.strip() for h in handles if h.strip()))
        self._submissions: List[Submission] = []
        self.load_data()

    def load_data(self):
        for api in self.apis:
            for handle in self.handles:
                try:
                    self._submissions.extend(api.get_user_submissions(handle))
                except Exception as e:
                    print(f"Erro ao processar handle {handle}: {e}")

    def get_upsolving_list(self) -> List[Problem]:
        solved: Set[str] = set()
        attempted: Dict[str, Problem] = {}

        for sub in self._submissions:
            pid = sub.problem.full_id
            if sub.verdict == "OK":
                solved.add(pid)
            else:
                if pid not in attempted:
                    attempted[pid] = sub.problem

        unsolved = [p for pid, p in attempted.items() if pid not in solved]
        unsolved.sort(key=lambda p: (p.rating == "Sem Rating", p.rating))
        return unsolved

    def filter_unsolved(self, target_tags: List[str] = None, contest_id: str = None) -> List[Problem]:
        filtered = self.get_upsolving_list()

        if target_tags:
            target_tags_lower = [t.lower() for t in target_tags]
            filtered = [
                p for p in filtered 
                if any(tag in [t.lower() for t in p.tags] for tag in target_tags_lower)
            ]

        if contest_id:
            filtered = [p for p in filtered if str(p.contest_id) == str(contest_id)]

        return filtered

    def _get_filtered_submissions(self, start_ts: int = None, end_ts: int = None) -> List[Submission]:
        subs = self._submissions
        if start_ts:
            subs = [s for s in subs if s.creation_time_seconds >= start_ts]
        if end_ts:
            subs = [s for s in subs if s.creation_time_seconds <= end_ts]
        return subs

    def get_verdict_stats(self, start_ts: int = None, end_ts: int = None) -> Dict[str, int]:
        stats = {}
        for sub in self._get_filtered_submissions(start_ts, end_ts):
            stats[sub.verdict] = stats.get(sub.verdict, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    def get_language_stats(self, start_ts: int = None, end_ts: int = None) -> Dict[str, int]:
        stats = {}
        for sub in self._get_filtered_submissions(start_ts, end_ts):
            lang = sub.programming_language
            stats[lang] = stats.get(lang, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    def get_tags_stats(self, start_ts: int = None, end_ts: int = None) -> Dict[str, int]:
        stats = {}
        for sub in self._get_filtered_submissions(start_ts, end_ts):
            for tag in sub.problem.tags:
                stats[tag] = stats.get(tag, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
        
    def get_available_tags(self) -> List[str]:
        tags = set()
        for prob in self.get_upsolving_list():
            tags.update(prob.tags)
        return sorted(list(tags))

    def get_incomplete_contests(self) -> Dict[str, List[Problem]]:
        contests: Dict[str, List[Problem]] = {}
        for prob in self.get_upsolving_list():
            contests.setdefault(prob.contest_id, []).append(prob)
        return dict(sorted(contests.items(), reverse=True))