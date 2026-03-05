# Project Policy

## Language
- All documents and code comments must be written in English

## Commit Convention
- Commit message format: `<type>: <description>`
- Type examples: `docs`, `feat`, `fix`, `refactor`, `chore`, `style`, `test`
- Do not include internal process terms (e.g., "cycle") in commit messages
- Single line only, no bullet point details

## Reference Document
- `docs/PROJECT_SPEC.md` is the single source of truth for the project
- All task progress must be checked against this document
- Original document content must not be summarized or modified

## Prompt Engineering
- Crafting high-quality prompts is critical to the success of this project
- Prompts must be precise, well-structured, and tested to ensure reliable LLM outputs
- Small models require especially clear and constrained prompts to produce correct results

## Project Structure
- Reference and policy documents go in the `docs/` folder
- Remove unnecessary files; keep only the spec document
