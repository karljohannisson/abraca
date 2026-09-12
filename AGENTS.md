# Agents

This repo is a **product**. The maintainability seed lives in [`.nose/`](.nose/README.md) (dot directory — open it even if a file listing hides it).

1. Always: [.nose/docs/workflow/agent.md](.nose/docs/workflow/agent.md)
2. Intent (this software): `product/requirements.md`, `product/axes.yaml`, `product/entry-points.yaml`, `product/probes.md`
3. If intent is stale vs the human’s last message: [.nose/docs/workflow/planning.md](.nose/docs/workflow/planning.md) before code.
4. Then [.nose/docs/workflow/implementing.md](.nose/docs/workflow/implementing.md) and [.nose/docs/workflow/review.md](.nose/docs/workflow/review.md).

Principles: [.nose/docs/principles/README.md](.nose/docs/principles/README.md). Combined \(W\): [.nose/docs/metric.md](.nose/docs/metric.md). At review:

```
PYTHONPATH=.nose python3 -m maintainability
```

Layout: [.nose/docs/workflow/README.md](.nose/docs/workflow/README.md).
