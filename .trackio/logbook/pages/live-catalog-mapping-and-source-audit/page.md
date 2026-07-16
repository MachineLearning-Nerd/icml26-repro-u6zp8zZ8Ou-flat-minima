# Live catalog mapping and source audit


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_febaac435ab1", "created_at": "2026-07-16T15:30:25+00:00", "title": "Four live claims mapped to the current PDF numbering"}
-->
# The four live-card claims are all addressed

The challenge's live `claims_anchored.json` and the automatic judge's three `claims.json` entries are both snapshotted in the artifact. The live card's final theorem numbers are shifted relative to the current arXiv PDF, so this logbook maps substance rather than silently repeating the drift.

| Live claim | Challenge wording anchor | Current PDF/source anchor | Evidence here |
|---:|---|---|---|
| 1 | Theorem 1 | PDF Theorem 1; `technical_arxiv.tex` line 6 | 576 exact SA-ERM certificates + 16,384 event trials |
| 2 | Theorems 2 and 3 | PDF Theorems 2 and 3; lines 57 and 93 | exact SAER=8/T + 1,984 exact suffix risks |
| 3 | catalog says Theorems 4 and 5 | substance is PDF Theorems 5 and 6; lines 157 and 178 | all SAM suffix empirical risks 0 + exact r^2/2 sharpness gap |
| 4 | catalog says Theorems 6 and 8 | lower is PDF Theorem 7, upper is PDF Theorem 8; lines 186 and 217 | 80 full SAM runs/4,800 suffixes + r^2T exponent audit |

## Primary-source identity

- PDF SHA-256 `47e2027051f0d411a657057374cb9b2095430f8dae0114c13763b04e6d50fa24` (34 pages)
- arXiv tar SHA-256 `1729d0cb3ef302e51a29805d78ddbdacf7552314b0b88e9655eb7623d1490da5`
- `main_arxiv.tex` SHA-256 `b529ee384983eddf8299a29e4ca4ed774654e7f571aa0951116eddc8e98b6145` (1196 lines)
- `technical_arxiv.tex` SHA-256 `2c52c89cf224faa91158baec5c94d47466f55f93e71bec787a612abd72665a9e` (238 lines)

PDF pages 7-11 were rendered and visually inspected; all relevant theorem statements and equations are legible. The source snapshot contains no official executable code, so the implementation is clean-room NumPy from the displayed equations.

## Source inconsistencies preserved, not exploited

- Theorem 1 defines the good sharp point as `rho e_d`; its proof's final display prints `rho e_I`. We evaluate the defined extra-coordinate point.
- Theorem 3 opens with (-1, 1) samples but later has a (0, 1) typo. The run uses signs, as its ReLU dynamics require.
- The final Theorem 3 proof display loses a square after the preceding squared bound. Reported risks are recomputed from the exact population expression.
- The SAM proof uses 2^n blocks of length T plus one trigger coordinate; the run allocates `2^n T+1` coordinates.

These notes narrow the audit trail; they do not change any reported claim result.
