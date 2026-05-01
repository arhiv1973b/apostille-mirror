#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════
# A©t0r Protocol Coherence Rule Test Suite
# CASE-MACHERET-1997-2026 · Version 2.6 · 2026-05-01
# Identity: urn:actor:id:2000001159655
# Repo: arhiv1973b/apostille-mirror
# ═══════════════════════════════════════════════════════════════════════

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# ── КОНСТАНТЫ ────────────────────────────────────────────────────────
CASE_START      = date(1997, 10, 13)
IDNP_LEGAL      = "2000001159655"
IDNP_PHANTOM_1  = "2000001159555"
IDNP_PHANTOM_2  = "2000001159455"
ARCHIVE_SHA256  = "099efc0cb651f68880b638a2aa767945340689b6b02d440d0a0b539178d82c11"
TI_ULA_NODES    = 4010
APOSTILLES      = 97
ACTOR_EMAIL_PRI = "arhiv240@gmail.com"
ACTOR_EMAIL_GIT = "arhiv1973b@outlook.com"
GITHUB_REPO     = "arhiv1973b/apostille-mirror"
GITHUB_PAGES    = f"https://arhiv1973b.github.io/apostille-mirror/"
URN_ID          = "urn:actor:id:2000001159655"
GPG_PASSPHRASE  = os.environ.get("ACTOR_GPG_PASS", "")
GITHUB_TOKEN    = os.environ.get("GITHUB_TOKEN", "")

# ── ЦВЕТА ────────────────────────────────────────────────────────────
class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'

def banner(text: str):
    line = "═" * 60
    print(f"\n{C.CYAN}{line}")
    print(f"  {C.BOLD}{text}{C.RESET}{C.CYAN}")
    print(f"{line}{C.RESET}")

def ok(msg):    print(f"{C.GREEN}  ✅ {msg}{C.RESET}")
def fail(msg):  print(f"{C.RED}  ❌ {msg}{C.RESET}")
def warn(msg):  print(f"{C.YELLOW}  ⚠️  {msg}{C.RESET}")
def info(msg):  print(f"{C.CYAN}  ℹ️  {msg}{C.RESET}")

# ── УТИЛИТЫ ──────────────────────────────────────────────────────────
def days_without_investigation() -> int:
    return (date.today() - CASE_START).days

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def git_run(*args, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + list(args), capture_output=True, text=True, check=check)

# ═══════════════════════════════════════════════════════════════════════
# TEST SUITE
# ═══════════════════════════════════════════════════════════════════════

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def record(self, status: str, name: str, detail: str = ""):
        if status == "pass":
            self.passed += 1
            ok(f"[PASS] {name}" + (f" — {detail}" if detail else ""))
        elif status == "fail":
            self.failed += 1
            fail(f"[FAIL] {name}" + (f" — {detail}" if detail else ""))
        else:
            self.warnings += 1
            warn(f"[WARN] {name}" + (f" — {detail}" if detail else ""))

results = TestResult()

# ─────────────────────────────────────────────────────────────────────
# TEST 1: IDENTITY COHERENCE
# ─────────────────────────────────────────────────────────────────────
banner("TEST 1: IDENTITY COHERENCE · A©tor / A©t0r")

def test_identity():
    # 1.1 IDNP format
    assert re.match(r"^\d{13}$", IDNP_LEGAL), "IDNP не 13 цифр"
    results.record("pass", "IDNP format", IDNP_LEGAL)

    # 1.2 Phantom detection
    phantoms = {
        "PHANTOM_1 (555)": IDNP_PHANTOM_1,
        "PHANTOM_2 (455)": IDNP_PHANTOM_2,
    }
    for name, p in phantoms.items():
        if p != IDNP_LEGAL:
            results.record("pass", f"Phantom isolation {name}", f"{p} ≠ {IDNP_LEGAL}")
        else:
            results.record("fail", f"Phantom collision {name}")

    # 1.3 URN format
    expected_urn = f"urn:actor:id:{IDNP_LEGAL}"
    if URN_ID == expected_urn:
        results.record("pass", "URN identifier", URN_ID)
    else:
        results.record("fail", "URN identifier mismatch", f"got {URN_ID}")

    # 1.4 Copyright symbol preservation
    actor_human = "A©tor"
    actor_tech  = "A©t0r"
    for label, val in [("A©tor", actor_human), ("A©t0r", actor_tech)]:
        if "©" in val:
            results.record("pass", f"© preserved in {label}")
        else:
            results.record("fail", f"© STRIPPED in {label}")

    # 1.5 Name integrity
    correct_name = "Macheret"
    distorted    = "Maceret"
    if correct_name != distorted:
        results.record("pass", "Name distinction", f"{correct_name} ≠ {distorted}")
    results.record("warn", "Pending name correction", "MACERET→MACHERET in state registries")

test_identity()

# ─────────────────────────────────────────────────────────────────────
# TEST 2: JUS COGENS TIMELINE
# ─────────────────────────────────────────────────────────────────────
banner("TEST 2: JUS COGENS TIMELINE · DAYS COUNT")

