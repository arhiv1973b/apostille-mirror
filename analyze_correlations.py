import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

# --- Пути к файлам ---
BASE_DIR = r"H:\ACTOR_DEV_ENV"
TIMELINE_PATH = os.path.join(
    BASE_DIR, r"apostille-mirror\FORENSIC_TIMELINE_20260615.json"
)
MED_EVENTS_PATH = os.path.join(BASE_DIR, "medical_identity_events.json")
REPORT_PATH = os.path.join(BASE_DIR, r"legal_analysis\correlation_report.md")


def parse_date(date_str):
    if not date_str or date_str == "unknown":
        return None
    if not date_str or date_str == "unknown":
        return None
    # Clean up common date formats
    date_str = date_str.replace("T", " ").replace("Z", "")
    if "." in date_str:
        date_str = date_str.split(".")[0]

    try:
        # Try parsing YYYY-MM-DD HH:MM:SS
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            # Try parsing YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None


def build_unified_timeline():
    unified_events = []

    # 1. Парсинг FORENSIC_TIMELINE
    if os.path.exists(TIMELINE_PATH):
        with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for e in data:
                ts = parse_date(e.get("Timestamp"))
                if ts:
                    detail = e.get("Detail", "")
                    if "Victoriabank" in detail:
                        category = "FINANCIAL"
                    elif "Fiscal de Stat" in detail:
                        category = "ADMINISTRATIVE"
                    else:
                        category = "ADMINISTRATIVE"

                    unified_events.append(
                        {"date": ts, "category": category, "title": e.get("Detail")}
                    )

    # 2. Парсинг medical_identity_events
    if os.path.exists(MED_EVENTS_PATH):
        with open(MED_EVENTS_PATH, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            for e in data.get("events", []):
                ts = parse_date(e.get("date"))
                if ts:
                    unified_events.append(
                        {"date": ts, "category": "MEDICAL", "title": e.get("title")}
                    )

    return sorted(unified_events, key=lambda x: x["date"])


def analyze_clusters(events, window_days=45):
    clusters = []
    for i in range(len(events)):
        cluster = [events[i]]
        for j in range(i + 1, len(events)):
            if (events[j]["date"] - events[i]["date"]).days <= window_days:
                cluster.append(events[j])
            else:
                break

        # Check if cluster has multiple categories
        categories = set(e["category"] for e in cluster)
        if len(categories) > 1:
            clusters.append(cluster)
    return clusters


def generate_markdown_report(events, clusters):
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# CORRELATION REPORT: SYSTEMIC INTERFERENCE\n\n")
        f.write("## 1. HEATMAP (MONTHLY DISTRIBUTION)\n\n")

        # Monthly matrix
        matrix = defaultdict(lambda: defaultdict(int))
        for e in events:
            month = e["date"].strftime("%Y-%m")
            matrix[month][e["category"]] += 1

        f.write("| Month | FINANCIAL | MEDICAL | ADMINISTRATIVE |\n")
        f.write("|-------|-----------|---------|----------------|\n")
        for month in sorted(matrix.keys()):
            f.write(
                f"| {month} | {matrix[month]['FINANCIAL']} | {matrix[month]['MEDICAL']} | {matrix[month]['ADMINISTRATIVE']} |\n"
            )

        f.write("\n\n## 2. DETECTED CLUSTERS (PROXIMITY ANALYSIS)\n\n")
        for i, cluster in enumerate(clusters):
            f.write(f"### Cluster {i + 1}\n")
            f.write(
                f"Period: {cluster[0]['date'].date()} to {cluster[-1]['date'].date()}\n\n"
            )
            for e in cluster:
                f.write(f"- [{e['category']}] {e['date'].date()}: {e['title']}\n")
            f.write("\n")


if __name__ == "__main__":
    events = build_unified_timeline()
    clusters = analyze_clusters(events)
    generate_markdown_report(events, clusters)
    print(f"Correlation report generated at {REPORT_PATH}")
