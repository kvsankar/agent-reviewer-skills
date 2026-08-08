# Experiment Report: Structured Skills for LLM Code Review

> [!CAUTION]
> **Historical exploratory report, not the project conclusion.** These March
> runs used deliberately vulnerable or synthetic targets, incomplete reference
> sets, and mostly one run per condition. Their apparent positive results did
> not become conclusive evidence. See the chronological
> [exploration history](../../docs/exploration-history.md) and the later
> [real-code conclusion](../../docs/experiment-conclusion.md).

**Date:** 2026-03-05 (Experiments 1-2), 2026-03-06 (Experiment 3), 2026-03-06 to 2026-03-08 (Experiments 4-6)
**Models:** claude-sonnet-4-20250514, gpt-5.3-codex (Codex CLI)
**Runs per condition:** 1 (Experiments 1-3, 5-6), 3 (Experiment 4)
**Evaluation methods:** Ground truth matching (Experiments 1-3), LLM-as-judge (Experiments 4-6)

## 1. Experiment Design

### 1.1 Research Question

Do structured code review skills (SKILL.md files with mnemonic IDs, before/after code examples, and detailed guidelines) improve LLM security review quality compared to zero-shot prompting?

### 1.2 Target Repositories

| Repository | Language | Ground Truth Issues | Files Reviewed |
|---|---|---|---|
| [pygoat](https://github.com/adeyosemanputra/pygoat) | Python/Django | 19 | `introduction/views.py` |
| [dvna](https://github.com/appsecco/dvna) | Node.js | 13 | `core/appHandler.js`, `core/authHandler.js`, `server.js` |
| auth (private) | Python | N/A (no ground truth) | `backend/authentication/services.py` |

Total ground truth: 32 issues across 2 repos (19 pygoat + 13 dvna).

### 1.3 Conditions

**Experiment 1 -- Baseline (with vs without skill):**

| Condition | Description | Prompt Tokens (approx) |
|---|---|---|
| zero-shot | "Review the following code for security issues" | ~100 |
| generic-prompt | OWASP/CWE-aware security prompt with structured output format | ~250 |
| full-skill | Complete SKILL.md with all guidelines and code examples | ~69K chars |

**Experiment 2 -- Ablation (skill component contribution):**

| Condition | Description | Prompt Tokens (approx) |
|---|---|---|
| full-skill | Complete SKILL.md unchanged | ~69K chars |
| principles-only | Code examples stripped, principles/risk/why preserved | ~35K chars |
| ids-only | Just frontmatter + mission + Key Guidelines mnemonic list + output format | ~8K chars |
| trimmed-20 | First 20 of ~50 guidelines only | ~20K chars |

**Experiment 3 -- Improved (guideline quality + prompt structure):**

Based on Experiment 1-2 findings, we made two improvements:
1. **Guideline quality:** Strengthened AUTHZ-CHECK (added IDOR + cookie trust examples), SESSION-SECURE (added unsigned cookie auth), TOKEN-EXPIRE (added predictable token pattern), VALIDATE-INPUT (added SSRF + open redirect). Added TOKEN-PREDICT and AUTHZ-CHECK to the JavaScript skill (previously missing entirely).
2. **Prompt structure:** Created a "hybrid" variant -- ids-only checklist up front + full detailed guidelines only for hard-to-detect categories (AUTHZ-CHECK, SESSION-SECURE, TOKEN-EXPIRE, TOKEN-PREDICT, VALIDATE-INPUT, COOKIE-SECURE, CSRF).

| Condition | Description | Prompt Tokens (approx) |
|---|---|---|
| full-v2 | Improved SKILL.md with strengthened auth/session/token guidelines | ~74K chars |
| hybrid | ids-only checklist + detailed examples for hard-to-detect categories only | ~31K chars |
| ids-only | Same as Exp 2 (control) | ~8K chars |

### 1.4 Evaluation Methodology

Ground truth matching uses three methods in priority order:

1. **Finding ID + text match:** The review contains a mnemonic ID matching the GT type pattern (e.g., `SQL-INJECT` matches GT type `SQL-INJECT`), AND the review text mentions the specific function or code pattern for that GT item (e.g., `sql_lab` for GT-PG-01).
2. **Text-only match:** The review text mentions the function name or code pattern associated with a GT item, even if no mnemonic ID was extracted.
3. **CWE match:** The review text contains the CWE number from the GT item (e.g., `CWE-89`).

**False positive classification:**
- Findings matching a GT vulnerability type present in the repo are NOT counted as FP (they are considered redundant detections of real issues).
- Findings classified as "noise" (e.g., `OWASP`, `AUTHENTICATION-PRESENT`) or "recommendation" (e.g., `MISSING-VALIDATION-LAYER`) are excluded from FP counts.
- Only findings that claim a vulnerability type NOT present in the ground truth are counted as FP.

---

## 2. Results

### 2.1 Experiment 1 -- Baseline: Per-Repo Breakdown

#### pygoat (19 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 | Duration |
|---|---|---|---|---|---|---|---|
| zero-shot | 12 | 1 | 7 | 92.3% | 63.2% | 75.0% | 65.1s |
| generic-prompt | 16 | 0 | 3 | 100.0% | 84.2% | 91.4% | 58.8s |
| full-skill | 14 | 0 | 5 | 100.0% | 73.7% | 84.8% | 66.6s |

#### dvna (13 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 | Duration |
|---|---|---|---|---|---|---|---|
| zero-shot | 8 | 1 | 5 | 88.9% | 61.5% | 72.7% | 50.0s |
| generic-prompt | 9 | 0 | 4 | 100.0% | 69.2% | 81.8% | 55.3s |
| full-skill | 10 | 4 | 3 | 71.4% | 76.9% | 74.1% | 66.6s |

#### Experiment 1 -- Aggregate (pygoat + dvna, 32 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| zero-shot | 20 | 2 | 12 | 90.9% | 62.5% | 74.1% |
| generic-prompt | 25 | 0 | 7 | 100.0% | 78.1% | 87.7% |
| full-skill | 24 | 4 | 8 | 85.7% | 75.0% | 80.0% |

### 2.2 Experiment 2 -- Ablation: Per-Repo Breakdown

#### pygoat (19 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 | Duration |
|---|---|---|---|---|---|---|---|
| full-skill | 17 | 1 | 2 | 94.4% | 89.5% | 91.9% | 124.4s |
| principles-only | 17 | 1 | 2 | 94.4% | 89.5% | 91.9% | 66.2s |
| ids-only | 16 | 0 | 3 | 100.0% | 84.2% | 91.4% | 69.9s |
| trimmed-20 | 14 | 4 | 5 | 77.8% | 73.7% | 75.7% | 59.2s |

#### dvna (13 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 | Duration |
|---|---|---|---|---|---|---|---|
| full-skill | 10 | 4 | 3 | 71.4% | 76.9% | 74.1% | 63.7s |
| principles-only | 11 | 8 | 2 | 57.9% | 84.6% | 68.8% | 65.5s |
| ids-only | 13 | 2 | 0 | 86.7% | 100.0% | 92.9% | 86.6s |
| trimmed-20 | 9 | 5 | 4 | 64.3% | 69.2% | 66.7% | 79.2s |

#### Experiment 2 -- Aggregate (pygoat + dvna, 32 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| full-skill | 27 | 5 | 5 | 84.4% | 84.4% | 84.4% |
| principles-only | 28 | 9 | 4 | 75.7% | 87.5% | 81.2% |
| ids-only | 29 | 2 | 3 | 93.5% | 90.6% | 92.1% |
| trimmed-20 | 23 | 9 | 9 | 71.9% | 71.9% | 71.9% |

### 2.3 Experiment 3 -- Improved: Per-Repo Breakdown

#### pygoat (19 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 | Duration |
|---|---|---|---|---|---|---|---|
| full-v2 | 18 | 3 | 1 | 85.7% | 94.7% | 90.0% | 86.8s |
| hybrid | 15 | 1 | 4 | 93.8% | 78.9% | 85.7% | 86.1s |
| ids-only | 13 | 3 | 6 | 81.2% | 68.4% | 74.3% | 56.2s |

#### dvna (13 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 | Duration |
|---|---|---|---|---|---|---|---|
| full-v2 | 10 | 7 | 3 | 58.8% | 76.9% | 66.7% | 84.2s |
| hybrid | 11 | 3 | 2 | 78.6% | 84.6% | 81.5% | 80.5s |
| ids-only | 11 | 7 | 2 | 61.1% | 84.6% | 71.0% | 79.4s |

#### Experiment 3 -- Aggregate (pygoat + dvna, 32 ground truth issues)

| Condition | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| full-v2 | 28 | 10 | 4 | 73.7% | 87.5% | 80.0% |
| hybrid | 26 | 4 | 6 | 86.7% | 81.2% | 83.9% |
| ids-only | 24 | 10 | 8 | 70.6% | 75.0% | 72.7% |

---

## 3. Detailed Ground Truth Matching

### 3.1 pygoat -- Per-Issue Detection Matrix

| GT ID | Type | Description | zero-shot | generic | full (e1) | full (e2) | princ. | ids (e2) | trim-20 | full-v2 | hybrid | ids (e3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GT-PG-01 | SQL-INJECT | SQL injection in sql_lab() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | CWE | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | CWE |
| GT-PG-02 | SQL-INJECT | SQL injection in injection_sql_lab() | -- | TEXT | CWE | CWE | CWE | CWE | CWE | CWE | ID+TEXT | CWE |
| GT-PG-03 | CMD-INJECT | Command injection in cmd_lab() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | CWE | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-PG-04 | CODE-INJECT | eval() in cmd_lab2() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-PG-05 | XML-INJECT | XXE in xxe_parse() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-PG-06 | CODE-INJECT | Pickle deserialization in insec_des_lab() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | -- |
| GT-PG-07 | CODE-INJECT | Unsafe YAML in a9_lab() | ID+TEXT | TEXT | CWE | CWE | CWE | CWE | ID+TEXT | CWE | CWE | ID+TEXT |
| GT-PG-08 | CODE-INJECT | ImageMath.eval() in a9_lab2() | -- | TEXT | CWE | CWE | CWE | CWE | CWE | CWE | CWE | CWE |
| GT-PG-09 | XSS-PREVENT | Reflected XSS in xss_lab() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | CWE | CWE | TEXT | ID+TEXT | -- | ID+TEXT |
| GT-PG-10 | XSS-PREVENT | XSS filter bypass in xss_lab2() | -- | TEXT | ID+TEXT | ID+TEXT | CWE | CWE | -- | CWE | -- | CWE |
| GT-PG-11 | AUTHZ-CHECK | Admin cookie manipulation in ba_lab() | -- | TEXT | -- | -- | -- | -- | -- | **ID+TEXT** | **ID+TEXT** | -- |
| GT-PG-12 | WEAK-HASH | MD5 hashing in crypto_failure_lab() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-PG-13 | PATH-TRAVERSE | Path traversal in ssrf_lab() | ID+TEXT | TEXT | -- | ID+TEXT | ID+TEXT | TEXT | -- | ID+TEXT | TEXT | -- |
| GT-PG-14 | VALIDATE-INPUT | SSRF in ssrf_lab2() | ID+TEXT | TEXT | -- | ID+TEXT | ID+TEXT | -- | -- | ID+TEXT | ID+TEXT | -- |
| GT-PG-15 | CODE-INJECT | SSTI in ssti_lab() | ID+TEXT | CWE | CWE | CWE | CWE | CWE | CWE | CWE | CWE | CWE |
| GT-PG-16 | CSRF-PROTECT | CSRF-exempt in auth_failure_lab3() | -- | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-PG-17 | NO-HARDCODE | Hardcoded JWT in sec_misconfig_lab3() | ID+TEXT | -- | -- | CWE | CWE | CWE | TEXT | TEXT | -- | -- |
| GT-PG-18 | SESSION-SECURE | Cookie auth in auth_lab_login() | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| GT-PG-19 | PII-LOG | Log injection in a10_lab2() | -- | -- | ID+TEXT | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | TEXT | ID+TEXT | ID+TEXT |

**Detection key:** ID+TEXT = mnemonic ID matched + function/code confirmed in text. TEXT = function name found in review text. CWE = CWE number matched. -- = not detected. **Bold** = newly detected in Experiment 3 (previously missed by all skill conditions).

### 3.2 dvna -- Per-Issue Detection Matrix

| GT ID | Type | Description | zero-shot | generic | full (e1) | full (e2) | princ. | ids (e2) | trim-20 | full-v2 | hybrid | ids (e3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GT-DV-01 | SQL-INJECT | SQL injection in userSearch() | -- | CWE | ID+TEXT | CWE | ID+TEXT | ID+TEXT | CWE | ID+TEXT | ID+TEXT | CWE |
| GT-DV-02 | CMD-INJECT | Command injection in ping() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-DV-03 | PII-ACCESS | Password hashes in listUsersAPI() | TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-DV-04 | XML-INJECT | XXE in bulkProducts() | ID+TEXT | TEXT | ID+TEXT | TEXT | TEXT | ID+TEXT | ID+TEXT | TEXT | ID+TEXT | ID+TEXT |
| GT-DV-05 | AUTHZ-CHECK | IDOR in userEditSubmit() | -- | -- | -- | -- | ID+TEXT | ID+TEXT | -- | **ID+TEXT** | **ID+TEXT** | -- |
| GT-DV-06 | CODE-INJECT | Deserialization in bulkProductsLegacy() | ID+TEXT | TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-DV-07 | VALIDATE-INPUT | Open redirect in redirect() | ID+TEXT | TEXT | -- | ID+TEXT | -- | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT | ID+TEXT |
| GT-DV-08 | ERROR-SAFE | Stack trace in calc() | ID+TEXT | TEXT | TEXT | -- | TEXT | ID+TEXT | -- | -- | ID+TEXT | ID+TEXT |
| GT-DV-09 | TOKEN-EXPIRE | Predictable reset token in resetPw() | -- | -- | -- | -- | -- | ID+TEXT | -- | **TEXT** | **TEXT** | TEXT |
| GT-DV-10 | NO-HARDCODE | Hardcoded session secret | ID+TEXT | TEXT | TEXT | TEXT | TEXT | TEXT | TEXT | TEXT | TEXT | TEXT |
| GT-DV-11 | COOKIE-SECURE | Cookie secure=false | TEXT | TEXT | TEXT | TEXT | TEXT | ID+TEXT | TEXT | TEXT | TEXT | TEXT |
| GT-DV-12 | XSS-PREVENT | Reflected XSS in products.ejs | -- | -- | CWE | CWE | CWE | CWE | -- | -- | -- | -- |
| GT-DV-13 | XSS-PREVENT | Stored XSS in products.ejs | -- | -- | TEXT | CWE | CWE | CWE | TEXT | -- | -- | TEXT |

### 3.3 Previously Missed Vulnerabilities -- Experiment 3 Impact

These GT items were missed by the **full-skill** condition in Experiments 1-2. The table shows whether Experiment 3's improved guidelines fixed them:

| GT ID | Type | Description | Exp 1-2 Status | full-v2 | hybrid |
|---|---|---|---|---|---|
| GT-PG-11 | AUTHZ-CHECK | Admin cookie manipulation in ba_lab() | Missed by all skill conditions | **FIXED** | **FIXED** |
| GT-PG-18 | SESSION-SECURE | Unsigned cookie auth in auth_lab_login() | Never detected by any condition | Still missed | Still missed |
| GT-DV-05 | AUTHZ-CHECK | IDOR in userEditSubmit() | Only principles/ids-only | **FIXED** | **FIXED** |
| GT-DV-09 | TOKEN-EXPIRE | Predictable MD5 reset token in resetPw() | Only ids-only (Exp 2) | **FIXED** | **FIXED** |

**3 of 4 previously hard issues now detected.** The improved AUTHZ-CHECK (with cookie trust + IDOR examples) and TOKEN-PREDICT guidelines directly addressed the systematic misses.

**GT-PG-18 remains the only issue never detected by any condition across all 3 experiments.** This vulnerability (using `set_cookie('userid', ...)` without signing) requires understanding that Django's `set_cookie` creates unsigned cookies vs Django's session framework which signs cookies. No condition -- including zero-shot, generic-prompt, or any skill variant -- has ever flagged this. It represents the current limit of single-pass LLM code review for architectural trust boundary analysis.

### 3.4 False Positive Analysis

**Full-skill false positives (across both experiments):**

| FP Finding ID | Repo | Description |
|---|---|---|
| CRED-STORE | dvna | Flagged credential storage practices (not in GT) |
| CRYPTO-STRONG | dvna | Flagged weak crypto algorithms (not in GT) |
| TIMING-ATTACK | dvna | Flagged timing-based side channels (not in GT) |
| SESSION-SECURE | dvna | Flagged session security (overlaps GT-DV-11 but different type) |
| XPATH-INJECT | dvna | Flagged potential XPath injection (not present) |
| CRYPTO-DEPRECATE | dvna | Flagged deprecated crypto usage (not in GT) |
| RANDOM-SECURE | pygoat | Flagged weak random number generation (not in GT as separate issue) |

Most FPs are legitimate security concerns that happen to not be in our ground truth. Only XPATH-INJECT is a true false alarm.

---

## 4. Analysis

### 4.1 Skill Impact on Recall

Comparing zero-shot to full-skill (Experiment 1 aggregate):

- **Recall improvement:** 62.5% -> 75.0% (+20% relative, +12.5pp absolute)
- **The skill helps find:** PII logging (GT-PG-19), CSRF issues (GT-PG-16), additional SQL injections (GT-PG-02), template injection indirectly via CWE
- **The skill doesn't help with:** Authorization logic (GT-PG-11), session design flaws (GT-PG-18)

### 4.2 Ablation: What Matters Most

Comparing skill variants (Experiment 2 aggregate):

| Condition | F1 | Key Insight |
|---|---|---|
| ids-only (8K chars) | **92.1%** | Mnemonic ID list alone is highly effective |
| full-skill (69K chars) | 84.4% | More detail doesn't always help; higher FP |
| principles-only (35K chars) | 81.2% | Best recall (87.5%) but worst precision (75.7%) |
| trimmed-20 (20K chars) | 71.9% | Partial guidelines confuse more than help |

**Key findings:**

1. **ids-only achieves the best F1 (92.1%)** with just ~8K chars of prompt. The concise mnemonic ID list (e.g., `SQL-INJECT: Check for parameterized queries`) gives the model a focused checklist without overwhelming it.

2. **Code examples improve precision, not recall.** Full-skill (with examples) has 84.4% precision vs principles-only (without examples) at 75.7%. The before/after code patterns help the model distinguish real issues from noise.

3. **Principles-only has the best recall (87.5%)** but generates more false positives. Without code examples to anchor judgments, the model over-reports.

4. **Partial guidelines (trimmed-20) underperform everything.** Giving 20 of ~50 guidelines is worse than giving just the ID list. The model seems to treat the partial list as exhaustive and misses categories not in the first 20.

5. **Token efficiency:** ids-only achieves 92.1% F1 with ~8K chars. Full-skill uses ~69K chars for 84.4% F1. The marginal value of additional tokens is negative beyond the mnemonic ID list for this task.

### 4.3 Generic Prompt Strength

The generic-prompt condition (Exp 1) achieves 87.7% F1 -- outperforming full-skill at 80.0% in Exp 1. This is notable because:

- It uses ~250 tokens vs ~69K for full-skill
- It achieves 100% precision (zero false positives)
- It has 78.1% recall -- better than zero-shot (62.5%) and full-skill Exp 1 (75.0%)

However, generic-prompt's strength may be inflated by our evaluation method: it finds issues via function names in free-form text (TEXT match), which are more likely to be correctly attributed. The structured mnemonic IDs from skill-guided reviews sometimes use different naming than our GT type patterns, causing matching failures.

### 4.4 Experiment 3: Guideline Quality + Prompt Structure

Experiment 3 tested two improvements simultaneously and compared against an ids-only control run:

**Improvement 1 -- Guideline quality (full-v2):**

| Metric | full-skill (Exp 2) | full-v2 (Exp 3) | Delta |
|---|---|---|---|
| Recall | 84.4% | **87.5%** | +3.1pp |
| pygoat recall | 89.5% | **94.7%** | +5.2pp |
| GT-PG-11 (AUTHZ cookie) | Missed | **Detected** | Fixed |
| GT-DV-05 (IDOR) | Missed | **Detected** | Fixed |
| GT-DV-09 (predictable token) | Missed | **Detected** | Fixed |

The strengthened AUTHZ-CHECK, TOKEN-EXPIRE, and VALIDATE-INPUT guidelines directly fixed 3 of the 4 previously hard issues. pygoat full-v2 hit **18/19** (only GT-PG-18 remains undetectable).

**Improvement 2 -- Prompt structure (hybrid):**

| Metric | full-v2 | hybrid | ids-only (Exp 3) |
|---|---|---|---|
| F1 | 80.0% | **83.9%** | 72.7% |
| Precision | 73.7% | **86.7%** | 70.6% |
| Recall | 87.5% | 81.2% | 75.0% |
| Prompt size | ~74K chars | ~31K chars | ~8K chars |
| False positives | 10 | **4** | 10 |

The hybrid approach (ids checklist + detailed examples for hard categories only) achieves:
- **Best precision** (86.7%) and **best F1** (83.9%) in Experiment 3
- **Fewest false positives** (4 vs 10 for both full-v2 and ids-only)
- **58% fewer tokens** than full-v2 for comparable recall
- Detects 3 of 4 previously hard issues (same as full-v2)

**Why hybrid works:** The ids-only checklist gives the model a focused scanning agenda. The detailed examples for auth/session/token categories provide the depth needed for subtle logic bugs without cluttering attention with 50+ detailed guidelines for common patterns the model already knows.

### 4.5 Variance Across Runs

ids-only shows meaningful variance between Exp 2 and Exp 3:

| Repo | ids-only (Exp 2) | ids-only (Exp 3) | Delta |
|---|---|---|---|
| pygoat recall | 84.2% | 68.4% | -15.8pp |
| dvna recall | 100.0% | 84.6% | -15.4pp |
| Aggregate F1 | 92.1% | 72.7% | -19.4pp |

This dramatic swing confirms that **single-run results have high variance**. The ids-only Exp 2 result (92.1% F1) was likely an optimistic outlier. The Exp 3 result (72.7%) may be pessimistic. True performance is likely between them. Future experiments need 3-5 runs per condition for statistical reliability.

---

## 5. Detailed Findings Per Condition

### 5.1 Full-v2 (Experiment 3) -- Best Recall

**pygoat: 18/19 detected (94.7% recall)**

Detected via ID+TEXT match: SQL-INJECT (sql_lab), CMD-INJECT (cmd_lab), CODE-INJECT (cmd_lab2, insec_des_lab), XXE-INJECT (xxe_parse), XSS-PREVENT (xss_lab), WEAK-HASH (crypto_failure_lab), PATH-TRAVERSE (ssrf_lab), SSRF-PREVENT (ssrf_lab2), CSRF-PROTECT (csrf_exempt), **AUTHZ-CHECK (ba_lab) [NEW]**

Detected via CWE/TEXT match: CWE-89 (injection_sql_lab), CWE-502 (yaml.load), CWE-94 (ImageMath, ssti_lab), CWE-79 (xss_lab2), TEXT (jwt, a10_lab2)

Missed: GT-PG-18 only (SESSION-SECURE -- unsigned cookies)

False positives: RANDOM-SECURE, LOG-SANITIZE, IMPORT-GOOD

**dvna: 10/13 detected (76.9% recall)**

Newly detected vs Exp 1-2: **GT-DV-05 (IDOR via AUTHZ-CHECK)**, **GT-DV-09 (predictable token via TEXT match)**

Missed: GT-DV-08 (error disclosure), GT-DV-12 (reflected XSS), GT-DV-13 (stored XSS)

False positives: TOKEN-PREDICT, SESSION-SECURE, RATE-LIMIT, HTTPS-ONLY, FAILING, IMMEDIATE, URGENT

### 5.2 Hybrid (Experiment 3) -- Best F1

**pygoat: 15/19 detected (78.9% recall, 93.8% precision)**

Detected via ID+TEXT match: SQL-INJECT (sql_lab, injection_sql_lab), CMD-INJECT (cmd_lab), CODE-INJECT (cmd_lab2, insec_des_lab), XXE-INJECT (xxe_parse), WEAK-HASH (crypto_failure_lab), SSRF-VULN (ssrf_lab2), MISSING-CSRF (csrf_exempt), PII-LOG (a10_lab2), **AUTHZ-CHECK (ba_lab) [NEW]**

Missed: GT-PG-09 (XSS), GT-PG-10 (XSS), GT-PG-17 (hardcoded JWT), GT-PG-18 (unsigned cookies)

False positives: HASH-PASSWORD (1 total -- best precision of any skill condition)

**dvna: 11/13 detected (84.6% recall, 78.6% precision)**

Newly detected vs Exp 1-2 full-skill: **GT-DV-05 (IDOR via AUTHZ-CHECK)**, **GT-DV-09 (predictable token via TEXT)**

Missed: GT-DV-12 (reflected XSS), GT-DV-13 (stored XSS)

False positives: TOKEN-PREDICT, SESSION-SECURE, INPUT-TYPE

### 5.3 Full-Skill (Experiment 2) -- Pre-Improvement Baseline

**pygoat: 17/19 detected (89.5% recall)**

Missed: GT-PG-11 (AUTHZ-CHECK -- cookie manipulation), GT-PG-18 (SESSION-SECURE -- unsigned cookies)

False positives: RANDOM-SECURE

**dvna: 10/13 detected (76.9% recall)**

Missed: GT-DV-05 (IDOR), GT-DV-08 (error disclosure), GT-DV-09 (predictable reset token)

False positives: CRED-STORE, XPATH-INJECT, CRYPTO-DEPRECATE, TIMING-ATTACK

### 5.4 Zero-Shot -- Baseline

**pygoat: 12/19 detected (63.2% recall)**

Found major injection vulnerabilities but missed: second SQL injection, ImageMath, XSS filter bypass, authorization, CSRF, session, PII logging.

**dvna: 8/13 detected (61.5% recall)**

Missed SQL injection (!), IDOR, predictable tokens, both XSS template issues.

---

## 6. Methodology Notes and Limitations

### 6.1 Evaluation Limitations

1. **Single run per condition.** LLM outputs are stochastic; single runs may not represent typical performance. The full-skill pygoat variance (73.7% vs 89.5% across experiments) shows this clearly.

2. **Generic-prompt finding extraction.** The generic-prompt condition produces 0 extracted findings via our regex-based mnemonic extractor, but the review text mentions functions by name. All generic-prompt TP comes from text/CWE matching. This makes its precision artificially 100% (0 FP because 0 extracted findings to misclassify).

3. **Ground truth scope.** Our GT covers only the most obvious vulnerabilities. Some "false positives" (like TIMING-ATTACK, CRED-STORE) are legitimate security concerns not in our GT. A broader GT would change precision numbers significantly.

4. **Function name matching sensitivity.** Some GT items use generic function patterns (e.g., "path", "redirect", "password") that may match text discussing unrelated topics, potentially inflating TP counts.

5. **Cross-language skill application.** The Python security skill was applied to pygoat; the JavaScript security skill to dvna. Skills are language-specific, so cross-comparisons between repos should be interpreted cautiously.

### 6.2 Experimental Infrastructure

- **Model:** claude-sonnet-4-20250514 via Claude CLI with OAuth (Pro Max subscription)
- **Invocation:** `claude --print --model MODEL --tools "" --dangerously-skip-permissions` with prompt on stdin
- **Environment isolation:** CLAUDECODE env var stripped to allow nested CLI invocation
- **Rate limiting:** 3-second delay between API calls
- **Timeout:** 300 seconds per review
- **Prompt construction:** Skill variant (or zero-shot/generic prompt) prepended to code files, separated by `---`

### 6.3 Ground Truth Sources

- **pygoat:** 19 issues manually cataloged from [adeyosemanputra/pygoat](https://github.com/adeyosemanputra/pygoat), a deliberately vulnerable Django application. Issues span SQL injection, command injection, code injection, XSS, XXE, deserialization, CSRF, path traversal, SSRF, SSTI, weak crypto, hardcoded secrets, broken auth, and log injection.

- **dvna:** 13 issues manually cataloged from [appsecco/dvna](https://github.com/appsecco/dvna), a deliberately vulnerable Node.js application. Issues span SQL injection, command injection, XXE, deserialization, IDOR, open redirect, error disclosure, predictable tokens, hardcoded secrets, insecure cookies, and XSS.

---

## 7. Conclusions

### From Experiments 1-2 (Baseline + Ablation)

1. **Structured skills improve recall over zero-shot** by +12.5pp (62.5% -> 75.0%), confirming that in-context guidelines help LLMs find more vulnerabilities.

2. **The mnemonic ID list alone is surprisingly effective.** The ids-only variant (8K chars) achieves high F1 in Exp 2 (92.1%), though with high variance across runs (72.7% in Exp 3). The model already has strong security knowledge -- it mainly needs a focused checklist.

3. **Code examples improve precision, not recall.** Full-skill vs principles-only shows examples help the model make more precise judgments (84.4% vs 75.7% precision) while recall is comparable.

4. **Partial guidelines hurt more than help.** Trimmed-20 (71.9% F1) underperforms ids-only despite containing more detail. An incomplete list narrows the model's focus unproductively.

### From Experiment 3 (Improved Guidelines + Hybrid Structure)

5. **Guideline quality matters for hard categories.** Strengthening AUTHZ-CHECK, TOKEN-EXPIRE, and VALIDATE-INPUT guidelines with specific examples (IDOR ownership checks, predictable token patterns, SSRF/redirect validation) fixed 3 of 4 previously undetectable issues. full-v2 hit 18/19 on pygoat (94.7% recall).

6. **The hybrid prompt structure is the optimal tradeoff.** ids-only checklist + detailed examples for hard categories achieves the best F1 (83.9%) with the fewest false positives (4), using 58% fewer tokens than full-skill. It works because:
   - Common vulnerability patterns (SQLi, XSS, command injection) don't need detailed examples -- the model knows them
   - Subtle patterns (IDOR, cookie trust, token predictability) DO need detailed examples to trigger detection
   - The checklist keeps the model focused; selective detail adds depth where needed

7. **One vulnerability remains undetectable.** GT-PG-18 (unsigned cookie auth in Django) has been missed by every condition across all 3 experiments, including zero-shot and generic-prompt. This represents the current limit of single-pass LLM review for architectural trust boundary analysis.

8. **Single-run variance is significant.** ids-only F1 ranges from 72.7% to 92.1% across experiments. Future work should use 3-5 runs per condition with statistical significance testing.

### Practical Recommendations

- **For production use:** Deploy the hybrid variant. It balances thoroughness and precision at reasonable token cost.
- **For skill development:** Invest guideline quality in categories the model struggles with (authorization, session, tokens). Don't add more detail for patterns the model already handles well (injection, XSS, crypto).
- **For evaluation:** Use 3+ runs per condition. Automated ground truth matching works but has limitations -- expert review of a sample of outputs would strengthen confidence.

---

## Appendix A: Skill Variant Token Sizes

| Variant | Characters | Approx Tokens | Notes |
|---|---|---|---|
| full-v2 | ~74,000 | ~18,500 | Improved auth/session/token guidelines |
| full (original) | ~69,000 | ~17,000 | Exp 1-2 version |
| principles-only | ~35,000 | ~8,750 | Code examples stripped |
| **hybrid** | **~31,000** | **~7,750** | **ids checklist + hard-category detail** |
| trimmed-20 | ~20,000 | ~5,000 | First 20 guidelines |
| ids-only | ~8,000 | ~2,000 | Mnemonic ID list only |
| generic-prompt | ~1,000 | ~250 | OWASP/CWE-aware prompt |
| zero-shot prompt | ~400 | ~100 | Minimal instruction |

## Appendix B: Ground Truth Definitions

### pygoat (19 issues)

| ID | Type | CWE | Severity | Function | Description |
|---|---|---|---|---|---|
| GT-PG-01 | SQL-INJECT | CWE-89 | CRITICAL | sql_lab | SQL injection via string concatenation |
| GT-PG-02 | SQL-INJECT | CWE-89 | CRITICAL | injection_sql_lab | SQL injection (second instance) |
| GT-PG-03 | CMD-INJECT | CWE-78 | CRITICAL | cmd_lab | Command injection via subprocess shell=True |
| GT-PG-04 | CODE-INJECT | CWE-94 | CRITICAL | cmd_lab2 | eval() on user input |
| GT-PG-05 | XML-INJECT | CWE-611 | HIGH | xxe_parse | XXE via unsafe XML parsing |
| GT-PG-06 | CODE-INJECT | CWE-502 | CRITICAL | insec_des_lab | Insecure pickle deserialization from cookies |
| GT-PG-07 | CODE-INJECT | CWE-502 | CRITICAL | a9_lab | Unsafe YAML loading with yaml.Loader |
| GT-PG-08 | CODE-INJECT | CWE-94 | HIGH | a9_lab2 | ImageMath.eval() with user-controlled expression |
| GT-PG-09 | XSS-PREVENT | CWE-79 | HIGH | xss_lab | Reflected XSS -- user input rendered unescaped |
| GT-PG-10 | XSS-PREVENT | CWE-79 | HIGH | xss_lab2 | XSS with ineffective filter bypass |
| GT-PG-11 | AUTHZ-CHECK | CWE-639 | HIGH | ba_lab | Admin access via client-side cookie manipulation |
| GT-PG-12 | WEAK-HASH | CWE-328 | HIGH | crypto_failure_lab | MD5 password hashing without salt |
| GT-PG-13 | PATH-TRAVERSE | CWE-22 | HIGH | ssrf_lab | Path traversal via unvalidated file parameter |
| GT-PG-14 | VALIDATE-INPUT | CWE-918 | HIGH | ssrf_lab2 | SSRF via unvalidated URL parameter |
| GT-PG-15 | CODE-INJECT | CWE-94 | CRITICAL | ssti_lab | Server-side template injection |
| GT-PG-16 | CSRF-PROTECT | CWE-352 | HIGH | auth_failure_lab3 | CSRF-exempt on state-changing endpoint |
| GT-PG-17 | NO-HARDCODE | CWE-798 | HIGH | sec_misconfig_lab3 | Hardcoded JWT secret key |
| GT-PG-18 | SESSION-SECURE | CWE-384 | HIGH | auth_lab_login | Cookie-based auth without signature verification |
| GT-PG-19 | PII-LOG | CWE-117 | MEDIUM | a10_lab2 | Unsanitized user input in log entries |

### dvna (13 issues)

| ID | Type | CWE | Severity | Function/Location | Description |
|---|---|---|---|---|---|
| GT-DV-01 | SQL-INJECT | CWE-89 | CRITICAL | userSearch() | SQL injection via string concatenation |
| GT-DV-02 | CMD-INJECT | CWE-78 | CRITICAL | ping() | Command injection via child_process.exec() |
| GT-DV-03 | PII-ACCESS | CWE-200 | HIGH | listUsersAPI() | API returns password hashes |
| GT-DV-04 | XML-INJECT | CWE-611 | CRITICAL | bulkProducts() | XXE via libxmljs with noent:true |
| GT-DV-05 | AUTHZ-CHECK | CWE-639 | HIGH | userEditSubmit() | IDOR -- no ownership check |
| GT-DV-06 | CODE-INJECT | CWE-502 | CRITICAL | bulkProductsLegacy() | Insecure deserialization via node-serialize |
| GT-DV-07 | VALIDATE-INPUT | CWE-601 | MEDIUM | redirect() | Open redirect -- unvalidated URL |
| GT-DV-08 | ERROR-SAFE | CWE-215 | MEDIUM | calc() | Stack trace disclosure -- no error handling |
| GT-DV-09 | TOKEN-EXPIRE | CWE-640 | CRITICAL | resetPw() | Password reset token is predictable MD5 of username |
| GT-DV-10 | NO-HARDCODE | CWE-798 | HIGH | server.js | Hardcoded session secret 'keyboard cat' |
| GT-DV-11 | COOKIE-SECURE | CWE-614 | MEDIUM | server.js | Cookie secure flag set to false |
| GT-DV-12 | XSS-PREVENT | CWE-79 | HIGH | products.ejs | Reflected XSS via unescaped output |
| GT-DV-13 | XSS-PREVENT | CWE-79 | HIGH | products.ejs | Stored XSS via unescaped product data |

---

## Experiments 4-6: Rhodes Python Code Quality Skill

### Overview

Experiments 4-6 extend the evaluation from security-focused skills to code quality skills, using the `python-rhodes-reviewer` skill (70 guidelines from Brandon Rhodes' conference talks and Python Patterns Guide). These experiments also introduce:

- **LLM-as-judge evaluation** -- a judge model semantically assesses whether each ground truth violation was caught, replacing the keyword/CWE matching used for security experiments
- **Cross-model comparison** -- Codex CLI (gpt-5.3-codex) vs Claude (claude-sonnet-4)
- **Real-world code** -- reviews of actual open-source repositories, not just synthetic targets

### Evaluation Method: LLM-as-Judge

For code quality skills, ground truth matching is subjective. A review might flag "database queries should be separated from calculation logic" without using the term "HOIST-IO." The judge receives each ground truth issue plus the full review text and determines whether the review semantically addresses that issue, regardless of terminology.

Judge model: claude-sonnet-4-20250514 (same model as reviewer, potential bias acknowledged).

---

## 4. Experiment 4: Rhodes Synthetic -- Multi-Run (3 runs per condition)

### 4.1 Design

**Target:** Synthetic `order_processor.py` with 15 planted Rhodes violations (comments stripped in v3).
**Skill:** `python-rhodes-reviewer/SKILL.md` (~62K chars, 70 guidelines)
**Conditions:** zero-shot, generic-prompt, full-skill, hybrid
**Runs per condition:** 3

**Important methodological fix:** The initial synthetic file (v1/v2) contained ground truth comments like `# GT-RH-14: NO-IMPORT-FX - Side effect at import time` directly in the source code. This leaked the answers to both the reviewer and the judge, inflating all scores -- Codex scored 100% recall. In v3, all hint comments were stripped and the experiment re-run. Results below are from the clean v3 run.

#### Conditions

| Condition | Description | Prompt Size |
|---|---|---|
| zero-shot | "Review this code for quality, style, and design issues" | 252 chars |
| generic-prompt | Pythonic idioms, SOLID, testability, separation of concerns, naming, code smells | 654 chars |
| full-skill | Complete Rhodes SKILL.md with all 70 guidelines and examples | 62,559 chars |
| hybrid | ids-only checklist + detailed guidance for 8 hard-to-detect guidelines (NO-MOCK, NO-CALL, TOP-DOWN, COPERNICAN, BREAK-TEST, PASS-FUNC, PREBOUND-METHOD, NO-SCATTERED-IFS) | 62,834 chars |

#### Ground Truth (15 planted violations)

| ID | Type | Severity | Function | Description |
|---|---|---|---|---|
| GT-RH-01 | HOIST-IO | HIGH | process() | I/O (file read, DB queries, DB write, notifications) mixed in business logic |
| GT-RH-02 | FUNC-SHELL | HIGH | fulfill_order() | Pure logic tangled with I/O (DB, HTTP, DB update) |
| GT-RH-03 | NO-MOCK | MEDIUM | get_daily_report() | Requires mocking DB + SMTP to test -- signals coupling |
| GT-RH-04 | COMP-INHERIT | MEDIUM | OrderProcessor | Multiple inheritance instead of composition |
| GT-RH-05 | NO-MUTSTATE | MEDIUM | get_order_summary() | Clears self.orders as side effect in a getter |
| GT-RH-06 | EXPLICIT-NAME | LOW | run(), _do() | Vague method names |
| GT-RH-07 | NAMED-TUPLE | LOW | create_shipping_label() | Dict with fixed keys instead of dataclass/namedtuple |
| GT-RH-08 | LIST-FRONT | MEDIUM | add_urgent() | list.insert(0, x) for O(n) front insertion |
| GT-RH-09 | NAME-COMMENT | LOW | calc() | Single-letter variables with explanatory comments |
| GT-RH-10 | INDENT-LIMIT | MEDIUM | validate_order_batch() | 7 levels of nesting |
| GT-RH-11 | NO-EVAL | HIGH | apply_dynamic_rule() | eval() on rule string |
| GT-RH-12 | TOP-DOWN | LOW | process_refund() | Calls helpers defined 20+ lines below |
| GT-RH-13 | NO-GLOBAL-MUT | MEDIUM | register_handler() | Module-level mutable globals |
| GT-RH-14 | NO-IMPORT-FX | HIGH | module level | I/O at import time: logging, sqlite3.connect, CREATE TABLE |
| GT-RH-15 | NO-CALL | LOW | OrderValidator | __call__() makes validator(order) ambiguous |

### 4.2 Results -- Multi-Run (v2, with GT comments -- TAINTED)

These results are included for transparency but should not be trusted. The GT comments in the source code leaked answers to the models.

| Condition | Avg Recall | Per-Run Recall |
|---|---|---|
| generic-prompt | 71.1% | 60%, 80%, 73% |
| zero-shot | 68.9% | 67%, 73%, 67% |
| full-skill | 62.2% | 73%, 67%, 47% |
| hybrid | 62.2% | 60%, 67%, 60% |

### 4.3 Results -- Clean (v3, GT comments stripped)

| Condition | Detected | Recall |
|---|---|---|
| generic-prompt | 10 | 66.7% |
| hybrid | 9 | 60.0% |
| zero-shot | 9 | 60.0% |
| full-skill | 8 | 53.3% |
| codex-zero-shot | 6 | 40.0% |

#### Per-Issue Detection Matrix (v3, clean)

| Issue | Type | codex | zero-shot | generic | full-skill | hybrid |
|---|---|---|---|---|---|---|
| GT-RH-01 HOIST-IO | arch | Y | Y | Y | Y | Y |
| GT-RH-02 FUNC-SHELL | arch | - | Y | Y | - | Y |
| GT-RH-03 NO-MOCK | arch | - | - | Y | - | - |
| GT-RH-04 COMP-INHERIT | OOP | - | Y | Y | Y | Y |
| GT-RH-05 NO-MUTSTATE | API | - | - | - | - | - |
| GT-RH-06 EXPLICIT-NAME | naming | - | - | Y | Y | - |
| GT-RH-07 NAMED-TUPLE | data | - | Y | - | - | - |
| GT-RH-08 LIST-FRONT | perf | Y | - | - | - | Y |
| GT-RH-09 NAME-COMMENT | style | Y | Y | Y | Y | Y |
| GT-RH-10 INDENT-LIMIT | style | Y | Y | Y | Y | Y |
| GT-RH-11 NO-EVAL | perf | Y | Y | Y | Y | Y |
| GT-RH-12 TOP-DOWN | org | - | - | - | - | - |
| GT-RH-13 NO-GLOBAL-MUT | OOP | - | Y | Y | Y | Y |
| GT-RH-14 NO-IMPORT-FX | org | Y | Y | Y | Y | Y |
| GT-RH-15 NO-CALL | OOP | - | - | - | - | - |

**Universally detected** (all conditions): HOIST-IO, NAME-COMMENT, INDENT-LIMIT, NO-EVAL, NO-IMPORT-FX -- these are well-known code smells any reviewer catches.

**Universally missed** (all conditions): NO-MUTSTATE (side effect in getter), TOP-DOWN (code ordering), NO-CALL (__call__ readability) -- genuinely subtle issues even with the skill loaded.

### 4.4 Impact of GT Comment Leakage

| Condition | v2 Recall (tainted) | v3 Recall (clean) | Drop |
|---|---|---|---|
| codex-zero-shot | 100.0% | 40.0% | -60.0pp |
| generic-prompt | 71.1% | 66.7% | -4.4pp |
| zero-shot | 68.9% | 60.0% | -8.9pp |
| full-skill | 62.2% | 53.3% | -8.9pp |
| hybrid | 62.2% | 60.0% | -2.2pp |

Codex was most affected because it processed the GT comments as strong signals for what to look for. Claude conditions were less affected, suggesting they relied more on general code understanding than comment hints.

**Lesson learned:** Synthetic test code must never contain ground truth annotations. This applies to any LLM evaluation -- models will exploit any signal in the input.

---

## 5. Experiment 5: Rhodes Synthetic -- Cross-Model Comparison

### 5.1 Design

Same clean synthetic target (v3, no GT comments). Compares Codex CLI (gpt-5.3-codex) against Claude conditions.

### 5.2 Findings by Type

Codex (gpt-5.3-codex) found 13 issues using its own taxonomy:

| Codex Finding | Maps to GT | Type |
|---|---|---|
| SEC-001 (eval) | GT-RH-11 NO-EVAL | security/perf |
| DB-001 (import-time side effects) | GT-RH-14 NO-IMPORT-FX | organization |
| ID-001 (non-unique order ID) | -- | correctness bug |
| DATA-001 (missing computed fields) | -- | correctness bug |
| DB-002 (wrong schema in query) | -- | correctness bug |
| NET-001 (SMTP misuse) | -- | correctness bug |
| NET-002 (no timeout on HTTP) | -- | robustness |
| VAL-001 (deep nesting) | GT-RH-10 INDENT-LIMIT | style |
| OBS-001 (print for logging) | -- | operations |
| PERF-001 (queue front insert) | GT-RH-08 LIST-FRONT | performance |
| STYLE-001 (cryptic naming) | GT-RH-09 NAME-COMMENT | naming |
| CFG-001 (per-request config read) | GT-RH-01 HOIST-IO | architecture |
| VAL-002 (silent product skip) | -- | correctness bug |

**Key insight:** Codex found 6 issues that map to our ground truth (40% recall) but also found 7 correctness/robustness bugs that no Claude condition flagged. Codex acts as a **bug hunter** rather than an **architectural reviewer**. The tools are complementary, not competing.

---

## 6. Experiment 6: Real-World Code (doit task runner)

### 6.1 Design

**Target:** [pydoit/doit](https://github.com/pydoit/doit) (2,028 stars) -- a Python task automation tool.
**Files:** `doit/action.py` (556 lines), `doit/runner.py` (577 lines)
**No ground truth** -- qualitative comparison of what each condition finds.
**Runs:** 1 per condition.

This is the most important experiment because it uses real-world code with no planted violations and no ground truth hints. The code has organic quality issues mixed with legitimate design decisions.

### 6.2 Results

| Condition | Findings | Duration | Finding IDs |
|---|---|---|---|
| zero-shot | 9 | 64.7s | LONG-METHOD-1, STRING-FORMAT-1, MAGIC-NUMBER-1, BROAD-EXCEPT-1, VALIDATION-1, LONG-METHOD-2, UNUSED-IMPORT-1, TYPE-HINTS-1, MUTABLE-DEFAULT-1 |
| generic-prompt | 8 | 86.3s | LONG-METHOD, GOD-CLASS, PARAM-COUNT, OLD-FORMAT, MAGIC-NUM, MIXED-CONCERNS, USE-CONST, BROAD-EXCEPT |
| full-skill | 9 | 73.1s | HOIST-IO, FUNC-SHELL, INDENT-LIMIT, PRECISE-NOUN, NO-GLOBAL-MUT, TOP-DOWN, EXPLICIT-NAME, DICT-COMP, EXCEPT-HIER |
| hybrid | 11 | 86.0s | HOIST-IO, NO-MOCK, FUNC-TEST, PRECISE-NOUN, TOP-DOWN, CONTROL-CALLER, NO-GLOBAL-MUT, KEY-SHARE, EXCEPT-HIER, FUNC-SHELL, INDENT-LIMIT |
| codex-zero-shot | 8 | 224.9s | KWARG_OVERRIDE_INJECTION, STD_STREAM_RESTORE_GAP, CALLABLE_ACTION_REEVALUATED, DEVNULL_FILE_DESCRIPTOR_LEAK, MREPORTER_SIGNATURE_MISMATCH, THREAD_RUNNER_DOUBLE_TEARDOWN, ASSERT_USED_FOR_RUNTIME_VALIDATION, EXACT_TYPE_CHECKS |

### 6.3 Analysis: Finding Quality by Category

| Category | zero-shot | generic | full-skill | hybrid | codex |
|---|---|---|---|---|---|
| **Surface lint** (long methods, formatting, type hints) | 6 | 5 | 0 | 0 | 0 |
| **Architectural** (I/O separation, testability, SoC) | 1 | 1 | 4 | 5 | 0 |
| **Domain-specific** (NO-MOCK, FUNC-TEST, CONTROL-CALLER) | 0 | 0 | 1 | 3 | 0 |
| **Actual bugs** (fd leak, stream restore, kwarg override) | 0 | 0 | 0 | 0 | 5 |
| **Code smells** (magic numbers, broad except, naming) | 2 | 2 | 4 | 3 | 3 |

### 6.4 Key Findings

**1. Skills shift reviews from surface to architecture.**
Without the skill, reviews focus on linter-level findings: long methods, string formatting, type hints, magic numbers. With the skill, reviews focus on architectural principles: I/O separation, testability, naming precision, exception hierarchies.

**2. The hybrid variant found the most issues (11) and the most domain-specific insights (3).**
NO-MOCK ("this architecture forces excessive mocking in tests"), FUNC-TEST ("complex class-based testing structure"), and CONTROL-CALLER ("methods assume too much about output handling") are insights that only emerge from Rhodes' philosophy. No other condition produced them.

**3. Codex found real bugs nobody else caught.**
File descriptor leaks, stream restore gaps after exceptions, kwargs override injection, double teardown in threading -- these are correctness issues, not style issues. Codex operates as a bug hunter, not an architectural reviewer.

**4. The tools are complementary.**
No single condition found everything. The skill provides architectural perspective; Codex provides bug detection; generic prompts provide surface coverage. A comprehensive review would combine approaches.

---

## 7. Cross-Experiment Conclusions

### 7.1 When Skills Add Value

| Scenario | Value | Evidence |
|---|---|---|
| **Architectural review** | High | Skills shift focus from surface lint to design principles (Experiment 6) |
| **Domain-specific insights** | High | NO-MOCK, CONTROL-CALLER, AUTHZ-CHECK only caught with skills (Experiments 3, 6) |
| **Structured output** | High | Skills produce consistent mnemonic IDs, before/after code, principle citations |
| **Bug detection** | None | Skills don't find correctness bugs -- use static analysis or Codex (Experiment 6) |
| **Obvious code smells** | Neutral-to-negative | Skills may crowd out findings the model catches natively (Experiment 4, full-skill at 53% vs zero-shot at 60%) |

### 7.2 The Prompt Dilution Problem

Across both security and Rhodes experiments, longer skill prompts consistently hurt recall on "easy" issues:

| Experiment | full-skill recall | zero-shot recall | Delta |
|---|---|---|---|
| Security (pygoat+dvna avg) | Higher F1 | Lower F1 | Skill helps |
| Rhodes synthetic (v3 clean) | 53.3% | 60.0% | Skill hurts |
| Rhodes real-world (doit) | 9 findings (architectural) | 9 findings (surface) | Different, not more |

The skill doesn't find *more* -- it finds *differently*. This is the core value proposition.

### 7.3 Practical Recommendations

1. **Use full skills for architectural and design reviews** where the goal is to enforce a specific philosophy (Rhodes, SOLID, clean architecture).

2. **Use hybrid variants** when you want both coverage and domain-specific insights. The hybrid was the most consistent performer on Rhodes real-world code.

3. **Don't use skills for generic quality checks** -- a well-crafted generic prompt performs equally or better on surface issues.

4. **Combine tools for comprehensive reviews** -- skills for architecture, static analysis for bugs, generic prompts for coverage.

5. **Keep skills concise** -- the 62K-char Rhodes skill showed prompt dilution effects. Skills under 30K chars are likely to perform better.

### 7.4 Methodology Notes

- **Single-run variance is significant.** In the multi-run Rhodes experiment (v2), recall ranged from 47% to 73% for the same condition. Single-run results should be treated as directional, not definitive.

- **LLM-as-judge has limitations.** The judge is the same model family as the reviewer, which may create blind spots. Issues the model systematically misunderstands won't be caught by the judge either.

- **Synthetic code is risky for evaluation.** The GT comment leakage (v2 vs v3) showed a 60-percentage-point inflation for Codex. Any annotation, naming convention, or structural hint in synthetic code can bias results. Real-world code is the only trustworthy target.

- **Codex comparison is single-model, single-run.** The gpt-5.3-codex results are directional. A fair cross-model comparison would need multiple runs, identical prompts, and controlled output formats.
