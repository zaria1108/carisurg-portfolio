# CariSurg Portfolio Week 0 
## Tutorial 1: Data Cleaning (Gender)

### What was done
I cleaned the Gender column of the hospital triage dataset.

### The problem
The Gender column had 6 inconsistent variants:
- Male, MALE, 1 (all meaning Male)
- Female, FEMALE, 0 (all meaning Female)

### My solution
- Changed all values to lowercase
- Mapped to numeric encoding:
  - 1 = Male
  - 0 = Female
  - 2 = Non-Binary

### What I learned
- How to explore dirty data before cleaning it
- How to use .map() to standardise inconsistent values
- The importance of documenting encoding decisions


## Tutorial 2: Data Cleaning (Fio2)

### What was done
I cleaned the Fio2 (Fraction of Inspired Oxygen) column from a hospital emergency triage dataset.

### The problem
| Property | Detail |
|---|---|
| Clinical meaning | The percentage of oxygen a patient is breathing |
| Valid range | 21–100% |
| Note | 21% = room air (normal). 100% = pure oxygen via ventilator — not an outlier. |

### The solution
- 22 missing (NaN) values
- Column needed type verification and range validation
- Required clinical understanding before any cleaning decision could be made

### My Solution
1. Inspected with `unique()` and `describe()` — confirmed clean percentages, no string errors
2. Applied `pd.to_numeric(..., errors='coerce')` for pipeline consistency
3. Range filter (21–100%) — found 0 out-of-range values
4. Imputed missing values with median (21.0)
5. Added a clinical category column to classify patients by oxygen support level

### What I Learned
- How to anchor cleaning decisions in clinical knowledge, not just statistics
- The difference between a statistical outlier and a physiologically impossible value
- How to use `pd.to_numeric(..., errors='coerce')` to handle mixed-type columns
- How to justify imputation method based on data distribution
- How to add clinical meaning back to cleaned data through categorisation
