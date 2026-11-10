# Data Dictionary: Kerala Kollam Case Lifecycle Dataset

**Dataset File:** `data/raw/kerala/kollam_lifecycle_kaplanmeier.csv`  
**Processed Target:** `data/processed/kollam_cases_cleaned.parquet` & `data/processed/kollam_cases_cleaned.csv`  
**Provenance:** Extracted from the Kollam ONCourts digital judicial portal for Negotiable Instruments Act Section 138 cases.  
**Total Records:** 1,284  
**Total Raw Columns:** 4  

---

## 1. Column-by-Column Specification

| Column Name | Description | Raw Data Type | Target Data Type | Missing % | Validation Rules | Modeling Suitability |
|:---|:---|:---|:---|:---|:---|:---|
| `filingnumber` | Unique case filing identifier (e.g. `KL-000004-2025`) | `object` (string) | `string` | 0.0% | Regex pattern `^KL-\d{6}-\d{4}$`; unique per case. | Identifier only (drop before model training). Useful for temporal stratification & group splitting. |
| `filing_date` | Date the case petition was filed | `object` (string) | `datetime64[ns]` | 0.0% | Valid date; must be $\le$ `relevant_date`; between 2024 and 2026. | High. Basis for extracting temporal features (`filing_year`, `filing_month`, `filing_quarter`, `day_of_week`). |
| `case_status` | Status of the case at observation cutoff date | `object` (string) | `category` | 0.0% | Allowed values: `{'Disposed', 'Pending'}`. | High. Determines target definition: binary event indicator for survival/duration analysis (1=Disposed, 0=Pending/Censored). |
| `relevant_date` | Event date: Disposal date for disposed cases, or observation cutoff (`March 10, 2026`) for pending cases | `object` (string) | `datetime64[ns]` | 0.0% | Valid date; must be $\ge$ `filing_date`. For pending cases, fixed to observation cutoff. | High. Used to calculate observed duration / case age in days. |

---

## 2. Derived Features (Engineered for Modeling)

| Derived Feature | Formula / Definition | Target Type | Role in Machine Learning |
|:---|:---|:---|:---|
| `duration_days` | `(relevant_date - filing_date).dt.days` | `int64` | **Regression Target** (for `case_status == 'Disposed'`) / Observed exposure time. |
| `event_observed` | `1` if `case_status == 'Disposed'` else `0` | `int8` | Censoring indicator (distinguishes complete duration from right-censored pending age). |
| `filing_year` | `filing_date.dt.year` | `int16` | Cohort feature (2024, 2025, 2026). |
| `filing_month` | `filing_date.dt.month` | `int8` | Cyclical/seasonal filing trend feature. |
| `filing_day_of_week` | `filing_date.dt.dayofweek` | `int8` | Filing day (0=Monday ... 6=Sunday). |
| `case_seq_no` | Numeric sequence from `filingnumber` | `int32` | Intra-year filing volume index. |

---

## 3. Data Integrity & Validation Findings

1. **Missing Values:** Zero missing values across all 1,284 records.
2. **Duplicate Detection:** 1,284 unique `filingnumber` values. No duplicated case filings.
3. **Chronology Check:** All `relevant_date` values are chronologically after or on `filing_date` (`min_duration = 0` days, `negative_durations = 0`).
4. **Censoring Consistency:** Exactly 100% (1,006/1,006) of `Pending` cases have `relevant_date == 'March 10, 2026'`, confirming strict right-censoring at the data cutoff date.
5. **Class Breakdown:**
   - Pending: 1,006 (78.35%)
   - Disposed: 278 (21.65%)
