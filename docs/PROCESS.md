# Project Process

## Iterative Development Cycle

All work follows a repeating cycle anchored to `docs/PROJECT_SPEC.md` as the absolute reference.

### Cycle Phases

```
Plan → Evaluate Plan → Implement → Evaluate Implementation → Test → Spec Validation → (repeat)
```

#### Phase 1: Plan
- Review `PROJECT_SPEC.md` requirements for the target task(s)
- Design the implementation approach
- Define acceptance criteria based on the spec

#### Phase 2: Evaluate Plan
- Verify the plan fully covers spec requirements
- Identify gaps, risks, or deviations from the spec
- Revise the plan before moving to implementation

#### Phase 3: Implement
- Write code following the approved plan
- Adhere to file names, outputs, and structure defined in the spec

#### Phase 4: Evaluate Implementation
- Test the implementation against spec requirements
- Check outputs, file names, data formats, and behavior
- Document any issues or deviations found

#### Phase 5: Test
- **Default: Smoke test** (lightweight, fast)
  - Verify already-executed outputs (file existence, size, structure)
  - For LLM-dependent tasks, test with 2-3 items only to validate logic
  - Check data integrity (JSON structure, DB schema, column names)
  - Do NOT re-run full pipelines or process all data
- **Full test**: Only when explicitly requested by the user
  - Run all scripts end-to-end with full dataset
  - Validate complete outputs and edge cases
  - User will provide specific instructions for full test scope

#### Phase 6: Spec Validation
- Cross-check every requirement in `PROJECT_SPEC.md` for the target task
- Verify: correct file names, output names, data fields, and expected behavior
- Mark each spec requirement as PASS or FAIL
- If any FAIL exists, the task is not complete

#### Repeat
- Feed test results and spec validation findings back into the next cycle
- Fix issues, refine, and iterate until all spec requirements PASS

## Core Principles

- **Spec is absolute**: `PROJECT_SPEC.md` is the single source of truth. No deviation allowed.
- **No assumptions**: If the spec defines it, follow it exactly. If unclear, clarify before proceeding.
- **Incremental progress**: Each iteration should produce a measurable improvement validated against the spec.
- **Evaluation-driven**: Every implementation must be evaluated before moving forward.
