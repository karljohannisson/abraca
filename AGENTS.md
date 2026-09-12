# Agents

This repo is a **product**. The maintainability seed lives in [`.nose/`](.nose/README.md) (dot directory — open it even if a file listing hides it).

Entry: [`.nose/docs/README.md`](.nose/docs/README.md). The human talks ([`.nose/docs/workflow/human.md`](.nose/docs/workflow/human.md)); you write `product/`. Infer unnamed axes.

1. If `product/` is missing, empty, or stale vs the human’s last message: [`.nose/docs/workflow/bootstrap.md`](.nose/docs/workflow/bootstrap.md) then [planning](.nose/docs/workflow/planning.md). Do not write product code until [handoff](.nose/docs/workflow/handoff.md) is true.
2. Always: [`.nose/docs/workflow/agent.md`](.nose/docs/workflow/agent.md)
3. Intent (this software): `product/requirements.md`, `product/axes.yaml`, `product/entry-points.yaml`, `product/probes.md` — you own these files.
4. Then [implementing](.nose/docs/workflow/implementing.md) and [review](.nose/docs/workflow/review.md). Hunt extras and delete them; do not ask the human to classify sites.

Principles: [.nose/docs/principles/README.md](.nose/docs/principles/README.md). Combined \(W\): [.nose/docs/metric.md](.nose/docs/metric.md). At review:

```
PYTHONPATH=.nose python3 -m maintainability
```
