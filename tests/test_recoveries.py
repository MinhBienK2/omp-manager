#!/usr/bin/env python3
"""Regression tests cho omp-manager (chỉ dùng stdlib).

Chạy:
    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "omp-manager")

HOUR = 3600_000
NOW = 1_700_000_000_000


def load_module():
    spec = importlib.util.spec_from_loader(
        "omp_manager", importlib.machinery.SourceFileLoader("omp_manager", SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


om = load_module()


def limit(vendor: str, model: str, used: float, resets_in: int, window: str = "5h",
          label: str | None = None) -> dict:
    return {
        "id": f"google-antigravity:{vendor}:default:{model}-{window}",
        "label": label or model,
        "scope": {"provider": "google-antigravity", "projectId": "p", "windowId": window},
        "window": {"id": window, "label": window.upper(), "durationMs": 5 * HOUR,
                   "resetsAt": NOW + resets_in},
        "amount": {"unit": "percent", "remainingFraction": (100 - used) / 100,
                   "usedFraction": used / 100, "remaining": 100 - used,
                   "used": used, "limit": 100},
        "status": "ok",
    }


def payload(limits: list[dict], email: str = "a@example.com") -> dict:
    return {
        "generatedAt": NOW,
        "reports": [{
            "provider": "google-antigravity",
            "fetchedAt": NOW,
            "metadata": {"email": email},
            "limits": limits,
        }],
        "accountsWithoutUsage": [],
        "disabledCredentials": [],
        "capacity": {},
    }


class RecoveriesTest(unittest.TestCase):
    def recover_by_bucket(self, accounts, bucket):
        recs = om.get_recoveries(accounts, NOW)
        return [r for r in recs if r["bucket"] == bucket]

    def test_extra_meter_uses_its_own_reset_time(self):
        """Extra meter phải lấy delta từ chính nó, không từ bucket shared-1w."""
        accounts = om.parse(payload([
            limit("google", "gemini", 3.0, 4 * HOUR),
            limit("anthropic", "3p", 40.0, 20 * HOUR, "weekly"),
            limit("google", "gemini-pro", 12.5, 1 * HOUR, label="Gemini Pro 5h"),
        ]))
        recs = self.recover_by_bucket(accounts, "Gemini Pro 5h")
        self.assertEqual(len(recs), 1)
        rec = recs[0]
        self.assertEqual(rec["delta"], 1 * HOUR)
        self.assertEqual(rec["resetsAt"], NOW + 1 * HOUR)
        # Meter extra reset sớm hơn mọi bucket khác -> phải đứng đầu.
        all_recs = om.get_recoveries(accounts, NOW)
        self.assertEqual(all_recs[0]["bucket"], "Gemini Pro 5h")

    def test_extra_meter_without_shared_weekly_bucket(self):
        """Account chỉ có meter extra (không có shared-1w) không được crash."""
        accounts = om.parse(payload([
            limit("google", "gemini", 3.0, 4 * HOUR),
            limit("google", "gemini-pro", 12.5, 1 * HOUR, label="Gemini Pro 5h"),
        ]))
        recs = self.recover_by_bucket(accounts, "Gemini Pro 5h")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["delta"], 1 * HOUR)

    def test_bucket_recovery_delta(self):
        accounts = om.parse(payload([
            limit("google", "gemini", 3.0, 4 * HOUR),
            limit("anthropic", "3p", 40.0, 20 * HOUR, "weekly"),
        ]))
        recs = self.recover_by_bucket(accounts, "C&G 1W")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["delta"], 20 * HOUR)
        self.assertEqual(recs[0]["recover_pct"], 40.0)


if __name__ == "__main__":
    unittest.main()
