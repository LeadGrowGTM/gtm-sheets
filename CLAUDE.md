# gtm-sheets

LeadGrow GTM Sheets — rowbound fork configured for Sheets-native enrichment, people-finding, and copy generation.

## What This Is

Parallel path to the orchestrator for cases where company data is already normalized and you need enrichment, people-finding, and copy without spinning up the full Python pipeline.

Three-sheet model:
- **companies** — normalized company data + enrichment waterfall outputs (tech stack, signals, homepage email, etc.)
- **people** — AI Ark people-finding outputs + email waterfall (Icypeas → LeadMagic → MillionVerifier)
- **copy** — AI copy generation with variable resolution per lead row

## Commands

```bash
npm install          # install deps
npm run build        # compile TypeScript
npm run dev          # run CLI in dev mode (tsx, no compile)
gtm-sheets run       # run enrichment pipeline
gtm-sheets status    # pipeline status
```

## Config Files

Configs live in `configs/`. One JSON file per sheet type:

| File | Sheet type | Purpose |
|------|------------|---------|
| `configs/companies.json` | companies tab | Enrichment waterfall: tech stack, signals, homepage email, etc. |
| `configs/people.json` | people tab | AI Ark people-finding + email waterfall |
| `configs/copy.json` | copy tab | Claude AI copy gen + variable resolution |

Config schema: rowbound v2 `PipelineConfig` with `tabs` key. See `src/core/types.ts`.

## Stack

- Runtime: Node.js ≥22, TypeScript
- Package manager: npm (rowbound upstream convention)
- Auth: gws CLI for Google Sheets (`mitchell@leadgrow.ai`)
- AI actions: Claude Haiku 4.5 via `claude -p --bare`
- Shell actions: ai-ark CLI, spider-agent, lg-llm-runtime

## Upstream

Forked from `eliasstravik/rowbound` v1.7.3 (MIT). Core engine untouched — all LeadGrow customization lives in `configs/`.
