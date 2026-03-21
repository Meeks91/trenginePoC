"""
Standalone Name Resolution Test Script
=======================================
Manually verifies that resolve_names_via_ddg() resolves known influencer names
to their expected platform handles via a real search client (DDG or Serper).

NOT a pytest test — DDG is unreliable in CI. Run this manually:

    PYTHONPATH="." python scripts/test_nr_resolution.py
    PYTHONPATH="." python scripts/test_nr_resolution.py --client strict --api-key <key>
    PYTHONPATH="." python scripts/test_nr_resolution.py --names "Jeff Nippard" "Alex Leonidas"

Exit codes:
    0 — all expected handles found
    1 — one or more expected handles missing
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.audit.AuditService import AuditLog
from services.extraction.NameResolver import resolve_names_via_ddg
from services.search.OpenSearchClient import OpenSearchClient
from services.search.StrictSearchClient import StrictSearchClient


# Fixtures:

DEFAULT_NAMES: list[str] = [
    "Jeff Nippard",
    "Alex Leonidas",
    "Sean Nalewanyj",
]

# (name_substr, handle_substr, platform) — flexible matching for DDG variance
EXPECTED: list[tuple[str, str, str]] = [
    ("Jeff Nippard", "jeffnippard", "Instagram"),
]

# Fixtures


def _build_client(client_type: str, api_key: str | None) -> OpenSearchClient | StrictSearchClient:
    mock_audit = MagicMock()
    if client_type == "strict":
        if not api_key:
            print("ERROR: --api-key required for --client strict", file=sys.stderr)
            sys.exit(2)
        return StrictSearchClient(mock_audit, api_key=api_key)
    return OpenSearchClient(mock_audit)


def _run(names: list[str], client_type: str, api_key: str | None) -> int:
    client = _build_client(client_type=client_type, api_key=api_key)
    template = client.nr_query_template()

    print(f"\n{'='*60}")
    print(f"  Name Resolution Test  (client={client_type})")
    print(f"  Template: {template}")
    print(f"  Names:    {names}")
    print(f"{'='*60}\n")

    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "nr_test")
        handles = resolve_names_via_ddg(
            names,
            audit,
            search_client=client,
            query_template=template,
            category="Fitness",
        )

    print(f"Resolved {len(handles)} handle(s):")
    for h in handles:
        print(f"  {h.platform:12s}  @{h.handle}  (name={h.name})")

    print()
    failures: list[str] = []
    for name_substr, handle_substr, platform in EXPECTED:
        matched = [
            h for h in handles
            if handle_substr in h.handle.lower() and h.platform == platform
        ]
        if matched:
            print(f"  ✅  '{name_substr}' → @{matched[0].handle} ({platform})")
        else:
            print(f"  ❌  '{name_substr}' → expected handle containing '{handle_substr}' on {platform}, got: {[h.handle for h in handles]}")
            failures.append(name_substr)

    print()
    if failures:
        print(f"FAILED: {len(failures)} expected resolution(s) missing.")
        return 1

    print("PASSED: all expected handles found.")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manual name→handle resolution test")
    parser.add_argument(
        "--names", nargs="+", default=DEFAULT_NAMES,
        help="Names to resolve (default: predefined fitness list)",
    )
    parser.add_argument(
        "--client", choices=["open", "strict"], default="open",
        help="Search client to use (default: open = DuckDuckGo)",
    )
    parser.add_argument(
        "--api-key", default=None,
        help="Serper API key (required for --client strict)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(_run(
        names=args.names,
        client_type=args.client,
        api_key=args.api_key,
    ))
