# CariSurg Portfolio

## Week 0 - Tutorial 1: Data Cleaning (Gender)

### What was done
I cleaned the Gender column from a hospital triage dataset.

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
