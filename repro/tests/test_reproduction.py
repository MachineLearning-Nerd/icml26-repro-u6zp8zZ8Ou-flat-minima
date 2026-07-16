#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "full"


def load_json(name: str) -> dict:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def load_csv(name: str) -> list[dict]:
    with (OUT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FlatMinimaReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = load_json("summary.json")
        cls.audit = load_json("source_audit.json")

    def test_01_identity_and_exact_claim_snapshot(self) -> None:
        claims = json.loads((ROOT / "repro" / "claims_snapshot.json").read_text())
        self.assertEqual(claims["openreview_id"], "u6zp8zZ8Ou")
        self.assertEqual(claims["arxiv_id"], "2511.03548")
        self.assertEqual(len(claims["automatic_claims"]), 3)
        self.assertEqual(len(claims["live_claims"]), 4)
        self.assertEqual(
            claims["automatic_claims"][0],
            "In non-negative, beta-smooth stochastic convex optimization, flat empirical minima can incur Omega(1) population risk while sharp minima generalize optimally.",
        )

    def test_02_paper_and_source_are_pinned(self) -> None:
        identity = self.audit["identity"]
        self.assertEqual(identity["pdf_sha256"], "47e2027051f0d411a657057374cb9b2095430f8dae0114c13763b04e6d50fa24")
        self.assertEqual(identity["main_tex_sha256"], "b529ee384983eddf8299a29e4ca4ed774654e7f571aa0951116eddc8e98b6145")
        self.assertEqual(identity["technical_tex_sha256"], "2c52c89cf224faa91158baec5c94d47466f55f93e71bec787a612abd72665a9e")
        self.assertEqual(digest(ROOT / "paper" / "2511.03548.pdf"), identity["pdf_sha256"])
        self.assertEqual(self.audit["anchors_1_based"]["theorem_7_sam_lower"]["line"], 186)
        self.assertEqual(self.audit["pdf_visual_audit"]["pages_rendered"], [7, 8, 9, 10, 11])

    def test_03_hard_event_frequencies_match_exact_probabilities(self) -> None:
        rows = load_csv("event_probabilities.csv")
        self.assertEqual({int(r["n"]) for r in rows}, {6, 8, 10, 12})
        self.assertTrue(all(int(r["trials"]) == 4096 for r in rows))
        for row in rows:
            self.assertLess(float(row["abs_error_zero_any"]), 0.03)
            self.assertLess(float(row["abs_error_zero_exact"]), 0.03)
            self.assertLess(float(row["abs_error_one_any"]), 0.03)
            self.assertGreater(float(row["theory_at_least_one"]), 0.63)
            self.assertGreater(float(row["theory_exactly_one"]), 0.36)

    def test_04_saerm_exact_flat_sharp_separation(self) -> None:
        rows = load_csv("saerm_flat_sharp_trials.csv")
        self.assertEqual(len(rows), 576)
        self.assertEqual({int(r["dimension"]) for r in rows}, {65, 257, 1025})
        for row in rows:
            self.assertEqual(float(row["flat_empirical_risk"]), 0.0)
            self.assertAlmostEqual(float(row["flat_saer_exact"]), float(row["global_saer_lower_exact"]), places=14)
            self.assertEqual(float(row["sharp_population_risk_exact"]), 0.0)
            self.assertGreaterEqual(float(row["population_gap_exact"]), 1.0 / 16.0)
            self.assertEqual(row["flat_is_saer_minimizer"], "True")
        self.assertLess(self.summary["claim_1_saerm"]["max_mc_z_score"], 3.5)

    def test_05_sharp_minimum_saturates_smoothness_growth(self) -> None:
        rows = load_csv("saerm_sharpness_certificate.csv")
        self.assertEqual(len(rows), 17)
        for row in rows:
            self.assertAlmostEqual(float(row["saer_growth"]), 0.5 * float(row["delta"]) ** 2, places=14)
            self.assertAlmostEqual(float(row["growth_ratio"]), 1.0, places=14)
            self.assertEqual(float(row["population_risk"]), 0.0)

    def test_06_sagd_all_conditions_and_unit_ball(self) -> None:
        rows = load_csv("sagd_scaling.csv")
        self.assertEqual([int(r["T"]) for r in rows], [64, 128, 256, 512, 1024])
        self.assertTrue(all(r["all_theorem_conditions"] == "True" for r in rows))
        self.assertTrue(all(float(r["max_iterate_norm"]) < 1.0 for r in rows))
        self.assertTrue(all(abs(float(r["lower_condition_eta_gap"]) - float(r["lower_condition_limit"])) < 1e-14 for r in rows))

    def test_07_sagd_saer_is_exactly_order_one_over_T(self) -> None:
        rows = load_csv("sagd_scaling.csv")
        for row in rows:
            self.assertAlmostEqual(float(row["saer_times_T"]), 8.0, places=12)
            self.assertAlmostEqual(float(row["saer_to_upper_ratio"]), 0.125, places=14)
        suffixes = load_csv("sagd_suffix_dynamics.csv")
        self.assertEqual(len(suffixes), 1984)
        self.assertTrue(all(float(r["empirical_risk"]) == 0.0 for r in suffixes))
        self.assertTrue(all(r["rho_flat_certificate"] == "True" for r in suffixes))

    def test_08_sagd_population_risk_is_constant_and_scales_as_lower_bound(self) -> None:
        rows = load_csv("sagd_scaling.csv")
        for row in rows:
            self.assertGreater(float(row["min_suffix_population_risk"]), 0.055)
            self.assertGreater(float(row["min_population_to_lower_scale"]), 0.055)
            self.assertAlmostEqual(float(row["lower_scale_eta2_gap2_T"]), 1.0, places=13)
        values = [float(r["min_suffix_population_risk"]) for r in rows]
        self.assertLess(max(values) - min(values), 0.002)

    def test_09_sagd_boundary_controls_remove_the_gap(self) -> None:
        rows = load_csv("sagd_boundaries.csv")
        self.assertEqual({r["boundary"] for r in rows}, {"r_equals_rho", "rho_threshold_violated"})
        for row in rows:
            self.assertEqual(row["theorem_lower_conditions_hold"], "False")
            self.assertEqual(float(row["max_suffix_population_risk"]), 0.0)

    def test_10_sam_one_dimensional_sharpness_is_exact(self) -> None:
        rows = load_csv("sam_sharpness.csv")
        self.assertEqual(len(rows), 54)
        for row in rows:
            radius = float(row["radius_r"])
            self.assertEqual(float(row["final_w"]), 0.0)
            self.assertEqual(float(row["empirical_risk_final"]), 0.0)
            self.assertAlmostEqual(float(row["sharpness_gap"]), 0.5 * radius**2, places=14)
            if radius > 0:
                self.assertAlmostEqual(float(row["gap_over_r2"]), 0.5, places=14)

    def test_11_full_sam_construction_dynamic_gates(self) -> None:
        rows = load_csv("sam_generalization_runs.csv")
        self.assertEqual(len(rows), 80)
        self.assertEqual({int(r["dimension"]) for r in rows}, {1025, 2049, 4097, 8193})
        self.assertEqual({int(r["dataset_seed"]) for r in rows}, set(range(10)))
        for row in rows:
            self.assertEqual(row["first_update_gate"], "True")
            self.assertEqual(row["chain_gate"], "True")
            self.assertEqual(row["unit_ball_gate"], "True")
            self.assertEqual(row["theorem_radius_condition"], "True")
            self.assertGreater(float(row["initial_gradient_norm"]), 0.0)
            self.assertLess(float(row["max_iterate_norm"]), 0.5)
            self.assertEqual(float(row["wstar_empirical_risk"]), 0.0)
            self.assertEqual(float(row["max_suffix_empirical_risk"]), 0.0)

    def test_12_full_sam_every_suffix_has_nontrivial_lower_certificate(self) -> None:
        suffixes = load_csv("sam_generalization_suffixes.csv")
        self.assertEqual(len(suffixes), 4800)
        self.assertTrue(all(math.isfinite(float(r["population_lower_certificate"])) for r in suffixes))
        self.assertTrue(all(float(r["certificate_to_lower_scale"]) > 0.058 for r in suffixes))
        self.assertTrue(all(float(r["empirical_risk"]) == 0.0 for r in suffixes))
        runs = load_csv("sam_generalization_runs.csv")
        saturated = [r for r in runs if r["regime"] == "saturated_eta_r_sqrtT"]
        self.assertEqual(len(saturated), 40)
        self.assertTrue(all(float(r["min_suffix_population_lower_certificate"]) > 0.014 for r in saturated))
        self.assertTrue(all(abs(float(r["lower_scale_eta2_r2_T"]) - 0.25) < 1e-13 for r in saturated))

    def test_13_stability_upper_matches_r2_T_exponents_with_disclosed_eta_gap(self) -> None:
        rows = load_csv("stability_scaling.csv")
        self.assertEqual(len(rows), 12)
        for row in rows:
            self.assertEqual(int(row["same_r_exponent"]), 2)
            self.assertEqual(int(row["same_T_exponent_before_radius_schedule"]), 1)
            self.assertAlmostEqual(float(row["upper_to_lower_ratio"]), 864.0, places=10)
            self.assertIn("looser", row["interpretation"])
        self.assertIn("nearly matches", self.summary["claim_3_sam"]["stability_scope"])

    def test_14_scope_is_finite_theorem_instance_not_universal_proof(self) -> None:
        scope = self.summary["scope"]
        self.assertTrue(scope["theorem_instances_not_proxy_tasks"])
        self.assertFalse(scope["universal_proof_claimed"])
        self.assertTrue(scope["conditional_event_sampling_disclosed"])
        self.assertFalse(scope["official_code_executed"])
        self.assertIn("No official executable code", self.audit["source_notes"][-1])

    def test_15_cpu_only_no_external_compute(self) -> None:
        env = self.summary["environment"]
        self.assertTrue(env["cpu_only"])
        self.assertFalse(env["gpu_used"])
        self.assertFalse(env["mps_used"])
        self.assertEqual(env["cuda_visible_devices"], "")
        self.assertEqual(env["external_model_calls"], 0)
        self.assertEqual(env["cloud_jobs"], 0)
        self.assertEqual(env["paid_api_calls"], 0)
        self.assertEqual(env["network_calls_during_reproduction"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
