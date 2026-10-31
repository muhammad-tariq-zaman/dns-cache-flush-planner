import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import classify, plan


class TestFlushPlanner(unittest.TestCase):
    def test_expired(self):
        self.assertEqual(classify(0, 60), "EXPIRED")
        self.assertEqual(classify(-5, 60), "EXPIRED")

    def test_expiring_at_threshold(self):
        self.assertEqual(classify(60, 60), "EXPIRING")

    def test_cached(self):
        self.assertEqual(classify(3600, 60), "CACHED")

    def test_plan_counts(self):
        rows = [{"hostname": "a", "record_type": "A", "ttl_remaining_seconds": "0"},
                {"hostname": "b", "record_type": "AAAA", "ttl_remaining_seconds": "3600"}]
        entries = plan(rows, 60)
        self.assertEqual([e[3] for e in entries], ["EXPIRED", "CACHED"])
