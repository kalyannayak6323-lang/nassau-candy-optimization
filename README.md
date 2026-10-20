# Nassau Candy Optimization Recommendation System

## Project Overview
A business analytics project to evaluate customer-to-factory distances, compare factory assignments, and estimate potential transportation cost savings.

## Business Objective
Identify alternative factory assignments that may reduce estimated transportation costs while supporting efficient customer order fulfillment.

## Project Files
- `calculate_distance.py` — calculates customer-to-factory distances.
- `final_factory_analysis.py` — analyzes factory assignments and estimates transportation costs.
- `customer_data_with_coordinates.xlsx` — customer locations with coordinates.
- `customer_factory_distances.xlsx` — calculated distance data.
- `nassau_candy_distributor.xlsx` — transaction dataset.
- `final_factory_analysis.xlsx` — final analysis workbook.
- `requirements.txt` — Python dependencies.
- `index.html` — project website.

## Methodology
1. Prepare customer location and transaction data.
2. Calculate distances between customer locations and factories.
3. Match transaction records with distance data.
4. Compare current and alternative factory assignments.
5. Estimate transportation costs using the model assumption of $1 per km.
6. Calculate estimated potential savings.

## Reported Results
- Current transportation cost: $20.41 million
- Estimated optimized cost: $8.31 million
- Potential savings: $12.10 million
- Potential savings percentage: 59.28%

These are reported model estimates. Reproduce the calculations from the supplied files before treating the results as independently verified.

## Requirements
Use Python with the dependencies listed in `requirements.txt`.

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run
Place the required Excel input files in the same working directory as the scripts, matching the filenames specified in the code.

Calculate distances:

```bash
python calculate_distance.py
```

Run the factory analysis:

```bash
python final_factory_analysis.py
```

Check the script configuration and required input filenames before running. Confirm that the expected output files are generated.

## Assumptions and Limitations
- Transportation cost is modeled at $1 per km.
- Actual savings depend on freight rates, factory capacity, product availability, service levels, and operational constraints.
- Validate the output workbook and dashboard before using estimates for operational decisions.

## Power BI Report
https://app.powerbi.com/links/BoZr2PYpUU?ctid=99ad5b45-6c02-49e3-af2b-831863f2e0dc&pbi_source=linkShare
