#!/usr/bin/env python3
"""Unit tests cho token formatting và token tracking logic của omp-manager."""

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


class TokenTest(unittest.TestCase):
    def test_fmt_token_num(self):
        self.assertEqual(om.fmt_token_num(450), "450")
        self.assertEqual(om.fmt_token_num(1200), "1.2k")
        self.assertEqual(om.fmt_token_num(15_400_000), "15.4M")
        self.assertEqual(om.fmt_token_num(2_500_000_000), "2.50B")


if __name__ == "__main__":
    unittest.main()
