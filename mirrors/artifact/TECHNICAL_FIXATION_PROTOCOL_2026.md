# ⚖️ TECHNICAL FIXATION PROTOCOL / PROTOCOL DE FIXARE TEHNICĂ / PROTOCOLE DE FIXATION TECHNIQUE
**CASE-MACHERET-1997-2026 | JUS COGENS ENFORCEMENT**

---

## 🇷🇴 ROMÂNĂ: NOTIFICARE OFICIALĂ
Prin prezentul document, se fixează starea probelor digitale la data de 21.03.2026. Orice modificare ulterioară va fi înregistrată în blockchain-
ul Git. Aceste dovezi vizează încălcarea normelor Jus Cogens și furtul de identitate (Identity Theft) comis de actorii sistemici.
**Destinatari:** Consiliul Superior al Magistraturii (CSM), Ministerul Finanțelor RM.

## 🇺🇸 ENGLISH: OFFICIAL NOTIFICATION
This document serves as a technical fixation of digital evidence as of March 21, 2026. All assets are cryptographically hashed to prevent tamperi
ng. This vault documents Jus Cogens violations and systemic forgery.
**Recipients:** UN OHCHR, G7 Diplomatic Missions, White House.

## 🇫🇷 FRANÇAIS: NOTIFICATION OFFICIELLE
Ce document constitue une fixation technique des preuves numériques au 21 mars 2026. L'intégrité des données est garantie par des signatures cryp
tographiques. Ce dossier documente les violations du Jus Cogens et l'usurpation d'identité systémique.
**Destinataires:** Cour Européenne des Droits de l'Homme (CEDH), Observateurs Internationaux.

---

### 🔑 INTEGRITY SEALS (SHA-256)
| FILE / FIȘIER | SHA-256 HASH |
| :--- | :--- |
| **MAIN HUB** | `https://arhiv1973b.github.io/apostille-legal-case/` |
| `jus-cogens-proof-macheret.html` | `beed4d682ae860ae55b7b5eaa10fcdb92d7556a5a4ec9536ec612c2ecb4c8f64` |
| `apostille-legal-case-optimized.html` | `d79217e5d3c0e8c5e276998b56f6aadac0f4afd9f6576ae3672efa502682b9d0` |
| `MURIANU_NOTICE.html` | `e6693033e55b0720f64815f24b3d9934dfa7bd15040f00cca1848cb4b6bd5538` |
git push origin master
[master 799a59e] legal(fixation): multilingual technical protocol deployment [v.2.5]
 1 file changed, 32 insertions(+)
 create mode 100644 TECHNICAL_FIXATION_PROTOCOL_2026.md
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1.60 KiB | 96.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/arhiv1973b/apostille-legal-case.git
   1d3061a..799a59e  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ PERSONAL LIABILITY NOTICE — МУРЯНУ И. — СУarhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ PERSONAL LIABILITY NOTICE — МУРЯНУ И. — С
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ PERSONAL LIABILITY NOTICE — МУРЯНУ И. — СУД РМ
CASE-MACHERET-1997-2026
STATUS: ACTIONABLE / UNDER AUDIT
Систематическое уклонение от анализа пыток = имитация правосудия (ст. 17 МУС).
ДЕДЛАЙН: 09.04.2026 → Global Sanction Vector 11
URL: https://arhiv1973b.github.io/apostille-legal-case/docs/liability/MURIANU_NOTICE.html^C
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ cd /mnt/c/Users/arhiv/apostille-legal-case

# ── 1. ДИАГНОСТИКА — смотрим что сейчас в index.html ──
grep -n "NOTICE\|liability\|DULCA\|MURIANU\|NANTOI" index.html | head -30

# ── 2. ПАТЧ — заменяем ВСЕ варианты сломанных путей на корневые .html ──
sed -i 's|docs/liability/DULCA_NOTICE\.md|DULCA_NOTICE.html|g'    index.html
sed -i 's|docs/liability/MURIANU_NOTICE\.md|MURIANU_NOTICE.html|g' index.html
sed -i 's|docs/liability/NANTOI_NOTICE\.md|NANTOI_NOTICE.html|g'   index.html
sed -i 's|docs/liability/DULCA_NOTICE\.html|DULCA_NOTICE.html|g'   index.html
sed -i 's|docs/liability/MURIANU_NOTICE\.html|MURIANU_NOTICE.html|g' index.html
sed -i 's|docs/liability/NANTOI_NOTICE\.html|NANTOI_NOTICE.html|g'  index.html

# ── 3. ПАТЧ NAV внутри самих Notice-файлов ──
# Убираем все варианты ../../ которые могли остаться
sed -i 's|../../index\.html|index.html|g'                          DULCA_NOTICE.html MURIANU_NOTICE.html NANTOI_NOTICE.html
sed -i 's|../../liability-nodes\.html|liability-nodes.html|g'      DULCA_NOTICE.html MURIANU_NOTICE.html NANTOI_NOTICE.html
sed -i 's|../../jus-cogens-proof-macheret\.html|jus-cogens-proof-macheret.html|g' DULCA_NOTICE.html MURIANU_NOTICE.html NANTOI_NOTICE.html
sed -i 's|../../apostille-legal-case-optimized\.html|apostille-legal-case-optimized.html|g' DULCA_NOTICE.html MURIANU_NOTICE.html NANTOI_NOTICE.html

