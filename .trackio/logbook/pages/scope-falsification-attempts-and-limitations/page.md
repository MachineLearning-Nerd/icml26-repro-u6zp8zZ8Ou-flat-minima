# Scope, falsification attempts, and limitations


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_2e4113c01d68", "created_at": "2026-07-16T15:30:26+00:00", "title": "What the finite evidence does and does not establish"}
-->
# Scope boundaries

- **Existential worst cases, not typical behavior.** The paper itself studies worst-case constructed SCO instances. These runs verify those finite instances and do not assert SA-GD or SAM usually generalizes poorly.
- **Finite certificates, not a replacement proof.** Exact identities are checked through T=1,024 for SA-GD and full SAM dynamics through T=128. Scaling supports the asymptotic forms; the universal quantifiers remain the paper's theorem.
- **Conditional runs are paired with unconditional event trials.** Dataset acceptance is used only after separately measuring the event probability and matching its exact formula. Attempts and seeds are retained.
- **Tie-breaking is part of the SA-GD construction.** The claim is existential. We verify the displayed maximizer attains the exact inner maximum; we do not claim all tie-breakers follow the same path.
- **SAM zero-gradient convention is disclosed.** The 1D sharpness example uses the source proof's no-op convention at gradient zero. The separate population-risk construction has a nonzero trigger gradient at initialization.
- **Stability is order-level.** Theorem 8 matches the r^2T dependence but is looser in eta (and beta normalization). No unknown big-O constant is inferred from finite data.
- **Source snapshot has no code.** There is no official implementation to import or benchmark. The complete clean-room equations, raw rows and tests are in the artifact.

# Prespecified attempts to remove each effect

1. SA-ERM rho=1 (outside rho<=1/2): population separation collapses to zero.
2. SA-GD r=rho: update and population risk collapse to zero.
3. SA-GD rho-threshold violation: population risk collapses to zero.
4. SAM sharpness r=0: SAER gap collapses to zero.
5. SAM lower bound: both fixed-r and saturated schedules are retained, so a single favorable radius schedule cannot determine the conclusion.

No row, seed, suffix, or failed boundary was filtered from the public outputs.
