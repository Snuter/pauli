# P.A.U.L.I. — User-Journey Concept
Patient-centered AI for Understanding Literature and Insights

See also: `concept-technical.md` for implementation.

## 1. Vision & who it is for

Make Open Access science from Europe PMC queryable by patients in plain
language, without hallucination, with care for critical information.

Primary user: person living with a chronic / rare condition (e.g. ME/CFS,
fatigue, post-exertional malaise / PEM) tracking research over time.

Non-goals: diagnosis, treatment recommendation, symptom triage. Research
information only, not medical advice.

## 2. Guiding principles (patient lens)

- Low energy / brain fog: short answers, save-for-later, Simple mode by default.
- Uncertainty: show what is known / unknown / in whom it was studied.
- Trust: every factual claim has a citation back to Europe PMC. No invented details.
- Honesty: system states when it does not know.
- Safety: gated trigger warnings before critical content.
- Continuity: follow topics, see what is new, print a 1-page summary for doctor visits.

## 3. Journey 1 — Onboarding with your own buzzwords

1. You enter 1–5 buzzwords for your condition.
   Example: `myalgic encephalomyelitis`, `PEM`.
2. The app checks each term against Europe PMC and tells you if a term is
   empty, too short, or too broad (>50k hits), with a hint to narrow it down.
3. For a valid topic the app fetches ~500 matching Open Access papers once,
   then lets you ask questions over them.

No built-in default topics — your library starts from what you enter.

## 4. Journey 2 — Asking a question

1. You ask in chat, e.g. `What triggers PEM?`
2. You get a short answer (<150 words) with every fact linked to a Europe PMC
   paper `[PMCID]`.
3. If your saved papers do not contain an answer, you get an honest unknown
   instead of a guess:
   `I don't know from your saved papers — [what is missing, what term to add,
   what to ask your doctor]`.
4. The app distinguishes:
   - no papers cached yet,
   - papers cached but no answer in them,
   - papers that conflict with each other.

## 5. Journey 3 — Standard / Simple language

Toggle: `Standard / Simple`. Same papers and citations, different wording.

- Standard: grade 8–10, keeps term + short definition,
  e.g. `post-exertional malaise (crash after effort)`.
- Simple (default for first answer): grade 5–6, sentences <15 words, expands
  all acronyms, uses glossary (`PEM -> crash after effort`), adds a
  `What this means:` line.

Simplification never adds new facts.

## 6. Journey 4 — Sensitive topics stay gated

Categories that trigger a gate: prognosis/mortality, suicidality, severe
disability, pregnancy/children, medical trauma, PEM crash risk.

1. Before showing details you see a blurred card:
   `This answer contains [category] — Show / Skip / Why am I seeing this?`
2. Nothing reveals without your click. Simple mode uses gentler wording.
3. Every gated answer also shows `Research info only, not medical advice`,
   plus local crisis resources where relevant.
4. You can set sensitivity locally: `low / standard / hide details`.

## 7. Journey 5 — Tracking & doctor visit

- Follow topics. A `Check for new papers` button shows e.g.
  `3 new papers since 2026-09-30`.
- Weekly manual digest in plain language.
- Personal library: save answers/papers for later (low-energy friendly).
- Doctor export: 1-page Markdown/PDF with question, short answer, citations,
  unknowns, and suggested questions for your doctor.

## 8. What good looks like (user view)

- Answers are short and readable in the chosen mode.
- Warning gate always appears before sensitive details, in both modes.
- Unknowns are explicit and tell you what to do next.
- Sync shows only what is new, no repeats.
- Printout fits one page for a visit.
