import os
import json
import hashlib
import time
from datetime import datetime, timezone
from ti_ula_replicator import sync_to_decentralized_cloud

# TI-ULA REAL-TIME DIRECTORY WATCHER & REPLICATOR (ZERO-DEPENDENCY POLLING)
# Case: CASE-MACHERET-1997-2026 | Protocol: UDHR-Override (Article 8)

TARGET_VAULTS = [
    "CADASTRAL_RECORDS",
    "MUNICIPAL_ARCHIVE_DUPLICATES",
    "PROPERTY_ALLOCATIONS",
]
MANIFEST_PATH = "ti_ula_convergence_cycle_iii.json"
POLL_INTERVAL_SECONDS = 5


def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def watch_vaults():
    print("=== TI-ULA REAL-TIME DIRECTORY WATCHER ACTIVE ===")
    print(f"Monitoring vaults: {TARGET_VAULTS} (Interval: {POLL_INTERVAL_SECONDS}s)")

    known_files = {}

    # Initial scan
    for vault in TARGET_VAULTS:
        os.makedirs(vault, exist_ok=True)
        for root, _, files in os.walk(vault):
            for file in files:
                fp = os.path.join(root, file)
                try:
                    known_files[fp] = os.path.getmtime(fp)
                except Exception:
                    pass

    try:
        while True:
            time.sleep(POLL_INTERVAL_SECONDS)
            current_files = {}
            updated = False

            for vault in TARGET_VAULTS:
                if not os.path.exists(vault):
                    continue
                for root, _, files in os.walk(vault):
                    for file in files:
                        fp = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(fp)
                            current_files[fp] = mtime
                            if fp not in known_files or known_files[fp] != mtime:
                                print(
                                    f"[!] New/Modified evidentiary artifact detected: {fp}"
                                )
                                known_files[fp] = mtime
                                updated = True
                        except Exception:
                            pass

            if updated:
                # Re-run anchoring
                anchors = []
                for vault in TARGET_VAULTS:
                    if not os.path.exists(vault):
                        continue
                    for root, _, files in os.walk(vault):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                h = get_file_hash(filepath)
                                anchors.append(
                                    {
                                        "node_type": "physical_document_scan",
                                        "path": filepath,
                                        "sha256": h,
                                        "timestamp": datetime.now(
                                            timezone.utc
                                        ).isoformat()
                                        + "Z",
                                        "udhr_binding": "Article 8",
                                    }
                                )
                            except Exception:
                                pass

                manifest = {
                    "cycle": "III_MUNICIPAL_CADASTRAL_SEAL_REALTIME",
                    "case_id": "CASE-MACHERET-1997-2026",
                    "total_anchored": len(anchors),
                    "cryptographic_locks": anchors,
                }
                with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, indent=4, ensure_ascii=False)
                print(
                    f"[✓] Manifest updated in real-time: {len(anchors)} records locked."
                )
                print("[>] Triggering decentralized cloud replication...")
                sync_to_decentralized_cloud()

    except KeyboardInterrupt:
        print("\n[!] Directory watcher terminated by operator.")


if __name__ == "__main__":
    watch_vaults()
