"""Answer HTML sanitizer (frozen per user Q&A freeze).

Pipeline: html.escape everything, then linkify only well-formed [PMC\\d+]
tokens to Europe PMC. Never mark raw LLM output |safe. GATE/CONFLICT markers
are stripped by safety/detector before this step; any residue stays escaped.
"""

from __future__ import annotations

import html as _html
import re as _re

_PMC_RE = _re.compile(r"\[(PMC\d+)\]")

_EPMC_URL = "https://europepmc.org/articles/{pmcid}"


def escape_and_linkify(text: str, allowed: set[str] | None = None) -> str:
    """Escape text then linkify [PMCID] tokens.

    allowed=None links every well-formed token; otherwise only tokens in
    allowed become links, others stay escaped text (fail closed, no invented
    link target).
    """
    escaped = _html.escape(text or "", quote=True)

    def _sub(m: _re.Match) -> str:
        pmcid = m.group(1)
        if allowed is not None and pmcid not in allowed:
            return m.group(0)
        url = _EPMC_URL.format(pmcid=pmcid)
        return f'<a href="{url}">[{pmcid}]</a>'

    return _PMC_RE.sub(_sub, escaped)
