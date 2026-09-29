import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_feed(self):
        state = core.new_game()
        self.assertTrue(core.feed(state, 1, 10))
        self.assertFalse(core.feed(state, 1, 10))

    def test_02_tank_capacity(self):
        state = core.new_game()
        state["tank_load"] = 90
        result = core.feed(state, 2, 20)
        self.assertFalse(result)

    def test_03_temp_boundary(self):
        state = core.new_game()
        self.assertEqual(core.check_temp(state, 35), "over")

    def test_04_cancel_releases_tank(self):
        state = core.new_game()
        core.feed(state, 1, 10)
        core.cancel_ferment(state, 1)
        self.assertEqual(state["tank_load"], 0)

    def test_05_inspect_failure_refunds(self):
        state = core.new_game()
        core.feed(state, 1, 10)
        state["batches"][1]["defect"] = True
        before = state["ingredient"]
        result = core.inspect(state, 1)
        self.assertFalse(result)
        self.assertEqual(state["ingredient"], before + 10)

    def test_06_no_output_on_fault(self):
        state = core.new_game()
        state["cold_fault"] = True
        result = core.output(state, 5)
        self.assertFalse(result)

    def test_07_holiday_once(self):
        state = core.new_game()
        state["batches"] = {1: {"amount": 0, "defect": False}}
        core.holiday(state)
        self.assertEqual(state["batches"][1]["amount"], 10)

    def test_08_load_preserves_batch(self):
        state = core.new_game()
        state["batch_id"] = 5
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["batch_id"], 5)


if __name__ == "__main__":
    unittest.main()
