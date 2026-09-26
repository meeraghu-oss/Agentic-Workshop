- source_spec: `_bmad-output/specs/spec-epic-1/stories/1-triage-decision-schema.md`
  summary: Ignore macOS `.DS_Store` files in repository hygiene rules.
  evidence: An unrelated `.DS_Store` is already untracked and could be included by a broad future add; it predates Story 1 and changing `.gitignore` is outside this story.
