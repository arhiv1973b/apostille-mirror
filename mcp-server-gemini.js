#!/usr/bin/env node
/**
 * MCP Server for Gemini CLI Docker Container
 * Enables OpenCode to communicate with gemini-cli container
 */

const http = require('http');

// Server configuration
const PORT = 3001;
const CONTAINER_NAME = 'gemini-cli';
const DOCKER_BIN = process.env.DOCKER_BIN || 'docker';

// Helper function to execute Docker commands
function execDockerCommand(cmd) {
  const { execSync } = require('child_process');
  try {
    const result = execSync(`${DOCKER_BIN} exec -i ${CONTAINER_NAME} ${cmd}`, {
      encoding: 'utf-8'
    });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Create HTTP server for MCP
const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;

  // Route handlers
  if (pathname === '/health') {
    res.statusCode = 200;
    res.end(JSON.stringify({ status: 'ok', container: CONTAINER_NAME }));
  } 
  else if (pathname === '/exec' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const { command } = JSON.parse(body);
        const result = execDockerCommand(command);
        res.statusCode = result.success ? 200 : 500;
        res.end(JSON.stringify(result));
      } catch (error) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: error.message }));
      }
    });
  }
  else if (pathname === '/files' && req.method === 'GET') {
    const result = execDockerCommand('ls -la /mnt/my_disk');
    res.statusCode = result.success ? 200 : 500;
    res.end(JSON.stringify(result));
  }
  else {
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(PORT, () => {
  console.log(`MCP Server for gemini-cli listening on port ${PORT}`);
  console.log(`Container: ${CONTAINER_NAME}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
