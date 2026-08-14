# Handoff for AI Agent

## Exact file path for the agent
- `C:\Users\arhiv\.copilot\session-state\e4960773-80ae-4bc5-97e2-45e432513833\files\handshake_for_agent.md`

## Only-for-agent instructions
1. Read `H:\ACTOR_DEV_ENV\copilot-worktrees\apostille-mirror\arhiv1973b-supreme-pancake\release_case_macheret_2026.md` first.
2. Do not rewrite the already completed English intro or the English commit-style summary.
3. Do not repeat work that is already complete.
4. Do not attempt deployment until the deployment target and secrets are explicitly confirmed.
5. Continue from the existing branch state only if a real target-specific change is required.

## What is already done
- The public release document is already in the repo.
- The release intro is already expanded and translated to English.
- The commit-style summary at the top is already in English.
- The branch `arhiv1973b-public-release-case-macheret-2026` is already pushed to `origin`.
- The existing PR for this branch was already created and merged earlier.
- The handoff section was already added to `release_case_macheret_2026.md`.

## What was deliberately not done
- No deployment was performed.
- No secret placeholders were added.
- No repo-wide restructuring was applied in this worktree.

## Handoff points where the agent can take over and later return the baton
1. Review the release document at `H:\ACTOR_DEV_ENV\copilot-worktrees\apostille-mirror\arhiv1973b-supreme-pancake\release_case_macheret_2026.md`.
2. Confirm the deployment target:
   - Docker registry
   - GitHub Actions workflow
   - server or VM
   - local container run
3. Confirm the runtime inputs:
   - registry credentials
   - workflow secrets
   - deployment host and path
   - network and socket access
4. If a target is confirmed, add only target-specific instructions or a dedicated deployment section.
5. If the target is not confirmed, stop and return the baton without mutating the repo.

## Suggested next action for the agent
- Add a deployment section or a target-specific instruction file only after the target is confirmed.
- Build the workflow around the already-pushed release branch without recreating the release text.
