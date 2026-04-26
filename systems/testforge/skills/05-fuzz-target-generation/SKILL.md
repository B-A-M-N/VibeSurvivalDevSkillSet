---
name: 05-fuzz-target-generation
description: Generate fuzz targets for input validation, boundary conditions
---

# skill 5 — Fuzz Target Generation

**Trigger**: fuzz-priority entries from test_matrix.json and uncovered boundary conditions.

## Step-by-step instructions
1. Identify functions/API endpoints that accept external input.
2. Create seed corpus from SCENARIOS values and spec examples.
3. Define dictionary entries, max_length, and validity constraints.
4. Instrument code for coverage-guided fuzzing (e.g., afl, libFuzzer, or foundry fuzz).
5. Write a fuzz target harness that calls the target with mutated inputs.
6. Output as `fuzz_targets/<target>.fuzz` and register in test_manifest.json.
7. Configure fuzzing parameters (iterations, timeout, corpus size).
8. Implement proper crash detection and classification.
9. Set up persistent storage for interesting corpus.
10. Validate fuzz targets against spec requirements.

## Fuzz Target Categories
- **Input validation fuzzing**: Invalid type, format, size
- **Boundary fuzzing**: Min/max values, edge cases
- **Type confusion fuzzing**: Type mismatch scenarios
- **State fuzzing**: Invalid state transitions
- **Format fuzzing**: Malformed structured data

## Output Structure
```
tests/
├── fuzz_targets/
│   ├── token_fuzz.target
│   ├── voting_fuzz.target
│   └── utils_fuzz.target
├── test_manifest.json
└── fuzz_stats.json
```

## Fuzz Target Format (Solidity example)
```solidity
contract TokenFuzz {
    function fuzz_transfer(bytes calldata data) public {
        vm.assume(data.length > 0 && data.length < 10000);
        // Parse data as transfer parameters
        (address to, uint256 amount) = abi.decode(data, (address, uint256));
        token.transfer(to, amount);
    }
}
```

## Fuzz Configuration
```json
{
  "fuzz_target": "token_fuzz",
  "iterations": 1000000,
  "timeout": 3600,
  "corpus_size": 10000,
  "dictionary": ["0x00", "0xff", "valid_address", "max_uint256"],
  "coverage_threshold": 0.85
}
```

## Seed Corpus Generation
- Extract values from SCENARIOS.md
- Include spec examples and edge cases
- Use real-world transaction data patterns
- Generate minimal failing inputs
- Create diverse input variations

## test_manifest.json Fuzz Section
```json
{
  "fuzz_targets": [
    {
      "target_id": "transfer-fuzz-001",
      "file": "tests/fuzz_targets/token_fuzz.target",
      "function": "fuzz_transfer",
      "iterations": 1000000,
      "timeout": 3600,
      "seed_count": 100,
      "coverage_target": 0.85
    }
  ]
}
```

## Coverage-Guided Fuzzing
- Track coverage during fuzzing sessions
- Prioritize inputs that increase coverage
- Detect and classify crashes
- Generate regression tests from findings
- Update seed corpus with new findings

## Integration Points
Consumes test_matrix.json from skill 01.
Complements unit (skill 02), kill (skill 03), and integration (skill 04) tests.
Outputs to tests/fuzz_targets/ directory.
Updates test_manifest.json with fuzz target registrations.
Provides input for skill 06 coverage validation.

## Best Practices
- Start with small, focused fuzzing campaigns
- Monitor coverage growth over time
- Classify and triage crashes by severity
- Maintain seed corpus evolution
- Balance fuzzing time across targets
- Use invariants as oracle for correctness