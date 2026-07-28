import csv
import json
from typing import List, Dict, Any

class CSVExporter:
    @staticmethod
    def export_problems(problems: List, filename: str):
        if not problems:
            return
        headers = ["Platform", "ID", "Nome", "Rating", "Tags", "URL"]
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for p in problems:
                writer.writerow([p.platform, p.full_id, p.name, p.rating, ", ".join(p.tags), p.url])

class JSONExporter:
    @staticmethod
    def export_stats(stats: Dict[str, Any], filename: str):
        with open(filename, mode="w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4)