#!/usr/bin/env python3
"""Sinh lại examples/sample-usage.json với timestamp "còn sống".

File JSON mẫu là snapshot tĩnh nên sau vài giờ `ompagy --input` sẽ báo
STALE và các cột "reset" sẽ âm. Chạy lại script này để làm mới:

    python3 examples/make_sample.py

Dữ liệu trong file mẫu là dữ liệu GIẢ LẬP (email example.com), không
chứa tài khoản thật.
"""

from __future__ import annotations

import json
import os
import time

HOUR = 3600_000
DAY = 24 * HOUR
NOW = int(time.time() * 1000)

PREFIX = "google-antigravity"


def limit(vendor: str, model: str, window: str, label: str, used: float,
          resets_in: int, status: str = "ok") -> dict:
    return {
        "id": f"{PREFIX}:{vendor}:default:{model}-{window}",
        "label": label,
        "scope": {
            "provider": PREFIX,
            "projectId": "aicode-consumers",
            "windowId": window,
            "shared": model.startswith("3p"),
        },
        "window": {
            "id": window,
            "label": window.upper(),
            "durationMs": DAY if window == "5h" else 7 * DAY,
            "resetsAt": NOW + resets_in,
        },
        "amount": {
            "unit": "percent",
            "remainingFraction": (100 - used) / 100,
            "usedFraction": used / 100,
            "remaining": 100 - used,
            "used": used,
            "limit": 100,
        },
        "status": status,
    }


def account(email: str, used_g5: float, used_g1w: float, used_s5: float,
            used_s1w: float, extra: bool = False) -> dict:
    limits = [
        limit("google", "gemini", "5h", "Gemini 5h", used_g5, 4 * HOUR + 50 * 60_000),
        limit("google", "gemini", "weekly", "Gemini Weekly", used_g1w, 2 * DAY + 6 * HOUR),
        limit("anthropic", "3p", "5h", "Claude & GPT (shared)", used_s5, 4 * HOUR + 55 * 60_000),
        limit("openai", "3p", "weekly", "Claude & GPT (shared)", used_s1w, 20 * HOUR),
    ]
    if extra:
        # Meter lạ (gemini-pro-5h) -> ompagy đưa vào mục "OTHER METERS",
        # không tính vào score.
        limits.append(
            limit("google", "gemini-pro", "5h", "Gemini Pro 5h", 12.5, 9 * HOUR)
        )
    return {
        "provider": PREFIX,
        "fetchedAt": NOW - 30_000,
        "metadata": {
            "endpoint": "https://daily-cloudcode-pa.googleapis.com",
            "projectId": "aicode-consumers",
            "email": email,
        },
        "limits": limits,
    }


def main() -> None:
    payload = {
        "generatedAt": NOW,
        "reports": [
            account("alice@example.com", 2.0, 9.1, 0.0, 65.9, extra=True),
            account("bob@example.com", 16.2, 56.1, 0.0, 51.9),
            account("carol@example.com", 0.0, 99.5, 0.0, 51.9),
        ],
        "accountsWithoutUsage": [],
        "disabledCredentials": [],
        "capacity": {
            PREFIX: [
                {"window": "5h", "durationMs": 5 * HOUR, "accounts": 3,
                 "usedAccounts": 0.3, "remainingAccounts": 2.7},
                {"window": "7d", "durationMs": 7 * DAY, "accounts": 3,
                 "usedAccounts": 2.1, "remainingAccounts": 0.9},
            ]
        },
    }
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample-usage.json")
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
