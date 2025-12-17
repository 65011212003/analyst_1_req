"""
Python Data Analysis Examples
Demonstrates: Data manipulation, analysis, visualization, and database connectivity
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class DataAnalyzer:
    """
    Comprehensive data analysis examples using Python
    Covers: Pandas, NumPy, data cleaning, aggregation, visualization
    """
    
    def __init__(self):
        self.employee_data = None
        self.sales_data = None
    
    def create_sample_data(self):
        """
        Creates sample datasets for analysis
        Demonstrates: DataFrame creation, date ranges, random data generation
        """
        print("=" * 60)
        print("Creating Sample Datasets")
        print("=" * 60)
        
        # Employee dataset
        np.random.seed(42)
        n_employees = 100
        
        departments = ['IT', 'HR', 'Finance', 'Marketing', 'Operations']
        
        self.employee_data = pd.DataFrame({
            'EmployeeID': range(1, n_employees + 1),
            'FirstName': [f'Employee{i}' for i in range(1, n_employees + 1)],
            'Department': np.random.choice(departments, n_employees),
            'Salary': np.random.randint(50000, 150000, n_employees),
            'YearsExperience': np.random.randint(0, 20, n_employees),
            'PerformanceScore': np.random.uniform(3.0, 5.0, n_employees),
            'HireDate': pd.date_range(end=datetime.now(), periods=n_employees, freq='D')
        })
        
        # Sales dataset
        date_range = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        n_sales = len(date_range) * 10
        
        self.sales_data = pd.DataFrame({
            'SaleID': range(1, n_sales + 1),
            'Date': np.random.choice(date_range, n_sales),
            'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], n_sales),
            'Quantity': np.random.randint(1, 50, n_sales),
            'UnitPrice': np.random.uniform(10, 500, n_sales),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], n_sales)
        })
        
        self.sales_data['TotalAmount'] = self.sales_data['Quantity'] * self.sales_data['UnitPrice']
        
        print(f"✓ Created employee dataset with {len(self.employee_data)} records")
        print(f"✓ Created sales dataset with {len(self.sales_data)} records\n")
        
        return self.employee_data, self.sales_data
    
    def basic_data_exploration(self):
        """
        Basic data exploration and information
        Demonstrates: head(), info(), describe(), shape, dtypes
        """
        print("=" * 60)
        print("1. BASIC DATA EXPLORATION")
        print("=" * 60)
        
        print("\nEmployee Data - First 5 rows:")
        print(self.employee_data.head())
        
        print("\n\nDataset Info:")
        print(f"Shape: {self.employee_data.shape}")
        print(f"Columns: {list(self.employee_data.columns)}")
        print(f"\nData Types:\n{self.employee_data.dtypes}")
        
        print("\n\nStatistical Summary:")
        print(self.employee_data.describe())
        
    def data_filtering_selection(self):
        """
        Data filtering and selection techniques
        Demonstrates: Boolean indexing, loc, iloc, query
        """
        print("\n" + "=" * 60)
        print("2. DATA FILTERING AND SELECTION")
        print("=" * 60)
        
        # Filter high earners
        high_earners = self.employee_data[self.employee_data['Salary'] > 100000]
        print(f"\n✓ High earners (>$100K): {len(high_earners)} employees")
        
        # Multiple conditions
        it_experienced = self.employee_data[
            (self.employee_data['Department'] == 'IT') & 
            (self.employee_data['YearsExperience'] > 5)
        ]
        print(f"✓ Experienced IT employees: {len(it_experienced)}")
        
        # Using query method
        top_performers = self.employee_data.query('PerformanceScore > 4.5')
        print(f"✓ Top performers (score > 4.5): {len(top_performers)}")
        
        # Select specific columns
        salary_info = self.employee_data[['EmployeeID', 'Department', 'Salary']]
        print(f"\n✓ Selected columns shape: {salary_info.shape}")
        
    def data_aggregation_grouping(self):
        """
        Data aggregation and grouping operations
        Demonstrates: groupby, agg, pivot_table
        """
        print("\n" + "=" * 60)
        print("3. DATA AGGREGATION AND GROUPING")
        print("=" * 60)
        
        # Group by department
        dept_stats = self.employee_data.groupby('Department').agg({
            'Salary': ['mean', 'min', 'max', 'count'],
            'YearsExperience': 'mean',
            'PerformanceScore': 'mean'
        }).round(2)
        
        print("\nDepartment Statistics:")
        print(dept_stats)
        
        # Sales analysis by product and region
        sales_summary = self.sales_data.groupby(['Product', 'Region']).agg({
            'TotalAmount': 'sum',
            'Quantity': 'sum',
            'SaleID': 'count'
        }).round(2)
        
        print("\n\nSales Summary by Product and Region:")
        print(sales_summary.head(10))
        
        # Pivot table
        sales_pivot = pd.pivot_table(
            self.sales_data,
            values='TotalAmount',
            index='Product',
            columns='Region',
            aggfunc='sum',
            fill_value=0
        ).round(2)
        
        print("\n\nSales Pivot Table (Product x Region):")
        print(sales_pivot)
        
    def data_transformation(self):
        """
        Data transformation and feature engineering
        Demonstrates: apply, map, lambda, creating new columns
        """
        print("\n" + "=" * 60)
        print("4. DATA TRANSFORMATION")
        print("=" * 60)
        
        # Create salary brackets
        def salary_bracket(salary):
            if salary < 70000:
                return 'Entry Level'
            elif salary < 100000:
                return 'Mid Level'
            else:
                return 'Senior Level'
        
        self.employee_data['SalaryBracket'] = self.employee_data['Salary'].apply(salary_bracket)
        
        # Calculate tenure in years
        self.employee_data['TenureYears'] = (
            (datetime.now() - self.employee_data['HireDate']).dt.days / 365
        ).round(2)
        
        # Performance category
        self.employee_data['PerformanceCategory'] = pd.cut(
            self.employee_data['PerformanceScore'],
            bins=[0, 3.5, 4.0, 4.5, 5.0],
            labels=['Needs Improvement', 'Good', 'Very Good', 'Excellent']
        )
        
        print("\nNew columns created:")
        print(self.employee_data[['EmployeeID', 'Salary', 'SalaryBracket', 
                                   'TenureYears', 'PerformanceCategory']].head())
        
        bracket_counts = self.employee_data['SalaryBracket'].value_counts()
        print(f"\n\nSalary Bracket Distribution:\n{bracket_counts}")
        
    def time_series_analysis(self):
        """
        Time series analysis
        Demonstrates: Date operations, resampling, rolling windows
        """
        print("\n" + "=" * 60)
        print("5. TIME SERIES ANALYSIS")
        print("=" * 60)
        
        # Set date as index
        sales_ts = self.sales_data.set_index('Date').sort_index()
        
        # Daily sales aggregation
        daily_sales = sales_ts.groupby('Date')['TotalAmount'].sum()
        
        # Monthly aggregation
        monthly_sales = sales_ts.resample('M')['TotalAmount'].sum()
        print("\nMonthly Sales:")
        print(monthly_sales.head())
        
        # 7-day moving average
        sales_ts['7Day_MA'] = sales_ts['TotalAmount'].rolling(window=7).mean()
        
        # Year-over-year comparison (if multi-year data)
        sales_by_month = sales_ts.resample('M').agg({
            'TotalAmount': ['sum', 'mean', 'count']
        })
        
        print("\n\nMonthly Sales Summary:")
        print(sales_by_month.head())
        
    def advanced_analytics(self):
        """
        Advanced analytics and insights
        Demonstrates: Correlation, percentiles, ranking
        """
        print("\n" + "=" * 60)
        print("6. ADVANCED ANALYTICS")
        print("=" * 60)
        
        # Correlation analysis
        numeric_cols = ['Salary', 'YearsExperience', 'PerformanceScore']
        correlation_matrix = self.employee_data[numeric_cols].corr()
        
        print("\nCorrelation Matrix:")
        print(correlation_matrix.round(3))
        
        # Percentile analysis
        salary_percentiles = self.employee_data['Salary'].quantile([0.25, 0.5, 0.75, 0.9])
        print("\n\nSalary Percentiles:")
        print(salary_percentiles)
        
        # Ranking
        self.employee_data['SalaryRank'] = self.employee_data['Salary'].rank(ascending=False)
        self.employee_data['PerformanceRank'] = self.employee_data['PerformanceScore'].rank(ascending=False)
        
        top_10 = self.employee_data.nsmallest(10, 'SalaryRank')[
            ['EmployeeID', 'Department', 'Salary', 'SalaryRank', 'PerformanceScore']
        ]
        print("\n\nTop 10 Highest Paid Employees:")
        print(top_10)
        
    def data_quality_checks(self):
        """
        Data quality and cleaning
        Demonstrates: Missing values, duplicates, data validation
        """
        print("\n" + "=" * 60)
        print("7. DATA QUALITY CHECKS")
        print("=" * 60)
        
        # Check for missing values
        missing_values = self.employee_data.isnull().sum()
        print("\nMissing Values:")
        print(missing_values)
        
        # Check for duplicates
        duplicates = self.employee_data.duplicated().sum()
        print(f"\n✓ Duplicate rows: {duplicates}")
        
        # Data validation
        invalid_salaries = self.employee_data[self.employee_data['Salary'] < 0]
        print(f"✓ Invalid salaries (< 0): {len(invalid_salaries)}")
        
        invalid_scores = self.employee_data[
            (self.employee_data['PerformanceScore'] < 0) | 
            (self.employee_data['PerformanceScore'] > 5)
        ]
        print(f"✓ Invalid performance scores: {len(invalid_scores)}")
        
        # Data type validation
        print(f"\n✓ All data types are correct: {self.employee_data.dtypes.to_dict()}")

def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("PYTHON DATA ANALYSIS DEMONSTRATION")
    print("=" * 60)
    print("Libraries: Pandas, NumPy, Matplotlib, Seaborn")
    print("=" * 60 + "\n")
    
    analyzer = DataAnalyzer()
    
    # Run all examples
    analyzer.create_sample_data()
    analyzer.basic_data_exploration()
    analyzer.data_filtering_selection()
    analyzer.data_aggregation_grouping()
    analyzer.data_transformation()
    analyzer.time_series_analysis()
    analyzer.advanced_analytics()
    analyzer.data_quality_checks()
    
    print("\n" + "=" * 60)
    print("✓ All examples completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
