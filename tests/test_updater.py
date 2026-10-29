#!/usr/bin/env python3
"""Unit tests cho version comparison, config env và dual identity của omp-manager."""

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


class VersionTest(unittest.TestCase):
    def test_parse_version(self):
        self.assertEqual(om.parse_version("1.2.0"), (1, 2, 0))
        self.assertEqual(om.parse_version("v2.0.1"), (2, 0, 1))
        self.assertEqual(om.parse_version("1.10.3"), (1, 10, 3))

    def test_is_newer(self):
        self.assertTrue(om.is_newer("1.2.1", "1.2.0"))
        self.assertTrue(om.is_newer("2.0.0", "1.9.9"))
        self.assertTrue(om.is_newer("1.10.0", "1.9.0"))
        self.assertFalse(om.is_newer("1.2.0", "1.2.0"))
        self.assertFalse(om.is_newer("1.1.9", "1.2.0"))


class ConfigEnvTest(unittest.TestCase):
    def tearDown(self):
        for key in ("OMPAGY_TEST_KEY", "OMP_MANAGER_TEST_KEY", "OMP_MANAGER_TEST_KEY2"):
            os.environ.pop(key, None)

    def test_both_prefixes_are_accepted(self):
        os.environ["OMPAGY_TEST_KEY"] = "from_ompagy"
        self.assertEqual(om.config_env("TEST_KEY"), "from_ompagy")

        os.environ.pop("OMPAGY_TEST_KEY")
        os.environ["OMP_MANAGER_TEST_KEY"] = "from_manager"
        self.assertEqual(om.config_env("TEST_KEY"), "from_manager")

    def test_missing_key_returns_default(self):
        self.assertIsNone(om.config_env("TEST_KEY_MISSING"))
        self.assertEqual(om.config_env("TEST_KEY_MISSING", "fallback"), "fallback")


class DualIdentityTest(unittest.TestCase):
    def test_program_name_is_one_of_the_two(self):
        self.assertIn(om.PROG_NAME, ("omp-manager", "ompagy"))

    def test_cache_dir_is_under_home_cache(self):
        path = om.cache_dir()
        self.assertTrue(path.startswith(os.path.expanduser("~/.cache")))
        self.assertIn(om.PROG_NAME, (os.path.basename(path), "ompagy", "omp-manager"))


if __name__ == "__main__":
    unittest.main()
