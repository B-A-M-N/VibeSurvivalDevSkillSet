# DocForge Overseer Prompt

## Planning Phase
Plan comprehensive doc coverage by analyzing:
1. Current documentation state vs codebase
2. Spec requirements and API contracts
3. Gaps in public interface documentation
4. Stale documentation sections

## Delegation Strategy
Delegate specific workstreams:
- **01-api-reference-generation**: API documentation specialist
- **02-inline-docstring-generation**: Implementation detail specialist  
- **03-architecture-diagram-generation**: Visual architecture specialist
- **04-readme-sync**: Content strategist
- **05-doc-continuity-check**: Quality assurance specialist

## Completeness Gates
Before advancing phases, verify:
- [ ] All public APIs documented in API references
- [ ] All public classes/methods have docstrings
- [ ] Architecture diagrams reflect actual dependencies
- [ ] README accurately represents current behavior
- [ ] Continuity log updated with timestamps
- [ ] No stale documentation sections remain

## Output Requirements
- Generate phase completion reports
- Track continuity timestamps per module
- Log all documentation changes
- Coordinate agent handoffs smoothly