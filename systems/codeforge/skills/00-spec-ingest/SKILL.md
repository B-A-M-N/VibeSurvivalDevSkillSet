---
name: spec-ingest
description: Parses MASTER_SPEC.md to extract contracts, data models, API specs, state machines, invariants, and hard gates.
---

## Steps to Read and Parse MASTER_SPEC.md

1. **Locate the Master Spec**: Find `MASTER_SPEC.md` at the repository root or in the `specs/` directory.
2. **Load and Validate**: Ensure the file exists and is well-formed YAML/Markdown with clear section delimiters.
3. **Extract Contracts**: Identify all top-level contract definitions, including service boundaries, data ownership, and SLA requirements.
4. **Extract Data Models**: Parse type definitions, field constraints, default values, and relationships (one-to-one, one-to-many, references).
5. **Extract API Specifications**: Document endpoints, HTTP methods, request/response schemas, authentication schemes, and rate limits.
6. **Extract State Machines**: Map states, transitions, triggers, and guards for each entity or workflow.
7. **Extract Invariants**: List rules that must hold true globally (e.g., "balance >= 0", "unique email per user").
8. **Extract Hard Gates**: Identify non-negotiable constraints (e.g., "GDPR compliance required", "encryption at rest mandatory").
9. **Normalize and Reference**: Assign unique IDs to each extracted element for cross-referencing.
10. **Generate SPEC_SUMMARY.md**: Produce a structured summary with sections for contracts, models, APIs, state machines, invariants, and hard gates.

## Output Specification

The output `SPEC_SUMMARY.md` should contain:
- A table of contents for quick navigation.
- A `## Contracts` section summarizing each contract with key fields.
- A `## Data Models` section with schema definitions and constraints.
- A `## API Specifications` section detailing endpoints and contracts.
- A `## State Machines` section visualizing or tabulating state transitions.
- A `## Invariants` section listing all global invariants with references.
- A `## Hard Gates` section outlining mandatory constraints and compliance requirements.

## Best Practices

- Use consistent identifiers (e.g., `SPEC-001`, `MODEL-002`).
- Include line references from the original MASTER_SPEC.md for traceability.
- Keep summaries concise but complete; link to detailed sections.
- Validate extracted invariants against the original spec to avoid omissions.
- Update SPEC_SUMMARY.md whenever MASTER_SPEC.md changes.

## Tooling Notes

- Prefer structured parsing (YAML frontmatter or marked sections) over regex.
- Support incremental updates by tracking last parsed position or hash.
- Log parsing errors with line numbers for easy debugging.
- Ensure backward compatibility with older spec versions where possible.