# T001 — …

- depends: []
- requirements: [FR-1]
- encodes: [example]
- uses: []
- authority: { symbol: pkg.example, path: src/pkg/example.py }
- copied_requirements: |
    FR-1: …
- acceptance:
    - …
    - verifies read the authority
    - no extra sites; W gate
- commit: `T001: …`
