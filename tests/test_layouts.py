#!/usr/bin/env python3
"""Unit tests cho logic layout adaptive responsive tiers của omp-manager."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "omp-manager")


def load_module():
    spec = importlib.util.spec_from_loader(
        "omp_manager", importlib.machinery.SourceFileLoader("omp_manager", SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


om = load_module()


class LayoutTest(unittest.TestCase):
    def setUp(self):
        self.accounts = [
            {
                "email": "alice_long_name_developer@example.com",
                "score": 92.5,
                "buckets": {
                    "gemini-5h": {"remaining": 98.2, "used": 1.8, "resetsAt": 1700000000000 + 3600000},
                    "gemini-1w": {"remaining": 85.0, "used": 15.0, "resetsAt": 1700000000000 + 86400000},
                    "shared-5h": {"remaining": 100.0, "used": 0.0, "resetsAt": None},
                    "shared-1w": {"remaining": 50.0, "used": 50.0, "resetsAt": 1700000000000 + 7200000},
                },
                "extra": [],
            },
            {
                "email": "bob@example.com",
                "score": 65.0,
                "buckets": {
                    "gemini-5h": {"remaining": 40.0, "used": 60.0, "resetsAt": 1700000000000 + 1800000},
                    "gemini-1w": {"remaining": 30.0, "used": 70.0, "resetsAt": 1700000000000 + 43200000},
                    "shared-5h": {"remaining": 100.0, "used": 0.0, "resetsAt": None},
                    "shared-1w": {"remaining": 20.0, "used": 80.0, "resetsAt": 1700000000000 + 3600000},
                },
                "extra": [],
            },
        ]
        self.now_ms = 1700000000000

    def test_short_email(self):
        long_email = "verylongusernamefordevelopment@example.com"
        shortened = om.short(long_email, max_len=20)
        self.assertLessEqual(len(shortened), 20)
        self.assertTrue("…" in shortened)

        short_email = "bob@test.com"
        self.assertEqual(om.short(short_email, max_len=20), short_email)

    def test_choose_layout_wide(self):
        tier = om.choose_layout(self.accounts, self.now_ms, term_w=160, force="auto")
        self.assertEqual(tier, "full")

    def test_choose_layout_compact(self):
        tier = om.choose_layout(self.accounts, self.now_ms, term_w=105, force="auto")
        self.assertIn(tier, ("compact", "tight", "micro"))

    def test_fit_layout_shrinks_under_tight_width(self):
        fitted = om.fit_layout(self.accounts, self.now_ms, term_w=65, name="micro")
        self.assertLessEqual(fitted["acct"], om.ACCT_MIN)
        self.assertFalse(fitted.get("num", True))

    def test_pct_decimals(self):
        self.assertEqual(om.pct_decimals(self.accounts, pct_w=6), 1)
        self.assertEqual(om.pct_decimals(self.accounts, pct_w=4), 0)


if __name__ == "__main__":
    unittest.main()
