# Clinical Data Quality Report

## 1. Project Overview

This report summarizes data quality checks performed on a synthetic clinical study dataset using Python and pandas.

## 2. Dataset Summary

- Total records: 100
- Total variables: 12
- Data source: Synthetic data created for educational purposes

## 3. Validation Approach

Twelve edit checks were implemented to identify missing subject identifiers and dates, duplicate subject IDs, date chronology issues, non-standard demographic coding, and values outside the project's assumed validation ranges.

## 4. Results

- Total discrepancy records: 20
- Unique subjects affected: 19
- Edit checks implemented: 12
- Edit checks with findings: 11

EC01 identified no missing Subject IDs. Findings were recorded for EC02 through EC12.

### Findings by Edit Check

| Check ID | Discrepancy Records |
|---|---:|
| EC02 | 2 |
| EC03 | 1 |
| EC04 | 1 |
| EC05 | 1 |
| EC06 | 2 |
| EC07 | 3 |
| EC08 | 2 |
| EC09 | 3 |
| EC10 | 2 |
| EC11 | 1 |
| EC12 | 2 |

## 5. Discrepancy Management

Findings were recorded in a discrepancy log containing the subject identifier, check ID, variable, observed value, issue description, and draft site query. The log is intended to support review and clarification. Values were not automatically corrected.

## 6. Limitations

- All records are synthetic and do not represent a real clinical trial.
- Validation ranges are assumed rules for this portfolio exercise, not universal clinical reference ranges.
- An out-of-range value is a signal for investigation, not proof that the value is incorrect.
- Potential unit inconsistencies require confirmation before conversion.
- A discrepancy record is not necessarily a unique subject.
- Draft site queries are examples and have not been sent to actual study sites.

## 7. Conclusion

The workflow processed 100 synthetic records and generated 20 discrepancy records affecting 19 unique subjects. The project demonstrates a basic approach to clinical data validation, discrepancy identification, and query documentation using Python and pandas.

## 8. Tools

- Python
- pandas
- Google Colab
- Microsoft Excel
- GitHub

## 9. Data Privacy

No real patient data were used. All data were generated for educational and portfolio purposes.

Report generated: 2026-10-21