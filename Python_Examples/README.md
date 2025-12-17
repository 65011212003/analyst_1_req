# Python Examples

This folder contains comprehensive Python programming examples covering data analysis, database connectivity, and more.

## Files

### 1. data_analysis.py
Comprehensive data analysis using Pandas and NumPy
- DataFrame creation and manipulation
- Data filtering and selection
- Aggregation and grouping
- Time series analysis
- Statistical analysis
- Data quality checks

### 2. database_connectivity.py
Database operations with SQL Server
- Connection management (pyodbc)
- CRUD operations
- Parameterized queries
- Stored procedure calls
- Pandas integration
- Bulk data operations

### 3. requirements.txt
Required Python packages

## Prerequisites

```bash
pip install -r requirements.txt
```

## Required Packages

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **pyodbc** - SQL Server connectivity
- **matplotlib** - Data visualization
- **seaborn** - Statistical visualization

## Running the Examples

```bash
# Data analysis examples
python data_analysis.py

# Database connectivity examples
python database_connectivity.py
```

## Key Concepts Covered

### Pandas Operations
- DataFrame creation and manipulation
- Filtering with boolean indexing
- GroupBy operations
- Pivot tables
- Time series analysis
- Data cleaning

### NumPy Operations
- Array creation
- Random number generation
- Statistical functions
- Mathematical operations

### Database Operations
- Connection management
- Parameterized queries (SQL injection prevention)
- CRUD operations
- Stored procedures
- Transaction handling
- Bulk operations

### Best Practices
1. ✅ Use parameterized queries to prevent SQL injection
2. ✅ Proper resource management (connections, cursors)
3. ✅ Error handling and transactions
4. ✅ Efficient data operations
5. ✅ Code documentation
6. ✅ Type hints and clear variable names

## Learning Path

1. Start with `data_analysis.py` to learn Pandas basics
2. Move to `database_connectivity.py` for database integration
3. Practice modifying the examples
4. Create your own analysis projects

## Common Use Cases

- **Data Analysis**: Analyze business data, create reports
- **Database Integration**: ETL operations, data migration
- **Reporting**: Generate automated reports
- **Data Quality**: Validate and clean datasets
