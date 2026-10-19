import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_frontend_and_backend_analytics_events_match():
    backend_source = (ROOT / "backend/app/routes_analytics.py").read_text(encoding="utf-8-sig")
    events_assignment = next(
        (
            node.value
            for node in ast.parse(backend_source).body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "VALID_EVENTS" for target in node.targets)
        ),
        None,
    )
    assert events_assignment is not None, "Backend VALID_EVENTS declaration is missing"
    backend_events = set(ast.literal_eval(events_assignment))

    frontend_source = (ROOT / "static/analytics.js").read_text(encoding="utf-8-sig")
    match = re.search(r"\b(?:const|let|var)\s+VALID_EVENTS\s*=\s*\[([^\]]*)\]", frontend_source)
    assert match is not None, "Frontend VALID_EVENTS declaration is missing"
    frontend_events = set(re.findall(r"['\"]([a-z0-9_]+)['\"]", match.group(1)))

    assert backend_events == frontend_events, (
        f"Backend-only analytics events: {sorted(backend_events - frontend_events)}; "
        f"frontend-only analytics events: {sorted(frontend_events - backend_events)}"
    )
