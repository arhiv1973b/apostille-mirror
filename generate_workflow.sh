#!/bin/bash
mkdir -p .github/workflows
cat << 'INNER_EOF' > .github/workflows/aips-integrity-lock.yml
name: AIPS-2025 Integrity Lock
on: [push, pull_request]
jobs:
  aips-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "AIPS-2025 Active"
INNER_EOF
echo "Workflow generated."
