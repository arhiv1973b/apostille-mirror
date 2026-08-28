import json
import hashlib
import datetime
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

DAG_FILE = "dag_manifest.json"
KEY_DIR = "crypto_keys"
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "artifact_key")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "artifact_key.pub")


def calculate_sha256(data_dict):
    """Вычисляет SHA-256 для сериализованного JSON-объекта."""
    json_string = json.dumps(data_dict, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(json_string.encode("utf-8")).hexdigest()


def ensure_ed25519_keys():
    """Создает ключи Ed25519, если они отсутствуют."""
    os.makedirs(KEY_DIR, exist_ok=True)
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = ed25519.Ed25519PrivateKey.generate()
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_bytes = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_bytes)
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_bytes)


def load_private_key():
    ensure_ed25519_keys()
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def sign_data(private_key, data_bytes):
    signature = private_key.sign(data_bytes)
    return signature.hex()


def load_dag():
    """Загружает существующий DAG или создает генезис-блок."""
    if os.path.exists(DAG_FILE):
        with open(DAG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_dag(dag_data):
    """Сохраняет обновленный DAG."""
    with open(DAG_FILE, "w", encoding="utf-8") as f:
        json.dump(dag_data, f, ensure_ascii=False, indent=2)


def main():
    dag = load_dag()

    prev_hash = "GENESIS_NODE"
    if len(dag) > 0:
        prev_hash = dag[-1].get("node_hash", "UNKNOWN")

    payload = {
        "case_id": "CASE-MACHERET-1997-2026",
        "document_ref": "Документ (162).pdf",
        "declaration_ref": "A©TOR_KEY=_# [⚖ A©tor Declaration]_.pdf",
        "event_date": "2026-04-21T00:00:00Z",
        "registration_date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "protocol": "A©tor Key / TI-ULA",
        "summary": "Открытое уведомление о выявлении мошенничества и криптографическая фиксация",
        "findings": {
            "fraud_type": [
                "Подлог идентификаторов",
                "Незаконная блокировка активов",
                "Фальсификация записей",
            ],
            "financial_impact_mdl": 25210256.15,
            "target_idnp": "...655...555...455",
            "evidence_count": 90,
            "legal_articles_md": ["191", "332", "349"],
        },
    }

    new_node = {"previous_hash": prev_hash, "payload": payload}

    node_hash = calculate_sha256(new_node)
    new_node["node_hash"] = node_hash

    # Ed25519 cryptographic signature of node_hash
    private_key = load_private_key()
    signature = sign_data(private_key, node_hash.encode("utf-8"))
    new_node["signature_ed25519"] = signature

    dag.append(new_node)
    save_dag(dag)
    print(f"Узел успешно зарегистрирован. Хеш: {node_hash}")
    print(f"Ed25519 Подпись: {signature}")

    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a") as env_file:
            env_file.write(f"NEW_NODE_HASH={node_hash}\n")


if __name__ == "__main__":
    main()
