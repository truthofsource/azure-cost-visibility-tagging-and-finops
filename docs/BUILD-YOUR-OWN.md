# Build your own from scratch: Azure Cost Visibility Tagging And Finops

Your own tagged Azure lab, budget notifications, cost view and a narrowly scoped optional shutdown design.

Start with a new folder, your own files and your own accounts. The numbered steps below describe the build; no portfolio repository checkout is required. The existing implementation/evidence elsewhere in this repository is a separate reference, not a claim that your new build has already passed.

## Prerequisites

Azure subscription with resource/tag, cost/budget and optional Logic App permissions; an approved notification mailbox and a realistic lab budget. A budget alert is not an automatic spending limit.

Use Bash on Linux/macOS/WSL for Bash blocks and PowerShell for PowerShell blocks. Select the tool versions supported by the official sources below, record the versions you actually install and retain generated dependency locks. Cloud resources, scanner downloads, logs and external AI calls can create costs; review the stated scope before enabling them.

## Create your project folder

Choose a new folder name. These first commands create a blank project; an optional `git init` gives it its own history. Create parent directories in your editor when a later step introduces a nested file.

```bash
mkdir my-azure-cost-visibility-tagging-and-finops
cd my-azure-cost-visibility-tagging-and-finops
git init
```

Create `.gitignore` before saving credentials or build outputs:

```gitignore
.venv/
node_modules/
.env
.env.*
local.settings.json
credentials.json
token.json
*.pem
*.key
*.tfstate*
*.tfplan
.terraform/
private*/
captures/
backups/
batch.json
reports/
out/
app-config.local.yaml
```

The source/file snippets are a starting implementation you type or paste into the named files. Replace `YOUR_*`, names, regions and addresses only with values from your own lab; do not place real client/employee records in a test project. Keep your terminal in this project root unless a step explicitly changes directory.

Before a first commit, set your own repository-local author with `git config user.name "YOUR_NAME"` and `git config user.email "YOUR_PUBLIC_COMMIT_EMAIL"`. Review `git status --short` and the staged diff before publishing; ignored local files are not a substitute for reviewing what you upload.

## Step 1 — Define ownership and tags

**Where:** Your own tagging.md file.

Choose environment, owner, costCenter and service tags, including who may change them. Decide how missing or inconsistent tags will be reviewed rather than assuming tags enforce a security boundary.

**Check before continuing:** You have a small tagging standard that matches the business ownership model.

## Step 2 — Create and tag a dedicated lab group

**Where:** Azure Portal → Resource groups → Create → Tags.

Create a group for your own project with the chosen tags and apply them to supported child resources. Verify actual child tags; a resource group tag is not automatically inherited unless you configure an appropriate policy/process.

**Check before continuing:** Your group/resources have the expected ownership metadata.

## Step 3 — Create your cost view

**Where:** Subscription → Cost Management → Cost analysis.

Choose a period, actual versus amortized cost basis, currency and grouping by service/resource group/tag. Record untagged costs, data freshness and shared-resource attribution limits so the chart does not imply every charge belongs neatly to one app.

**Check before continuing:** The saved view answers who owns the spend and what basis it uses.

## Step 4 — Configure a budget and verify the route

**Where:** Cost Management → Budgets → Add.

Select your scope/amount/time period and add deliberate actual/forecast thresholds with an approved email/action route. Confirm recipient verification and the test/observed notification separately from the existence of the budget object.

**Check before continuing:** The budget settings and notification delivery evidence are recorded; no spending cap is claimed.

## Step 5 — Design an optional Logic App shutdown for one lab VM

**Where:** Logic App Designer; managed identity and VM IAM.

Create a disabled recurrence workflow, enable its managed identity and grant only the reviewed read/deallocate operations at the one lab VM scope. Add an authenticated ARM read of that exact VM, check an explicit owner-approved shutdown tag/window, then a bounded POST to its deallocate action; keep the workflow disabled until dependencies and recovery are tested.

**Check before continuing:** The design cannot select arbitrary VMs and does not treat stopping an OS as complete cost removal.

## Step 6 — Test the decision before activation

**Where:** Your selected lab VM and workflow history.

First run an observation-only version that records whether this exact VM would qualify. If you later approve the lab action, verify deallocation and a tested restart/access path; do not stop production/provider jobs to obtain a screenshot.

**Check before continuing:** Any real shutdown has an observed target, outcome and recovery result.

## Step 7 — Review residual spend and close out

**Where:** Cost analysis and your inventory.

Compare the observation period with disks, IPs, backups, logs, registry images and other retained services. Disable/delete your lab automation and remove only your lab resources after recording the remaining charges and owners.

**Check before continuing:** Your savings explanation includes ongoing storage/network costs and reporting delay.

## Verification and your own screenshots

| Evidence | What to record | Your result |
| --- | --- | --- |
| New build | Your own files/resource settings and tool versions | Not yet recorded |
| Working path | The actual successful request, configuration or recovery result | Not yet recorded |
| Failure boundary | A meaningful denied, malformed, stale or failed case | Not yet recorded |
| Recovery / cleanup | What you restored or removed and what remains billed | Not yet recorded |

Capture your own architecture/configuration, one working result and one failure/recovery result. Keep tokens, credentials, personal records and private identifiers out of public screenshots. The architecture diagram explains the design; record your own results rather than treating it as execution evidence.

## Troubleshooting order

1. Confirm the named file, working directory and selected tool/interpreter.
2. Check the exact input and resource/account selected for the failing step.
3. Separate identity permission, network/DNS reachability and application validation.
4. Keep the actual error and reconcile an unknown write outcome before repeating it; do not widen access or repeat paid operations blindly.

The numbered steps describe a build procedure. Local syntax checks, an accepted API request, a completed hosted operation and a human verification are different evidence levels; fill in the verification table with what you actually observed.

## Official implementation references

- [learn.microsoft.com — quick-acm-cost-analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis)
- [learn.microsoft.com — tutorial-acm-create-budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
- [learn.microsoft.com — authenticate-with-managed-identity](https://learn.microsoft.com/en-us/azure/logic-apps/authenticate-with-managed-identity)
