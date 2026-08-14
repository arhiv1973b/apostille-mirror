# 🚀 Gemini CLI Docker + OpenCode MCP Integration

## Быстрый старт

### 1. Запуск контейнера
```bash
$env:PATH += ";C:\Program Files\Docker\Docker\resources\bin"
docker-compose -f "F:\Мой диск\docker-compose.yml" up -d
```

### 2. Интерактивный доступ к контейнеру
```bash
docker exec -it gemini-cli bash
```

### 3. Запуск MCP сервера (для OpenCode)
```bash
cd H:\ACTOR_DEV_ENV
node mcp-server-gemini.js
```

### 4. Запуск OpenCode с MCP
```bash
opencode --mini
```

## 📁 Структура

- **Контейнер**: `gemini-cli` (us-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.1.1)
- **Рабочая директория**: `/mnt/my_disk` (смонтирована из `F:\Мой диск`)
- **MCP Server**: http://localhost:3001
- **Git репозиторий**: https://github.com/arhiv1973b/apostille-mirror.git

## 🔌 MCP API Endpoints

### Health Check
```bash
curl http://localhost:3001/health
```
**Ответ**: `{"status":"ok","container":"gemini-cli"}`

### Список файлов
```bash
curl http://localhost:3001/files
```

### Выполнение команды в контейнере
```bash
curl -X POST http://localhost:3001/exec \
  -H "Content-Type: application/json" \
  -d '{"command":"ls -la /mnt/my_disk"}'
```

## 📊 Статус контейнера

```bash
docker ps | grep gemini-cli
```

**Ожидаемый результат**:
```
gemini-cli   us-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.1.1   Up 5 minutes
```

## 🐛 Troubleshooting

### MCP сервер не запускается
```bash
# Проверить, запущен ли Node.js
node --version

# Проверить, используется ли порт 3001
netstat -ano | findstr :3001

# Убить процесс на порту 3001
taskkill /PID <PID> /F
```

### Контейнер не видит файлы
```bash
# Проверить монтирование
docker exec gemini-cli ls -la /mnt/my_disk

# Скопировать файлы вручную
docker cp "F:\Мой диск\*.pdf" gemini-cli:/mnt/my_disk/
```

### OpenCode не видит MCP
```bash
# Список подключённых MCP серверов
opencode mcp list

# Добавить MCP сервер вручную
opencode mcp add gemini-cli-docker --url "http://localhost:3001"
```

## 📝 Git Commands

### Посмотреть статус
```bash
cd H:\ACTOR_DEV_ENV
git status
```

### Сделать коммит
```bash
git add .
git commit -m "ваше сообщение"
git push origin sync-approved-portal-20260814
```

## 🔐 Безопасность

- ✅ Контейнер запущен без привилегий
- ✅ MCP сервер доступен только локально (localhost:3001)
- ✅ Файлы Google Drive смонтированы в контейнер безопасно
- ⚠️ Убедитесь, что порт 3001 не открыт публично

## 📞 Контакты

**Репозиторий**: https://github.com/arhiv1973b/apostille-mirror.git
**Ветка**: `sync-approved-portal-20260814`
**Последний аудит**: 2026-08-12

---
*Документ обновлён: 2026-08-12 | MCP Integration v1.0*
