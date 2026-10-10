---
type: Reference
title: OKF Spec v0.2
description: Open Knowledge Format — markdown + YAML bundle spec.
tags: [okf, spec]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: okf-spec
    resource: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
    title: OKF SPEC.md v0.2
---

# OKF v0.2

Bundle = directory of markdown concepts. `type` required; `title/description/resource/tags/sources/generated/verified/status` optional. Reserved `index.md` / `log.md`. Links = graph. Conformance: parseable YAML + non-empty `type`.