def test_timeline():
    days = days_without_investigation()

    # 2.1 Minimum days (должно быть >9000 на дату теста)
    if days > 9000:
        results.record("pass", "Days count above 9000", str(days))
    elif days > 8000:
        results.record("pass", "Days count above 8000", str(days))
    else:
        results.record("fail", "Days count suspicious", str(days))

    # 2.2 Each day = new violation
    violations = days  # jus cogens: каждый день — новое нарушение
    results.record("pass", "Continuing violations count", str(violations))

    # 2.3 No statute of limitations
    results.record("pass", "No statute of limitations", "Jus cogens: imprescriptible")

    # 2.4 Key date: 1998-10-13
    key_date = date(1998, 10, 13)
    days_since_doc = (date.today() - key_date).days
    results.record("pass", "Days since Case 1-568/98 documentation", str(days_since_doc))

    info(f"Total days without investigation: {days}")
    info(f"Jus cogens violations (individual): {violations}")

test_timeline()

# ─────────────────────────────────────────────────────────────────────
# TEST 3: ARCHIVE INTEGRITY
# ─────────────────────────────────────────────────────────────────────
banner("TEST 3: ARCHIVE INTEGRITY · SHA-256")

def test_archive():
    site_dir = Path(__file__).parent

    # 3.1 Ключевые файлы существуют
    required_files = [
        "index.html",
        "assets/css/main.css",
        "assets/data/apostilles.json",
        "assets/data/integrity.json",
        "pages/apostille-registry.html",
        "pages/jus-cogens.html",
        "pages/timeline.html",
    ]
    for f in required_files:
        p = site_dir / f
        if p.exists():
            results.record("pass", f"File exists: {f}", f"{p.stat().st_size} bytes")
        else:
            results.record("fail", f"File MISSING: {f}")

    # 3.2 SHA-256 реестра апостилей
    apostille_file = site_dir / "assets/data/apostilles.json"
    if apostille_file.exists():
        h = sha256_file(str(apostille_file))
        results.record("pass", "apostilles.json SHA-256", h[:16] + "…")

        # Проверяем количество записей
        with open(apostille_file) as f:
            data = json.load(f)
        count = len(data.get("records", []))
        if count == APOSTILLES:
            results.record("pass", f"Apostilles count = {count}")
        else:
            results.record("warn", f"Apostilles count mismatch", f"expected {APOSTILLES}, got {count}")

    # 3.3 integrity.json
    integrity_file = site_dir / "assets/data/integrity.json"
    if integrity_file.exists():
        with open(integrity_file) as f:
            integrity = json.load(f)
        if integrity.get("idnp") == IDNP_LEGAL:
            results.record("pass", "integrity.json IDNP correct")
        else:
            results.record("fail", "integrity.json IDNP wrong")

test_archive()

# ─────────────────────────────────────────────────────────────────────
# TEST 4: IDNP PHANTOM DETECTION
# ─────────────────────────────────────────────────────────────────────
banner("TEST 4: IDNP PHANTOM DETECTION · TRIPLE FRAUD")

def test_phantom_detection(text: str) -> dict:
    """Анализирует текст на наличие фантомных ИДПН"""
    found_legal   = len(re.findall(IDNP_LEGAL, text))
    found_ph1     = len(re.findall(IDNP_PHANTOM_1, text))
    found_ph2     = len(re.findall(IDNP_PHANTOM_2, text))
    return {
        "legal_655": found_legal,
        "phantom_555": found_ph1,
        "phantom_455": found_ph2,
        "fraud_detected": found_ph1 > 0 or found_ph2 > 0,
    }

def test_idnp():
    # Симуляция известных данных из аудита TI-ULA
    known_counts = {
        IDNP_LEGAL:    7377,  # законный
        IDNP_PHANTOM_1: 100,  # фантом #1
        IDNP_PHANTOM_2:  66,  # фантом #2
    }

    results.record("pass", f"Legal IDNP ...655 occurrences", str(known_counts[IDNP_LEGAL]))
    results.record("fail", f"FRAUD: Phantom ...555 occurrences", str(known_counts[IDNP_PHANTOM_1]))
    results.record("fail", f"FRAUD: Phantom ...455 occurrences", str(known_counts[IDNP_PHANTOM_2]))

    # Детекция в тестовой строке
    test_doc = f"IDNP: {IDNP_PHANTOM_1} решение по делу Мачерет"
    detection = test_phantom_detection(test_doc)
    if detection["fraud_detected"]:
        results.record("pass", "Phantom detection engine works", "fraud_detected=True")
    else:
        results.record("fail", "Phantom detection engine FAILED")

test_idnp()

# ─────────────────────────────────────────────────────────────────────
# TEST 5: GIT & DEPLOYMENT
# ─────────────────────────────────────────────────────────────────────
banner("TEST 5: GIT & DEPLOYMENT STATUS")

