# Next.js 15 + SQLite SaaS CLAUDE.md Template

This PR adds an opinionated `CLAUDE.md` for a greenfield SaaS built with Next.js 15 App Router and SQLite.

## Setup in 3 steps

1. Copy the template into your project root:
   ```bash
   cp templates/nextjs-sqlite/CLAUDE.md ./CLAUDE.md
   ```
2. Adjust the package manager command names only if your `package.json` differs.
3. Ask Claude Code to read `CLAUDE.md` before making changes.

## Why this template is opinionated

It chooses a small, boring architecture: Server Components by default, route handlers as thin adapters, service/repository layers for business logic, and explicit SQL migrations.

The goal is to stop Claude Code from asking generic structure questions and to prevent common SaaS mistakes: SQL string interpolation, client-side auth trust, mutable old migrations, unbounded list queries, and vague utility modules.

## Manual validation

I validated the template by checking it against a minimal Next.js 15 + SQLite project shape and confirming it answers the usual first-context questions without extra clarification:

- where routes, services, repos, migrations, and components go
- how database migrations are named and applied
- what commands to run before completion
- what security and anti-pattern rules to follow
