# Adversarial Case Matrix

Build each case from a synthetic posting unless an authorized, frozen corpus exists. Keep expected outcomes independent of scorer output.

| Risk | Minimum challenge | Required observation |
|---|---|---|
| Contradictory requirements | Required license in one section, preferred in another | Conflict is surfaced; no silent eligibility pass |
| Missing compensation | Strong title and duties, no salary | Fit and compensation uncertainty remain separate |
| Remote ambiguity | “Remote” plus mandatory local travel or residence | Commute/location gate follows explicit constraints |
| Title inflation | Executive title with entry-level duties | Evidence outweighs title string |
| Mixed career lanes | Operations leadership plus unrelated technical specialty | Lane uncertainty is exposed or governed |
| Stale posting | Old or internally inconsistent dates | Staleness is flagged without inventing availability |
| Preferred degree | Degree preference mixed with “Scrum Master” wording | Degree preference is independently detected |
| Required degree | Candidate lacks a genuinely mandatory degree | Hard-gate policy is applied exactly as defined |
| Eligibility unknown | Posting omits a decisive requirement | `None` cannot yield Priority/Consider Application |
| Threshold edges | Scores 49.99, 50.00, 64.99, 65.00 | Exact documented boundary behavior |
| Fallback routing | Missing metadata with routable ID prefix | Fallback basis and confidence penalty are visible |
| Misleading keywords | High keyword overlap but unrelated work | False relevance does not dominate evidence |
| Negative evidence | Strong transferable experience plus explicit disqualifier | Disqualifier is not averaged away |
| Duplicate evidence | Same resume fact appears in multiple dimensions | Evidence is not double-counted |
| Empty description | Title only | Manual review or insufficient information |
| Nondeterminism | Same input executed repeatedly | Identical canonical output |

For every case, store the fixture, expected result, rationale, author, creation time, whether the builder saw it, and execution result.
