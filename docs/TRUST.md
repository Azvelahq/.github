# Trust and governance

Trust is earned through the relationship between a stated principle, an implemented control, evidence of operation and accountable authority.

## Public and private boundaries

This public repository provides identity, collaboration standards and policy direction. Internal access decisions, incident details, operational risks, production authorization, private research and sensitive evidence belong in appropriately restricted systems. Credentials must not be committed to Git, even in a private repository.

## Assurance language

| State | Meaning |
| --- | --- |
| Proposed | A control or policy has been designed, not verified. |
| Not executed | The relevant evaluation has not run. |
| Inconclusive | Available evidence does not establish an outcome. |
| Technical pass (scoped) | Evidence supports a defined test and environment only. |
| Fail | A requirement was not met. |
| Blocked | Platform, evidence or authority prevents progression. |
| Authorized | The designated authority has approved the stated action. |

A release should require applicable controls, valid evidence, artifact integrity and authorized approval. The policies in this public repository do not implement or enforce that release gate. GitHub plan limits may prevent specific controls from being enforced, especially on private repositories. Never equate policy text with technical enforcement.

## Reference frameworks

These are useful sources for future control design, not certifications or assertions of full compliance:

- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) and [generative AI profile](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [OpenSSF OSPS Baseline](https://baseline.openssf.org/)
- [SLSA](https://slsa.dev/)
- [OWASP SAMM](https://owaspsamm.org/)

See [engineering principles](PRINCIPLES.md) and [responsible AI](RESPONSIBLE_AI.md) for our public expectations.
