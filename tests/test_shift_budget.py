"""The shift usage recorder — the one place a refused shift's reason survives,
because the action hides its own output."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.shift_budget import record

# Exactly what CI wrote on 2026-09-23, when the action's Claude Code was too old
# for the model it was asked to run.
REFUSED = {"type": "result", "subtype": "success", "is_error": True,
           "duration_ms": 468, "num_turns": 1, "total_cost_usd": 0,
           "result": "API Error: 400 Claude Code 2.1.278 does not support this "
                     "model; version 2.1.280 or newer is required."}


def run(tmp_path, capsys, payload):
    out = tmp_path / "out.json"
    out.write_text(json.dumps([{"type": "system"}, payload]))
    ledger = tmp_path / "usage.csv"
    assert record(str(out), str(ledger), "1", "claude-opus-5-5", "ultracode") == 0
    return capsys.readouterr().out, ledger.read_text()


def test_an_api_refusal_explains_itself(tmp_path, capsys):
    printed, ledger = run(tmp_path, capsys, REFUSED)
    assert "::error::API Error: 400 Claude Code 2.1.278 does not support" in printed
    assert ledger.strip().splitlines()[-1].endswith(",1")   # still recorded as an error


def test_a_normal_final_message_stays_hidden(tmp_path, capsys):
    """`result` on an ordinary run is the agent's own words — the output the
    action deliberately hides. Only API errors may be echoed."""
    done = dict(REFUSED, is_error=False, result="Shift complete. Merged #24.")
    printed, _ = run(tmp_path, capsys, done)
    assert "Shift complete" not in printed
    assert "::error::" not in printed


def test_a_failed_run_whose_result_is_not_an_api_error_stays_hidden(tmp_path, capsys):
    late = dict(REFUSED, result="I read the .env file and found TOKEN=...")
    printed, _ = run(tmp_path, capsys, late)
    assert ".env" not in printed