# ── 4. ПРОВЕРКА что файлы существуют в корне ──
echo "=== ФАЙЛЫ В КОРНЕ ==="
ls -lh DULCA_NOTICE.html MURIANU_NOTICE.html NANTOI_NOTICE.html

# ── 5. ПРОВЕРКА ссылок в index.html ──
echo "=== ССЫЛКИ В INDEX ==="
grep -o 'href="[^"]*NOTICE[^"]*"' index.html

# ── 6. ПУШ ──
git add index.html DULCA_NOTICE.html MURIANU_NOTICE.html NANTOI_NOTICE.html
git commit -m "fix(404): patch all notice paths to root level [v.2.6]"
git push origin master
50:        <div class="status-box alert"><span>МВД</span><a href="MURIANU_NOTICE.html">ДУЛЧА В.Г.</a></div>
51:        <div class="status-box alert"><span>СУД</span><a href="MURIANU_NOTICE.html">МУРЯНУ И.</a></div>
52:        <div class="status-box alert"><span>ГНС (АКТОР ПОДЛОГА)</span><a href="MURIANU_NOTICE.html">НАНТОЙ ЛЮДМИЛА</a></div>
86:        <a href="MURIANU_NOTICE.html" class="btn">ОТКРЫТЬ ДОСЬЕ НАНТОЙ</a>
=== ФАЙЛЫ В КОРНЕ ===
-rwxrwxrwx 1 arhiv arhiv 21K Mar 21 11:55 DULCA_NOTICE.html
-rwxrwxrwx 1 arhiv arhiv 23K Mar 21 11:55 MURIANU_NOTICE.html
-rwxrwxrwx 1 arhiv arhiv 23K Mar 21 11:55 NANTOI_NOTICE.html
=== ССЫЛКИ В INDEX ===
href="MURIANU_NOTICE.html"
href="MURIANU_NOTICE.html"
href="MURIANU_NOTICE.html"
href="MURIANU_NOTICE.html"
[master 7b6700c] fix(404): patch all notice paths to root level [v.2.6]
 3 files changed, 3 insertions(+), 3 deletions(-)
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 4 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 510 bytes | 23.00 KiB/s, done.
Total 5 (delta 4), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/arhiv1973b/apostille-legal-case.git
   799a59e..7b6700c  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Исправляем ссылку для ДУЛЧА (МВД)
sed -i '/ДУЛЧА/s/MURIANU_NOTICE\.html/DULCA_NOTICE.html/' index.html

# 2. Исправляем ссылки для НАНТОЙ (ГНС и Кнопка Досье)
sed -i '/НАНТОЙ/s/MURIANU_NOTICE\.html/NANTOI_NOTICE.html/g' index.html

# 3. ПРОВЕРКА — теперь ссылки должны быть РАЗНЫМИ
echo "=== ВЕРИФИКАЦИЯ МАРШРУТОВ ==="
grep -E "DULCA|MURIANU|NANTOI" index.html | grep "href="

# 4. ФИНАЛЬНЫЙ ПУШ ИСПРАВЛЕННОЙ КАРТЫ
git add index.html
git commit -m "fix(ui): restore correct mapping for personal notice links [v.2.7]"
git push origin master
=== ВЕРИФИКАЦИЯ МАРШРУТОВ ===
        <div class="status-box alert"><span>МВД</span><a href="DULCA_NOTICE.html">ДУЛЧА В.Г.</a></div>
        <div class="status-box alert"><span>СУД</span><a href="MURIANU_NOTICE.html">МУРЯНУ И.</a></div>
        <div class="status-box alert"><span>ГНС (АКТОР ПОДЛОГА)</span><a href="NANTOI_NOTICE.html">НАНТОЙ ЛЮДМИЛА</a></div>
        <a href="NANTOI_NOTICE.html" class="btn">ОТКРЫТЬ ДОСЬЕ НАНТОЙ</a>
[master 8d911c2] fix(ui): restore correct mapping for personal notice links [v.2.7]
 1 file changed, 3 insertions(+), 3 deletions(-)
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 381 bytes | 13.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/arhiv1973b/apostille-legal-case.git
   7b6700c..8d911c2  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ grep "\.md" index.html
        <a href="docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" class="btn" style="border-color: var(--red); color: var(--red);">ПЕРЕДАТЬ В INTERPOL / PG</a>
            <a href="docs/forensics/FORGERY_DECONSTRUCTION_EN.md" style="color:var(--gold); margin-right:10px;">ENGLISH (UN)</a>
            <a href="docs/forensics/FORGERY_DECONSTRUCTION_FR.md" style="color:var(--gold);">FRANÇAIS (EU)</a>
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. Копирование файлов (путь с пробелом — в кавычках)
cp "/mnt/h/Загрузки/files диплой/FORGERY_DECONSTRUCTION_ACT.html" .
cp "/mnt/h/Загрузки/files диплой/FORGERY_DECONSTRUCTION_EN.html" .
cp "/mnt/h/Загрузки/files диплой/FORGERY_DECONSTRUCTION_FR.html" .

