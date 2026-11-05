"""The generator must share no code with the detector (rule 3)."""
import ast
from pathlib import Path

SYNTH = Path(__file__).resolve().parents[1] / "synth"


def test_synth_imports_nothing_from_src():
    for path in SYNTH.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                assert not name.split(".")[0] in {"causal_atlas", "src"}, f"{path.name}: {name}"
