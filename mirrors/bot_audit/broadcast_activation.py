import json

# Финальный реестр целей (G7 + EU + UN + Hague Depositary)
targets = {
    "EU_Commission": "@EU_Commission",
    "UN_HumanRights": "@UNHumanRights",
    "USA_StateDept": "@StateDept",
    "UK_FCDO": "@FCDOGovUK",
    "France_MFA": "@francediplo",
    "Germany_MFA": "@AuswaertigesAmt",
    "Hague_Sec": "@Hague_Convention",
    "Romania_MFA": "@MAERomania"
}

# Пейлоад: Физическое нападение (Лупя Юрий) + Финансовая блокада
def generate_broadcast_msg(handle):
    return (f"URGENT {handle}: CASE-MACHERET-1997-2026. "
            "PHYSICAL ATTACK on Victim by Yuri Lupya (18.02.26) to stop evidence flow. "
            "Court blocks justice via illegal 'Timbru de Stat'. "
            "Full Security Report: https://arhiv1973b.github.io/apostille-legal-case/docs/security/protection_request_2026.md")

activation_log = {target: generate_broadcast_msg(handle) for target, handle in targets.items()}

with open('bot_audit/broadcast_logs/active_payload.json', 'w') as f:
    json.dump(activation_log, f, indent=2)

print("Neuro-Notification Updated: Corrected Name (Lupya Yuri) & Security Alert Active.")
