import numpy as np

# Constants for tax brackets and rates
FEDERAL_TAX_BRACKETS = [0, 55867, 111733, 173205, 246752]
FEDERAL_TAX_RATES = [0.15, 0.205, 0.26, 0.29, 0.33]

ONTARIO_TAX_BRACKETS = [0, 51446, 102894, 150000, 220000]
ONTARIO_TAX_RATES = [0.0505, 0.0915, 0.1116, 0.1216, 0.1316]

CPP_RATE = 0.0570  # CPP rate
EI_RATE = 0.0163  # EI rate
CPP_MAX = 3766.00  # CPP max contribution
EI_MAX = 889.54  # EI max contribution

CORPORATE_TAX_RATE = 0.12  # Corporate tax rate
DIVIDEND_TAX_RATE = 0.15  # Dividend tax rate

GST_HST_RATE = 0.13  # GST/HST rate for Ontario

HOURS_WORKED_PER_YEAR = 2000
HOURLY_RATE = 75  # Modify as needed

# Function to calculate tax for a given income using progressive brackets
def calculate_tax(income, brackets, rates):
    tax = 0
    for i in range(1, len(brackets)):
        if income > brackets[i]:
            tax += (brackets[i] - brackets[i - 1]) * rates[i - 1]
        else:
            tax += (income - brackets[i - 1]) * rates[i - 1]
            break
    return tax

# Function to calculate personal tax on salary
def calculate_personal_tax(salary):
    federal_tax = calculate_tax(salary, FEDERAL_TAX_BRACKETS, FEDERAL_TAX_RATES)
    ontario_tax = calculate_tax(salary, ONTARIO_TAX_BRACKETS, ONTARIO_TAX_RATES)
    
    cpp_contribution = min(salary * CPP_RATE, CPP_MAX)
    ei_contribution = min(salary * EI_RATE, EI_MAX)
    
    total_personal_tax = federal_tax + ontario_tax + cpp_contribution + ei_contribution
    return total_personal_tax

# Function to calculate dividend tax
def calculate_dividend_tax(dividends):
    return dividends * DIVIDEND_TAX_RATE

# Function to calculate corporate tax with tax credits
def calculate_corporate_tax(income_after_expenses):
    tax_credit = income_after_expenses * 0.05  # Assume 5% corporate tax credits
    return (income_after_expenses * CORPORATE_TAX_RATE) - tax_credit

# Function to calculate GST/HST payable and ITCs
def calculate_gst_hst(total_income, expenses):
    gst_hst_payable = total_income * GST_HST_RATE
    itc = expenses * GST_HST_RATE
    return gst_hst_payable - itc

# Total income calculation
def calculate_total_income(hourly_rate):
    return hourly_rate * HOURS_WORKED_PER_YEAR

# Main optimization function to minimize total tax
def optimize_tax(hourly_rate):
    total_income = calculate_total_income(hourly_rate)
    best_salary = 0
    best_total_tax = float('inf')
    best_split = None

    # Conservative bounds for expenses
    expense_min = 0.10 * total_income
    expense_max = 0.20 * total_income

    # Iterate over salary splits (0% to 100%) and expenses (within bounds)
    for salary_percentage in np.linspace(0, 1, 100):
        for expenses in np.linspace(expense_min, expense_max, 50):
            salary = total_income * salary_percentage
            dividends = total_income - salary - expenses
            if dividends < 0:
                continue  # Ensure dividends are non-negative

            corporate_income_after_expenses = total_income - salary - expenses
            personal_tax = calculate_personal_tax(salary)
            corporate_tax = calculate_corporate_tax(corporate_income_after_expenses)
            dividend_tax = calculate_dividend_tax(dividends)
            net_gst_hst = calculate_gst_hst(total_income, expenses)

            total_tax = personal_tax + corporate_tax + dividend_tax + net_gst_hst

            # Check if this is the best (minimized) tax liability
            if total_tax < best_total_tax:
                best_total_tax = total_tax
                best_salary = salary
                best_split = {
                    "salary": salary,
                    "dividends": dividends,
                    "expenses": expenses,
                    "personal_tax": personal_tax,
                    "corporate_tax": corporate_tax,
                    "dividend_tax": dividend_tax,
                    "net_gst_hst": net_gst_hst,
                    "total_tax": total_tax
                }

    return best_split

# Print the optimal solution
def main():
    optimal_split = optimize_tax(HOURLY_RATE)

    print("Optimal Salary/Dividend/Expense Split:")
    print(f"Salary: ${optimal_split['salary']:.2f}")
    print(f"Dividends: ${optimal_split['dividends']:.2f}")
    print(f"Expenses: ${optimal_split['expenses']:.2f}")
    print(f"Personal Tax: ${optimal_split['personal_tax']:.2f}")
    print(f"Corporate Tax: ${optimal_split['corporate_tax']:.2f}")
    print(f"Dividend Tax: ${optimal_split['dividend_tax']:.2f}")
    print(f"Net GST/HST Payable: ${optimal_split['net_gst_hst']:.2f}")
    print(f"Total Tax Liability: ${optimal_split['total_tax']:.2f}")

# Run the main function
main()
