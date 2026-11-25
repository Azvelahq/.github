# Azvela workflow templates

These templates are starter workflows, not universal test engines or release gates. They use a read-only default token, pinned checkout, no persisted checkout credentials, standard hosted runners and bounded execution time.

| Template | Repository contract |
| --- | --- |
| `universal-ci.yml` | A reviewed `Makefile` defines a `ci` target that runs relevant build, tests and static checks. |
| `research-validation.yml` | A reviewed `Makefile` defines `research-validate` with reproducibility checks, evaluation metadata and scoped tests. |

Install only after implementing the target. Missing targets or failing checks must cause a nonzero exit, not a false pass. The selected project owns language/toolchain setup, dependency verification, test coverage, artifact retention and resource budgets. These templates do not provide GPU access or call AI APIs. Do not add secrets or privileged execution to workflows triggered by untrusted pull requests. Review `Makefile` changes as executable code.

The checkout reference is pinned to [v6.1.0](https://github.com/actions/checkout/commit/d23441a48e516b6c34aea4fa41551a30e30af803). Review future updates and keep templates synchronized with the approved revision.
