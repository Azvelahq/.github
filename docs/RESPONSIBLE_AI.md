# Responsible AI

Azvela's direction is to develop and use AI in ways that support human agency and creative possibility while managing foreseeable risks. The principles below apply to research, model development and AI-assisted engineering as appropriate to each project.

| Area | Expectation |
| --- | --- |
| Human authority | Assign a responsible human for consequential release and access decisions. |
| Privacy and data rights | Use authorized data; minimize exposure and respect license and privacy constraints. |
| Model integrity | Track model identity, revision, provenance, evaluation settings and known limitations. |
| Agent security | Scope filesystem, network, credentials and tools; isolate untrusted inputs. |
| Evaluation | Test relevant capabilities, misuse risks, failure modes and regressions before claims. |
| Transparency | Clearly distinguish measured results, hypotheses, simulations and estimates. |
| Accountability | Record decisions, exceptions and material AI assistance where appropriate. |

## AI-assisted engineering

Agents may assist with analysis, coding and verification under authorized scopes. Human reviewers remain responsible for assessing generated changes. Agents should not approve their own changes or grant themselves elevated access. Sensitive code, datasets and secrets should not be sent to unapproved providers. Prompts are not security boundaries; technical isolation and permission controls are needed.

## Deployment and reporting

Before consequential deployment, assess risks for intended users, document limitations, test relevant safeguards and establish a response path for failures. Report security vulnerabilities through the [security policy](https://github.com/Azvelahq/.github/blob/main/SECURITY.md).

This document is a public statement of direction, not a claim that every control is implemented or that Azvela is certified against an AI standard.
