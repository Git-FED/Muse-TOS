# Terms of Service Scanner

Check the rules and terms of service **before you act**. This scanner is an add-on module for `terms-of-service-tracker/`: it reads the tracker's saved snapshots, compares one user-named action against the written rules, and gives one of four verdicts.

## Verdicts

- **CLEAR** — the action matches the written rules cited by the scan.
- **CONFLICT** — the action breaks a written rule; the conflicting rule is quoted.
- **CONTRADICTION** — a human instruction conflicts with the written rules; both are quoted and the written rule wins.
- **UNCHECKED** — the rules could not be fetched or verified. This is never a silent pass.

Written rules are the only authority. A person saying “go ahead” never overrides the written rules. The rule text comes from the tracker's snapshots; if a platform has no snapshot, the scan must say UNCHECKED rather than guess.

Read [setup](docs/SCANNER-SETUP.md) and [day-to-day usage](docs/SCANNER-USAGE.md) next.

**Advise only:** this module never posts, emails, or contacts a platform on your behalf without a separate explicit order. Do not invent platforms, actions, rules, or verdicts. Missing information is unavailable and results in UNCHECKED where verification is required.
