# Debug 04 — nome acessível no seletor de arquivos

- **Encontrado por:** `test_every_form_control_has_label_or_accessible_name`
- **Sintoma:** o `input[type=file]` era acionável pela dropzone, mas não possuía nome acessível próprio.
- **Causa:** o texto descritivo estava associado à dropzone, não ao controle oculto.
- **Correção:** inclusão de `aria-label="Selecionar arquivos XML ou ZIP"`.
- **Regressão:** teste estático exige label, ancestral `label` ou nome ARIA para todo controle.
