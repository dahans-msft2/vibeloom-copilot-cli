"""VibeLoom v0.3 deterministic engine.

Parsing, schema validation, ID registry, contract graph, traces, dispatch,
status. Stdlib only at runtime. The engine never makes semantic judgments.
"""

__version__ = "0.3.0"

# Engine schema version handled per-trace family (see traces.py); package
# version lives here.
