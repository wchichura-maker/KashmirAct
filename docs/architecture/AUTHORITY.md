# Authority hierarchy

Conflicts are resolved in this order:

1. Explicit and most recent project decisions
2. Foundation document (`docs/foundation/KashmirAct_Fundacao_v0.1.md`)
3. P0 specification (`docs/p0/KashmirAct_Prototype0_Specification_v0.1.md`)
4. Technical planning documents
5. Implementation documentation
6. Existing code
7. Technical inference
8. Agent preference

Rules:

- Do not replace a project decision because another architecture looks more elegant.
- Do not silently turn a provisional decision into a final one.
- Do not invent requirements absent from the documents.
- If a real conflict exists: record it, preserve both facts, choose only when authority is sufficient.

This file records the hierarchy. It does not outrank the Foundation or the P0 spec.
