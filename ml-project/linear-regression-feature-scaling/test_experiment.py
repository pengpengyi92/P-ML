import unittest

from experiment import STEPS, TEST, TRAIN, run


class FeatureScalingTests(unittest.TestCase):
    def test_holdout_has_distinct_feature_pairs(self):
        self.assertTrue({row[:2] for row in TRAIN}.isdisjoint(row[:2] for row in TEST))

    def test_ols_is_an_exact_fit(self):
        reference = run()[0]
        self.assertLess(reference.train_mse, 1e-24)
        self.assertLess(reference.test_mse, 1e-24)

    def test_same_rate_diverges_raw_but_converges_scaled(self):
        _, raw, conservative, scaled = run()
        self.assertTrue(raw.diverged)
        self.assertLess(raw.updates, STEPS)
        self.assertFalse(conservative.diverged)
        self.assertGreater(conservative.test_mse, 1.0)
        self.assertFalse(scaled.diverged)
        self.assertLess(scaled.test_mse, 1e-12)


if __name__ == "__main__":
    unittest.main()
