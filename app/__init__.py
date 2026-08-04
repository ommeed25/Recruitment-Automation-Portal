from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_REAL_APP = _ROOT.parent / "linkedin_integration" / "app"

__path__ = [str(_ROOT), str(_REAL_APP)]
