# A©t0r Evidence Vault — CASE-MACHERET-1997-2026
## Инструкция автономного деплоя · Windows + GitHub Pages

---

## БЫСТРЫЙ ДЕПЛОЙ (3 шага)

```powershell
# ШАГ 1: Открыть PowerShell как Администратор, перейти в папку сайта
cd "H:\Загрузки\MACHERET_SITE"   # или куда распакован архив

# ШАГ 2: Установить токен GitHub
# Получить на: https://github.com/settings/tokens → Fine-grained tokens
# Права: Contents (write), Pages (write)
$env:GITHUB_TOKEN = "ghp_ВАШТОКЕН"

# ШАГ 3: Запустить автодеплой
Set-ExecutionPolicy Bypass -Scope Process
.\DEPLOY.ps1
```

Сайт будет доступен через ~2 минуты:
**https://arhiv1973b.github.io/apostille-mirror/**

---

## СТРУКТУРА САЙТА

```
MACHERET_SITE/
├── index.html                    ← Главная страница
├── pages/
│   ├── apostille-registry.html   ← Реестр 97 апостилей (с поиском)
│   ├── jus-cogens.html           ← Jus Cogens доказательный акт (4 языка)
│   ├── timeline.html             ← Хронология 1997-2026
│   ├── evidence.html             ← Доказательства
│   └── pledoarie.html            ← Pledoarie Finală
├── assets/
│   ├── css/main.css              ← Design system
│   ├── js/                       ← Скрипты
│   └── data/
│       ├── apostilles.json       ← 97 записей реестра
│       ├── integrity.json        ← SHA-256 + статус (автообновление)
│       └── robot_qa_log.json     ← Лог ответов робота
├── docker-compose.yml            ← Автономный стек (offline)
├── docker/
│   ├── nginx.conf                ← Веб-сервер конфиг
│   └── robot/
│       ├── Dockerfile
│       └── robot.py              ← Автономный ИИ-агент (Ollama)
├── actor_protocol_test.py        ← Тест-сюит A©t0r Protocol
├── DEPLOY.ps1                    ← PowerShell автодеплой
└── .github/workflows/deploy.yml  ← GitHub Actions CI/CD
```

---

## НАСТРОЙКА GITHUB РЕПОЗИТОРИЯ

### 1. Создать репозиторий
```
Имя: apostille-mirror
Email аккаунт: arhiv1973b@outlook.com
Тип: Public
```

### 2. Включить GitHub Pages
```
Settings → Pages → Source: GitHub Actions
```

### 3. Добавить секреты (опционально)
```
Settings → Secrets → Actions:
ACTOR_GPG_PASS = <ваш GPG пароль>
```

---

## АВТОНОМНЫЙ РЕЖИМ (без интернета)

```powershell
# Запуск всего стека локально
docker-compose up -d

# Проверка
docker-compose ps

# Сайт доступен на: http://localhost:8080
# Ollama API: http://localhost:11434
```

### Загрузка моделей Ollama (CPU, без GPU)
```bash
# Qwen 2.5 7B — рекомендуется для CPU
ollama pull qwen2.5:7b

# DeepSeek-V3 (требует ≥16GB RAM)
ollama pull deepseek-v3

# Llama 3.1 8B — хороший баланс
ollama pull llama3.1:8b
```

---

## ТЕСТ-СЮИТ

```bash
# Запуск проверки целостности
python3 actor_protocol_test.py

# Ожидаемый результат:
# ✅ 27+ прошли
# ❌ 3 провалены (это ДОКУМЕНТАЦИЯ МОШЕННИЧЕСТВА, не ошибки кода)
# ⚠️  3 предупреждения (требуют действий на стороне государства)
```

---

## GPG ПОДПИСЬ

```powershell
# Генерация ключа (если не существует)
gpg --batch --gen-key gpg-params.txt

# Экспорт публичного ключа (для GitHub)
gpg --armor --export arhiv1973b@outlook.com

# Настройка Git
git config --global commit.gpgsign true
git config --global user.signingkey <KEY_ID>
```

---

## КОНФИГУРАЦИЯ OLLAMA (без GPU/NVIDIA)

```yaml
# В docker-compose.yml уже настроен CPU режим
# Для лучшей производительности:
environment:
  - OLLAMA_NUM_THREADS=8          # число CPU потоков
  - OLLAMA_MAX_LOADED_MODELS=1    # одна модель в памяти
```

---

## БЕЗОПАСНОСТЬ СЕКРЕТОВ

```powershell
# Никогда не коммитить токены в git
# Использовать переменные окружения:
$env:GITHUB_TOKEN = "..."     # удаляется при закрытии PowerShell
$env:ACTOR_GPG_PASS = "..."

# Или Windows Credential Manager:
cmdkey /add:github.com /user:arhiv1973b /pass:<TOKEN>
```

---

## МОНИТОРИНГ

GitHub Actions автоматически:
- Обновляет счётчик дней каждые 6 часов
- Пересчитывает SHA-256 при каждом push
- Верифицирует целостность архива
- Деплоит на GitHub Pages

---

**CASE-MACHERET-1997-2026 · A©tor · ИДНП 2000001159655**  
**JUS COGENS · ERGA OMNES · МУС СТ.17 · БЕЗ СРОКА ДАВНОСТИ**  
**arhiv1973b.github.io/apostille-mirror**