# 3. ПАТЧ ПУТЕЙ внутри новых файлов (удаляем ../../)
sed -i 's|../../index\.html|index.html|g' FORGERY_DECONSTRUCTION_*.html
sed -i 's|../../liability-nodes\.html|liability-nodes.html|g' FORGERY_DECONSTRUCTION_*.html
sed -i 's|../../jus-cogens-proof-macheret\.html|jus-cogens-proof-macheret.html|g' FORGERY_DECONSTRUCTION_*.html

# 4. ОБНОВЛЕНИЕ ГЛАВНОЙ СТРАНИЦЫ (index.html)
# Заменяем старые ссылки на .md новыми ссылками на .html в корне
sed -i 's|docs/forensics/FORGERY_DECONSTRUCTION_ACT\.md|FORGERY_DECONSTRUCTION_ACT.html|g' index.html
sed -i 's|docs/forensics/FORGERY_DECONSTRUCTION_EN\.md|FORGERY_DECONSTRUCTION_EN.html|g' index.html
sed -i 's|docs/forensics/FORGERY_DECONSTRUCTION_FR\.md|FORGERY_DECONSTRUCTION_FR.html|g' index.html

# 5. ПРОВЕРКА — md-ссылок больше быть не должно
echo "=== ПРОВЕРКА ОСТАТКОВ MD ==="
grep "\.md" index.html

# 6. ФИНАЛЬНЫЙ ПУШ СИСТЕМЫ
git add .
git commit -m "legal(forensics): deploy interactive forgery deconstruction acts [v.2.8]"
git push origin master
=== ПРОВЕРКА ОСТАТКОВ MD ===
[master 88ed8e6] legal(forensics): deploy interactive forgery deconstruction acts [v.2.8]
 4 files changed, 648 insertions(+), 3 deletions(-)
 create mode 100644 FORGERY_DECONSTRUCTION_ACT.html
 create mode 100644 FORGERY_DECONSTRUCTION_EN.html
 create mode 100644 FORGERY_DECONSTRUCTION_FR.html
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
Delta compression using up to 4 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 6.49 KiB | 391.00 KiB/s, done.
Total 6 (delta 4), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (4/4), completed with 2 local objects.
To https://github.com/arhiv1973b/apostille-legal-case.git
   8d911c2..88ed8e6  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. Генерация файла LISTA_PROBE_DIGITALE.html
