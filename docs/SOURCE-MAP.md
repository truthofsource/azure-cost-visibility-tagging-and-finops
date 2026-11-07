# Source and Public Adaptations

Actual platform source includes the workbook builder, saved-view helper, governance module, budget notifications, common tags and VM shutdown schedule. [Original hashes](source-map.json) precede public organization/subscription/resource substitutions. No private invoice, actual recipient, secret, state or Git history is included.

The public cost-controls root extracts the actual budget block, turns its surrounding subscription/budget binding into example inputs and adds a default-Off creation flag. It calls the copied governance module conditionally and exposes the actual seven-key tagging pattern as an example output. It does not tag every existing resource or recreate environment state.

The governance child module is copied behavior, including enforcement disabled. Mock tests are new public checks. The full production policy and isolated VM schedule remain context references with omitted owning-root dependencies; they are not standalone deployments.

The local budget-percentage/tag-gap/shutdown helpers, fictional data, tests and reference viewer are new demonstration code. The Logic App template is a new disabled, Compose-only design derived from the deferred allowlist/recovery requirement. It is not represented as a previously implemented executor.

The actual workbook builder retains its missing `criticality` key so the public test can expose the source gap. Live saved-view operations are not executed; tests use its actual view-body builder and fake responses. Source extraction and local checks are not a fresh Azure bill, compliance scan or service-state inventory.