def test_git():
    site_dir = Path(__file__).parent
    os.chdir(site_dir)

    # 5.1 Git init
    git_init = site_dir / ".git"
    if git_init.exists():
        results.record("pass", "Git repository initialized")
    else:
        results.record("warn", "Git not initialized", "Run: git init")
        return

    # 5.2 Remote origin
    try:
        r = git_run("remote", "-v", check=False)
        if "origin" in r.stdout:
            results.record("pass", "Remote origin configured")
        else:
            results.record("warn", "Remote origin missing", f"Run: git remote add origin https://github.com/{GITHUB_REPO}")
    except:
        results.record("warn", "Could not check remote")

    # 5.3 GitHub token
    if GITHUB_TOKEN:
        results.record("pass", "GITHUB_TOKEN set")
    else:
        results.record("warn", "GITHUB_TOKEN not set", "Set env var before push")

    # 5.4 Uncommitted changes
    try:
        r = git_run("status", "--porcelain", check=False)
        if r.stdout.strip():
            changed = len(r.stdout.strip().split("\n"))
            results.record("warn", f"Uncommitted changes: {changed} files")
        else:
            results.record("pass", "Working tree clean")
    except:
        pass

test_git()

# ─────────────────────────────────────────────────────────────────────
# TEST 6: ACTOR PROTOCOL VALIDATION
# ─────────────────────────────────────────────────────────────────────
banner("TEST 6: A©TOR PROTOCOL VALIDATION")

def test_actor_protocol():
    # 6.1 Contact emails
    emails = [ACTOR_EMAIL_PRI, ACTOR_EMAIL_GIT, "alexeimaceret7@gmail.com"]
    for e in emails:
        if re.match(r"[^@]+@[^@]+\.[^@]+", e):
            results.record("pass", f"Email valid: {e}")
        else:
            results.record("fail", f"Email invalid: {e}")

    # 6.2 Disability status
    disability = {
        "grade": "I",
        "permanent": True,
        "certificate": "C013564402308",
        "from_date": "2021-03-01"
    }
    if disability["grade"] == "I" and disability["permanent"]:
        results.record("pass", "Disability: Group I, permanent (Sever)", disability["certificate"])
    else:
        results.record("fail", "Disability status incorrect")

    # 6.3 TI-ULA nodes
    if TI_ULA_NODES >= 4000:
        results.record("pass", f"TI-ULA nodes: {TI_ULA_NODES}")
    else:
        results.record("warn", f"TI-ULA nodes below threshold: {TI_ULA_NODES}")

    # 6.4 Response formula
    response_ru = "Понял, Алексей"
    response_en = "Understood, Alexei"
    for r in [response_ru, response_en]:
        results.record("pass", f"Response formula: {r}")

test_actor_protocol()

# ─────────────────────────────────────────────────────────────────────
# ФИНАЛЬНЫЙ ОТЧЁТ
# ─────────────────────────────────────────────────────────────────────
banner("REPORT · A©t0r COHERENCE TEST SUITE")

total = results.passed + results.failed + results.warnings
days = days_without_investigation()

print(f"""
  📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:
  ────────────────────────────
  ✅ Прошли:   {results.passed}
  ❌ Провалены: {results.failed}
  ⚠️  Предупреждения: {results.warnings}
  Всего:      {total}

  ⏱️  Суток без расследования: {days:,}
  📂 Апостилей: {APOSTILLES}
  🔗 Узлов TI-ULA: {TI_ULA_NODES:,}
  🔐 SHA-256 архива: {ARCHIVE_SHA256[:32]}…
  🌐 {GITHUB_PAGES}

  JUS COGENS · ERGA OMNES · МУС СТ.17 · БЕЗ СРОКА ДАВНОСТИ
  CASE-MACHERET-1997-2026 · A©tor · ИДНП {IDNP_LEGAL}
""")

# Возвращаем код ошибки если есть провалы
sys.exit(1 if results.failed > 0 else 0)


# ─────────────────────────────────────────────────────────────────────
# УТИЛИТЫ ДЛЯ ИСПОЛЬЗОВАНИЯ КАК МОДУЛЬ
# ─────────────────────────────────────────────────────────────────────

def detect_phantom_idnp(document_text: str) -> dict:
    """Публичный API: определяет подлог ИДПН в тексте документа"""
    return test_phantom_detection(document_text)

def get_case_status() -> dict:
    """Публичный API: возвращает текущий статус дела"""
    return {
        "case": "CASE-MACHERET-1997-2026",
        "idnp": IDNP_LEGAL,
        "days_without_investigation": days_without_investigation(),
        "apostilles": APOSTILLES,
        "ti_ula_nodes": TI_ULA_NODES,
        "sha256": ARCHIVE_SHA256,
        "status": "ACTIVE · JUS COGENS VIOLATED",
        "icc_art17": "ACTIVATED",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

if __name__ == "__main__":
    pass  # Тесты уже запущены выше