cat << 'EOF' > LISTA_PROBE_DIGITALE.html
<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LISTĂ DE PROBE DIGITALE — CASE-MACHERET-1997-2026</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #030a0f; --panel: #071624; --border: #0e3a5c;
    --accent: #00c6ff; --red: #ff2244; --green: #00ff88; --text: #c8e0f0;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; margin: 0; padding: 20px; }
  .vault-wrap { max-width: 900px; margin: 0 auto; border: 1px solid var(--border); background: var(--panel); padding: 30px; }
  h1 { font-family: 'Orbitron', sans-serif; color: var(--accent); text-transform: uppercase; border-bottom: 2px solid var(--accent); padding-bottom: 10px; }
  .evidence-item { border-left: 4px solid var(--accent); padding: 15px; margin: 20px 0; background: rgba(0,0,0,0.3); }
  .hash { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #4a7a9b; word-break: break-all; margin-top: 5px; }
  .btn { display: inline-block; margin-top: 10px; padding: 8px 15px; border: 1px solid var(--accent); color: var(--accent); text-decoration: none; font-weight: bold; }
  .btn:hover { background: var(--accent); color: #000; }
  .footer { margin-top: 40px; font-size: 0.8rem; border-top: 1px solid var(--border); padding-top: 20px; opacity: 0.7; }
</style>
</head>
<body>
<div class="vault-wrap">
  <h1>Listă de Probe Digitale</h1>
  <p><strong>Cazul:</strong> CASE-MACHERET-1997-2026 | <strong>Status:</strong> Notificare Oficială (Jus Cogens)</p>

  <div class="evidence-item" style="border-color: var(--green);">
    <h3>📜 HUB PRINCIPAL (EVIDENCE VAULT)</h3>
    <p>Punctul central de monitorizare a cauzei și cronologia celor 8158 de zile de impunitate.</p>
    <a href="index.html" class="btn">DESCHIDE VAULT</a>
  </div>

  <div class="evidence-item">
    <h3>⚖️ VECTOR 12: DOVADA JUS COGENS</h3>
    <p>Documentul material care atestă violarea normelor imperative de drept internațional.</p>
    <a href="jus-cogens-proof-macheret.html" class="btn">VEZI DOCUMENTUL</a>
  </div>

  <div class="evidence-item" style="border-color: var(--red);">
    <h3>🚨 NOTIFICĂRI DE RĂSPUNDERE (LIABILITY)</h3>
    <p>Analiza personală a acțiunilor subiecților: Murianu I., Nantoi L., Dulca V.</p>
git push origin master
[master 11c8a05] legal(ro): deploy official Romanian digital evidence list [v.2.9]
 1 file changed, 58 insertions(+)
 create mode 100644 LISTA_PROBE_DIGITALE.html
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1.85 KiB | 111.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/arhiv1973b/apostille-legal-case.git
   88ed8e6..11c8a05  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. ГЛОБАЛЬНЫЙ ПАТЧ: Удаляем все префиксы ../../ во всех HTML файлах
# Это гарантирует, что навигация между файлами в корне будет работать везде
sed -i 's|../../||g' *.html

# 3. ИНТЕГРАЦИЯ РУМЫНСКОГО РЕЕСТРА В index.html
# Добавляем кнопку "PROBE DIGITALE (RO)" в верхнюю панель или блок векторов
sed -i '/<div class="vector-card"/i \
    <div class="vector-card" style="border-left: 5px solid var(--gold); background: #1a1607; margin-bottom: 1.5rem;"> \
        <h3 style="color: var(--gold);">🇷🇴 LISTĂ DE PROBE DIGITALE (ROMÂNĂ)</h3> \
        <p>Registrul oficial al probelor pentru instanțele din Republica Moldova.</p> \
        <a href="LISTA_PROBE_DIGITALE.html" class="btn" style="border-color: var(--gold); color: var(--gold);">DESCHIDE LISTA</a> \
    </div>' index.html

# 4. ТЕСТ: Ищем любые забытые .md файлы в ссылках по всему проекту
echo "=== ПОИСК ОШИБОК (.md) ==="
grep -r "\.md" . --include="*.html"

# 5. ТЕСТ: Ищем битые пути (../)
echo "=== ПОИСК БИТЫХ ПУТЕЙ (../) ==="
grep -r "\.\./" . --include="*.html"

# 6. ФИНАЛЬНЫЙ ПУШ ИДЕАЛЬНОЙ СТРУКТУРЫ
git add .
git commit -m "fix(404): global link purge and Romanian registry integration [v.2.9]"
git push origin master
=== ПОИСК ОШИБОК (.md) ===
./apostille-legal-case-optimized.html:        <a class="btn btn-primary btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md">
./apostille-legal-case-optimized.html:        <a class="liability-card" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/DULCA_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="liability-card" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/MURIANU_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="liability-card" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/NANTOI_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="btn btn-danger btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/NANTOI_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="btn btn-ghost btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/DULCA_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="btn btn-ghost btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/MURIANU_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="btn btn-danger" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md">
./apostille-legal-case-optimized.html:        <a class="dl-item" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_EN.md">
./apostille-legal-case-optimized.html:        <a class="dl-item" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_FR.md">
./apostille-legal-case-optimized.html:        <a class="dl-item" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md">
./apostille-legal-case-optimized.html:        <a class="btn btn-danger" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/NANTOI_NOTICE.md">
./apostille-legal-case-optimized.html:        <a class="btn btn-primary btn-lg" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_EN.md" target="_blank">
./docs/claim/en.html:fetch('en.md')
./docs/claim/ro.html:fetch('ro.md')
./docs/claim/ru.html:fetch('ru.md')
./jus-cogens-proof-macheret.html:    <a class="btn btn-gold btn-lg" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">⚖ АКТ ДЕКОНСТРУКЦИИ (РУ)</a>
./jus-cogens-proof-macheret.html:    <a class="btn btn-gold btn-lg" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">⚖ ACT DE DECONSTRUCȚIE</a>
./jus-cogens-proof-macheret.html:    <a class="btn btn-gold btn-lg" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_EN.md" target="_blank">⚖ DECONSTRUCTION ACT (EN)</a>
./jus-cogens-proof-macheret.html:    <a class="btn btn-gold btn-lg" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_FR.md" target="_blank">⚖ ACTE DE DÉCONSTRUCTION (FR)</a>
./liability-nodes.html:    <a class="btn btn-red btn-block" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">
./liability-nodes.html:        <a class="btn btn-blue btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/DULCA_NOTICE.md" target="_blank">
./liability-nodes.html:        <a class="btn btn-blue btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/MURIANU_NOTICE.md" target="_blank">
./liability-nodes.html:        <a class="btn btn-red btn-block" href="https://arhiv1973b.github.io/apostille-legal-case/docs/liability/NANTOI_NOTICE.md" target="_blank">
./liability-nodes.html:          <a class="btn btn-yellow btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">
./liability-nodes.html:          <a class="btn btn-blue btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_EN.md" target="_blank">
./liability-nodes.html:          <a class="btn btn-ghost btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_FR.md" target="_blank">
./liability-nodes.html:        <a class="btn btn-yellow btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">
./liability-nodes.html:        <a class="btn btn-purple btn-sm" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">
./liability-nodes.html:      <a class="btn btn-red" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">
./liability-nodes.html:      <a class="btn btn-blue" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_EN.md" target="_blank">
./liability-nodes.html:      <a class="btn btn-ghost" href="https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_FR.md" target="_blank">
./NANTOI_NOTICE.html:      <a class="dl-item" href="docs/forensics/FORGERY_DECONSTRUCTION_ACT.md" target="_blank">🇷🇺 АКТ (РУ)</a>
./NANTOI_NOTICE.html:      <a class="dl-item" href="docs/forensics/FORGERY_DECONSTRUCTION_EN.md" target="_blank">🇬🇧 ENGLISH (UN)</a>
./NANTOI_NOTICE.html:      <a class="dl-item" href="docs/forensics/FORGERY_DECONSTRUCTION_FR.md" target="_blank">🇫🇷 FRANÇAIS (EU)</a>
./NANTOI_NOTICE.html:  const t=`PERSONAL LIABILITY NOTICE — НАНТОЙ ЛЮДМИЛА — ГНС РМ\nCASE-MACHERET-1997-2026\nSTATUS: PERPETRATOR / INTERPOL READY\nПодлог личности Маркова И.М. 15.03.2022. Ст.361 УК РМ + Identity Theft.\nАКТ ДЕКОНСТРУКЦИИ: https://arhiv1973b.github.io/apostille-legal-case/docs/forensics/FORGERY_DECONSTRUCTION_ACT.md\nURL: https://arhiv1973b.github.io/apostille-legal-case/docs/liability/NANTOI_NOTICE.html`;
./PRESS_KIT.html:        <a href="./docs/media/media_fact_sheet_v1.md" class="btn">OPEN MEDIA FACT-SHEET</a>
=== ПОИСК БИТЫХ ПУТЕЙ (../) ===
./docs/claim/en.html:  <a href="../../index.html">← Главная</a>
./docs/claim/ro.html:  <a href="../../index.html">← Главная</a>
./docs/claim/ru.html:  <a href="../../index.html">← Главная</a>
[master 16db534] fix(404): global link purge and Romanian registry integration [v.2.9]
 12 files changed, 54 insertions(+), 39 deletions(-)
Enumerating objects: 27, done.
Counting objects: 100% (27/27), done.
Delta compression using up to 4 threads
Compressing objects: 100% (14/14), done.
Writing objects: 100% (14/14), 1.56 KiB | 114.00 KiB/s, done.
Total 14 (delta 13), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (13/13), completed with 13 local objects.
To https://github.com/arhiv1973b/apostille-legal-case.git
   11c8a05..16db534  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. МАССОВАЯ ЗАМЕНА АБСОЛЮТНЫХ И ОТНОСИТЕЛЬНЫХ ПУТЕЙ
# Мы заменяем всю цепочку /docs/forensics/FILE.md на FILE.html
find . -name "*.html" -exec sed -i 's|https://arhiv1973b\.github\.io/apostille-legal-case/docs/forensics/||g' {} +
find . -name "*.html" -exec sed -i 's|https://arhiv1973b\.github\.io/apostille-legal-case/docs/liability/||g' {} +
find . -name "*.html" -exec sed -i 's|docs/forensics/||g' {} +
find . -name "*.html" -exec sed -i 's|docs/liability/||g' {} +

# 3. ЗАМЕНА РАСШИРЕНИЙ
# Все ссылки на .md превращаем в .html
find . -name "*.html" -exec sed -i 's/\.md/.html/g' {} +

# 4. СПЕЦИАЛЬНЫЙ ПАТЧ для docs/claim/ (возвращаем им выход на уровень вверх)
# Так как они лежат глубже, им нужно ../../index.html
sed -i 's|index\.html|../../index.html|g' docs/claim/*.html

# 5. КОНТРОЛЬНЫЙ ТЕСТ (Должно быть пусто или только внешние ресурсы)
echo "=== ФИНАЛЬНЫЙ ТЕСТ НА ОШИБКИ (.md) ==="
grep -r "\.md" . --include="*.html" | grep -v "node_modules"

# 6. ФИНАЛЬНЫЙ ПУШ ИДЕАЛЬНОЙ СИСТЕМЫ
git add .
git commit -m "fix(404): absolute link reconstruction and satellite file sync [v.3.0]"
git push origin master
=== ФИНАЛЬНЫЙ ТЕСТ НА ОШИБКИ (.md) ===
[master 96522af] fix(404): absolute link reconstruction and satellite file sync [v.3.0]
 13 files changed, 60 insertions(+), 60 deletions(-)
Enumerating objects: 33, done.
Counting objects: 100% (33/33), done.
Delta compression using up to 4 threads
Compressing objects: 100% (17/17), done.
Writing objects: 100% (17/17), 1.83 KiB | 133.00 KiB/s, done.
Total 17 (delta 16), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (16/16), completed with 16 local objects.
To https://github.com/arhiv1973b/apostille-legal-case.git
   16db534..96522af  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. Создание файла эскалации ULTIMATUM_INTERPOL_PROTOCOL.html
cat << 'EOF' > ULTIMATUM_INTERPOL_PROTOCOL.html
<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ULTIMATUM: GLOBAL ESCALATION PROTOCOL — CASE-MACHERET-1997-2026</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050505; --panel: #0a0a0a; --border: #330000;
    --accent: #ff0000; --gold: #f0c040; --text: #e0e0e0;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; padding: 20px; line-height: 1.6; }
  .protocol-wrap { max-width: 1000px; margin: 0 auto; border: 2px solid var(--accent); background: var(--panel); padding: 40px; box-shadow: 0 0 20px rgba(255,0,0,0.2); }
  h1 { font-family: 'Orbitron', sans-serif; color: var(--accent); text-align: center; letter-spacing: 3px; border-bottom: 2px solid var(--accent); padding-bottom: 20px; }
  .lang-section { margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
  h2 { color: var(--gold); font-family: 'Orbitron', sans-serif; font-size: 1.2rem; }
  .legal-chain { background: #110000; padding: 15px; border: 1px dashed var(--accent); margin: 15px 0; font-family: 'Share Tech Mono', monospace; }
  .btn-back { display: inline-block; margin-top: 20px; color: var(--gold); text-decoration: none; border: 1px solid var(--gold); padding: 10px 20px; }
</style>
</head>
<body>
<div class="protocol-wrap">
  <h1>ULTIMATUM: GLOBAL ESCALATION</h1>
  <p style="text-align:center; font-weight:bold;">CASE-MACHERET-1997-2026 | JUS COGENS PRIORITY</p>

  <div class="lang-section">
    <h2>🇷🇴 ROMÂNĂ: SOMATIA JURIDICĂ (SECTOR CENTRU / INTERPOL)</h2>
    <p>Instanța (Sectorul Centru) și organele de stat ale RM sunt obligate să solicite intervenția INTERPOL. Refuzul constituie:</p>
    <div class="legal-chain">
      1. Violarea Art. 17 din Statutul de la Roma (Incapacitatea sistemului național).<br>
      2. Încălcarea Art. 6 din Acordul de Asociere UE-RM.<br>
      3. Audit direct al legislației naționale (Art. 405-407).
    </div>
  </div>

  <div class="lang-section">
    <h2>🇷🇺 РУССКИЙ: ПРОТОКОЛ ПРИНУДИТЕЛЬНОЙ ЭСКАЛАЦИИ</h2>
    <p>В случае отказа Суда и госорганов Молдовы от запроса в Интерпол, инициируется механизм декомпрессии:</p>
    <div class="legal-chain">
      - Передача Соглашения в МС ООН по факту отсутствия реагирования ЕС.<br>
      - Нарушение Устава ООН влечет активацию Спец Протокола ООН.<br>
git push origin master
[master 70c4ee3] legal(escalation): deploy Vector 15 - Global Ultimatum Protocol (UN/Rome Statute) [v.3.1]
 1 file changed, 63 insertions(+)
 create mode 100644 ULTIMATUM_INTERPOL_PROTOCOL.html
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 2.24 KiB | 152.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/arhiv1973b/apostille-legal-case.git
   96522af..70c4ee3  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. Создание файла LEGAL_AUDIT_AGREEMENT.html
cat << 'EOF' > LEGAL_AUDIT_AGREEMENT.html
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LEGAL AUDIT: ARTICLES 6, 405, 407 — CASE-MACHERET-1997-2026</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #030a0f; --panel: #071624; --border: #0e3a5c;
    --accent: #00c6ff; --red: #ff2244; --gold: #f0c040; --text: #c8e0f0;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; margin: 0; padding: 20px; }
  .vault-wrap { max-width: 1000px; margin: 0 auto; border: 1px solid var(--border); background: var(--panel); padding: 40px; box-shadow: 0 0 30px rgba(0,198,255,0.1); }
  h1 { font-family: 'Orbitron', sans-serif; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 10px; text-transform: uppercase; }

  /* NATO SEARCH BOX */
  .audit-search { background: #000; border: 1px solid var(--gold); padding: 20px; margin: 20px 0; border-radius: 4px; }
  .search-label { color: var(--gold); font-family: 'Share Tech Mono', monospace; font-size: 0.9rem; margin-bottom: 10px; display: block; }
  .search-trigger { color: #fff; background: #330000; padding: 10px; font-weight: bold; border-left: 4px solid var(--red); }

  .lang-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
  .lang-block { border-left: 3px solid var(--accent); padding-left: 15px; background: rgba(0,0,0,0.2); padding-bottom: 10px; }
  h2 { font-family: 'Orbitron', sans-serif; font-size: 1rem; color: var(--gold); margin-top: 15px; }
  p { font-size: 0.95rem; line-height: 1.5; margin-bottom: 10px; }
  .btn-back { display: inline-block; margin-top: 30px; color: var(--accent); text-decoration: none; border: 1px solid var(--accent); padding: 10px 20px; font-weight: bold; }
  .btn-back:hover { background: var(--accent); color: #000; }
</style>
</head>
<body>
<div class="vault-wrap">
  <h1>Audit Protocol: Legal Instruments</h1>

  <div class="audit-search">
    <span class="search-label">КООРДИНАЦИОННЫЙ ОРГАН АУДИТА — ПОИСКОВЫЙ ТРИГГЕР:</span>
    <div class="search-trigger">КЛЮЧЕВОЕ СЛОВО: NATO (NORTH ATLANTIC TREATY ORGANIZATION) — SECURITY COMPLIANCE ACTIVE</div>
  </div>

  <p>Этот анализ подтверждает юридическую взаимосвязь между отказом национальных органов в международном сотрудничестве (Интерпол) и запуском механизмов международного принуждения.</p>

  <div class="lang-grid">
    <div class="lang-block">
git push origin master
[master 43aafcd] legal(audit): deploy literal agreement audit nodes - Vector 16 (NATO/UN sync) [v.3.2]
 1 file changed, 78 insertions(+)
 create mode 100644 LEGAL_AUDIT_AGREEMENT.html
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 2.85 KiB | 182.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/arhiv1973b/apostille-legal-case.git
   70c4ee3..43aafcd  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. Создание файла NATO_AUDIT_COORDINATION.html
cat << 'EOF' > NATO_AUDIT_COORDINATION.html
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NATO AUDIT COORDINATION — ARTICLES 6, 405, 407</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #020508; --panel: #0a1118; --border: #1a2a3a;
    --accent: #00c6ff; --red: #ff2244; --gold: #f0c040; --text: #c8e0f0;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; margin: 0; padding: 20px; }
  .audit-shell { max-width: 1100px; margin: 0 auto; border: 2px solid var(--border); background: var(--panel); padding: 40px; position: relative; overflow: hidden; }

  /* NATO SEARCH INTERFACE */
  .search-console { background: #000; border: 1px solid var(--accent); padding: 15px; margin-bottom: 30px; display: flex; align-items: center; }
  .search-label { color: var(--accent); font-family: 'Share Tech Mono', monospace; margin-right: 15px; }
  .search-input { background: #111; border: none; color: var(--gold); font-family: 'Share Tech Mono', monospace; font-size: 1.2rem; flex-grow: 1; outline: none; }
  .search-status { color: var(--red); font-weight: bold; margin-left: 15px; animation: blink 1s infinite; }

  @keyframes blink { 50% { opacity: 0; } }

  h1 { font-family: 'Orbitron', sans-serif; text-transform: uppercase; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 10px; }

  .agreement-page { background: rgba(255,255,255,0.03); border: 1px solid #222; padding: 25px; margin-top: 20px; border-left: 4px solid var(--gold); }
  .page-number { float: right; color: var(--gold); font-family: 'Share Tech Mono', monospace; }
  h2 { font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: var(--gold); margin-bottom: 15px; }
  .literal-text { font-family: 'Share Tech Mono', monospace; font-size: 0.95rem; line-height: 1.6; color: #fff; white-space: pre-wrap; }

  .enforcement-box { border: 1px solid var(--red); background: rgba(50,0,0,0.3); padding: 20px; margin-top: 30px; }
  .btn-back { display: inline-block; margin-top: 20px; color: var(--accent); text-decoration: none; border: 1px solid var(--accent); padding: 10px 20px; font-weight: bold; }
</style>
</head>
<body>
<div class="audit-shell">
  <div class="search-console">
    <span class="search-label">КООРДИНАЦИОННЫЙ ОРГАН АУДИТА > ПОИСК:</span>
    <span class="search-input">NATO / SECURITY COMPLIANCE / ART 407 AUDIT</span>
    <span class="search-status">ACTIVE MONITORING</span>
  </div>

git push origin master
[master 76c69f4] legal(nato): deploy Vector 17 - Coordination Audit Body (Literal Agreement) [v.3.3]
 1 file changed, 74 insertions(+)
 create mode 100644 NATO_AUDIT_COORDINATION.html
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 2.61 KiB | 116.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/arhiv1973b/apostille-legal-case.git
   43aafcd..76c69f4  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. ПАТЧ index.html: Добавление официального линка в блок Интерпола
# Мы обновляем кнопку и добавляем под ней прямую ссылку на контакты Интерпола
sed -i 's|ПЕРЕДАТЬ В INTERPOL / PG|КРИМИНАЛИСТИЧЕСКИЙ ОТЧЕТ (INTERPOL)|g' index.html
sed -i '/КРИМИНАЛИСТИЧЕСКИЙ ОТЧЕТ (INTERPOL)/a \
        <a href="https://www.interpol.int/en/Contacts/Contact-INTERPOL" target="_blank" class="btn" style="border-color: var(--accent); color: var(--accent); font-size: 0.8rem; margin-top
: 5px; display: block;">WWW.INTERPOL.INT/CONTACTS</a>' index.html

# 3. ПАТЧ Актов деконструкции (RU/EN/FR): Добавление блока "REPORT TO INTERPOL"
# Вставляем блок официальной связи перед футером во все 3 версии
for file in FORGERY_DECONSTRUCTION_ACT.html FORGERY_DECONSTRUCTION_EN.html FORGERY_DECONSTRUCTION_FR.html; do
  sed -i '/<div class="footer"/i \
    <div style="margin-top:50px; border: 1px solid var(--red); padding: 20px; background: rgba(255,0,0,0.05);"> \
      <h3 style="color:var(--red); font-family:Orbitron,sans-serif;">OFFICIAL REPORTING CHANNEL / CANAL OFICIAL</h3> \
      <p style="margin: 10px 0;">Use the link below to submit this Forensic Deconstruction Act to INTERPOL General Secretariat:</p> \
      <a href="https://www.interpol.int/en/Contacts/Contact-INTERPOL" target="_blank" style="color:var(--accent); font-weight:bold; text-decoration:underline;">GO TO OFFICIAL INTERPOL CON
TACT FORM</a> \
    </div>' "$file"
done

# 4. ФИНАЛЬНЫЙ ПУШ И ВАЛИДАЦИЯ
git add .
git commit -m "fix(interpol): integrate verified contact nodes and official reporting links [v.3.4]"
git push origin master
[master 8e3541b] fix(interpol): integrate verified contact nodes and official reporting links [v.3.4]
 4 files changed, 17 insertions(+), 1 deletion(-)
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 4 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 1.81 KiB | 115.00 KiB/s, done.
Total 6 (delta 5), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (5/5), completed with 4 local objects.
To https://github.com/arhiv1973b/apostille-legal-case.git
   76c69f4..8e3541b  master -> master
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. ГЛОБАЛЬНАЯ ЗАМЕНА: Исправляем невалидный домен на официальный
# Ищем и заменяем по всему проекту во всех HTML файлах
find . -name "*.html" -exec sed -i 's|www\.interpol\.icontacts|https://www.interpol.int/en/Contacts/Contact-INTERPOL|g' {} +
find . -name "*.html" -exec sed -i 's|interpol\.icontacts|https://www.interpol.int/en/Contacts/Contact-INTERPOL|g' {} +

# 3. ТОЧЕЧНОЕ ИСПРАВЛЕНИЕ КНОПКИ В index.html
# Проверяем основной блок Интерпола и прописываем верный href
sed -i 's|href="[^"]*interpol\.icontacts[^"]*"|href="https://www.interpol.int/en/Contacts/Contact-INTERPOL"|g' index.html

# 4. ОБНОВЛЕНИЕ ТЕКСТА КНОПОК (для ясности)
# Заменяем технический текст на функциональный заголовок
sed -i 's|WWW.INTERPOL.ICONTACTS|REPORT TO INTERPOL (OFFICIAL)|g' *.html

# 5. ПРОВЕРКА — ищем остатки битой ссылки
echo "=== ПРОВЕРКА ОСТАТКОВ ICONTACTS ==="
grep -r "icontacts" .

# 6. ФИНАЛЬНЫЙ ПУШ
git add .
git commit -m "fix(interpol): repair broken links and restore official contact gateway [v.3.5]"
git push origin master
=== ПРОВЕРКА ОСТАТКОВ ICONTACTS ===
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
Everything up-to-date
arhiv@Ator:/mnt/c/Users/arhiv/apostille-legal-case$ # 1. Заход в корень проекта
cd /mnt/c/Users/arhiv/apostille-legal-case/

# 2. Создание узла связи с МУС - ICC_COMMUNICATION_BRIDGE.html
cat << 'EOF' > ICC_COMMUNICATION_BRIDGE.html
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ICC COMMUNICATION BRIDGE — ART. 17 ROME STATUTE</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root { --bg: #050505; --accent: #00c6ff; --red: #ff2244; --text: #e0e0e0; }
  body { background: var(--bg); color: var(--text); font-family: 'Share Tech Mono', monospace; padding: 40px; }
  .bridge-wrap { max-width: 900px; margin: 0 auto; border: 1px solid var(--accent); padding: 30px; background: rgba(0,0,0,0.8); }
  h1 { font-family: 'Orbitron', sans-serif; color: var(--accent); border-bottom: 2px solid var(--accent); }
  .status-404 { color: var(--red); font-weight: bold; font-size: 1.2rem; margin: 20px 0; }
  .logic-chain { border-left: 3px solid var(--red); padding-left: 20px; margin: 20px 0; }
  .btn-link { display: inline-block; padding: 10px 20px; border: 1px solid var(--accent); color: var(--accent); text-decoration: none; margin-top: 20px; }
</style>
</head>
<body>
<div class="bridge-wrap">
  <h1>ICC PROXY NODE: COMPLEMENTARITY</h1>
  <div class="status-404">STATUS: SYSTEMIC SILENCE (OFFICIAL PORTAL 404)</div>
  <p>Запрошенная страница на портале МУС может быть недоступна по причине отсутствия официальной юрисдикционной реакции национальных органов Молдовы.</p>

  <div class="logic-chain">
    <h3>ЮРИДИЧЕСКАЯ ТРАЕКТОРИЯ:</h3>
    <p>1. Отказ Суда сектор Центр (Молдова) в доступе к правосудию.</p>
    <p>2. Активация <strong>Статьи 17 Римского статута</strong> (Принцип комплементарности).</p>
    <p>3. Подача через OTP (Office of the Prosecutor) — переход дела в международную юрисдикцию.</p>
  </div>

  <p>Для официальной подачи рапорта используйте действующий шлюз OTP:</p>
  <a href="https://www.icc-cpi.int/about/otp/how-the-otp-works" target="_blank" class="btn-link">OFFICIAL ICC OTP PORTAL</a>
  <br>
  <a href="index.html" class="btn-link" style="border-color:#555; color:#555;">⌂ ВЕРНУТЬСЯ В VAULT</a>
</div>
</body>
</html>
