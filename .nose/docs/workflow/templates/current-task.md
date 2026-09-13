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
    - verifies iterate the authority
    - CLI extras none
    - W gate
- commit: `T001: …`
