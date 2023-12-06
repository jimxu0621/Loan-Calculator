import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LoanCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Amortized Loan Calculator")

        # Define StringVars
        self.principal_var = tk.StringVar(value="$100,000")
        self.interest_rate_var = tk.StringVar(value="6%")
        self.years_var = tk.StringVar(value="10")
        self.months_var = tk.StringVar(value="0")
        self.compound_var = tk.StringVar(value="Monthly (APR)")
        self.payback_var = tk.StringVar(value="Every Month")
        self.monthly_payment_var = tk.StringVar()
        self.total_payments_var = tk.StringVar()
        self.total_interest_var = tk.StringVar()

        # Create the layout
        ttk.Label(root, text="Loan Amount").grid(column=0, row=0, sticky=tk.W)
        principal_entry = ttk.Entry(root, textvariable=self.principal_var)
        principal_entry.grid(column=1, row=0, sticky=tk.EW)

        # Loan Term
        ttk.Label(root, text="Loan Term").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        # Years Entry
        years_entry = ttk.Entry(root, textvariable=self.years_var, width=5)
        years_entry.grid(column=1, row=1, sticky=tk.EW, padx=(5, 2))

        # Years Label
        ttk.Label(root, text="years").grid(column=2, row=1, sticky=tk.W, padx=(2, 5))

        # Months Entry
        months_entry = ttk.Entry(root, textvariable=self.months_var, width=5)
        months_entry.grid(column=3, row=1, sticky=tk.EW, padx=(5, 2))

        # Months Label
        ttk.Label(root, text="months").grid(column=4, row=1, sticky=tk.W, padx=(2, 5))

        ttk.Label(root, text="Interest Rate").grid(column=0, row=2, sticky=tk.W)
        interest_rate_entry = ttk.Entry(root, textvariable=self.interest_rate_var)
        interest_rate_entry.grid(column=1, row=2, sticky=tk.EW)

        # Compound Dropdown Menu
        ttk.Label(root, text="Compound").grid(column=0, row=3, sticky=tk.W)
        compound_options = ['Annually', 'Quarterly', 'Monthly']
        self.compound_dropdown = ttk.Combobox(root, textvariable=self.compound_var, values=compound_options, state='readonly')
        self.compound_dropdown.grid(column=1, row=3, sticky=tk.EW)
        self.compound_dropdown.current(2)  
        compound_dropdown = ttk.Combobox(root, textvariable=self.compound_var, values=compound_options, state='readonly')
        compound_dropdown.grid(column=1, row=3, sticky=tk.EW)

        # Pay Back Dropdown Menu
        ttk.Label(root, text="Pay Back").grid(column=0, row=4, sticky=tk.W)
        payback_options = ['Every Month']
        payback_dropdown = ttk.Combobox(root, textvariable=self.payback_var, values=payback_options, state='readonly')
        payback_dropdown.grid(column=1, row=4, sticky=tk.EW)

        # Buttons
        calculate_button = ttk.Button(root, text="Calculate", command=self.on_calculate)
        calculate_button.grid(column=0, row=5, columnspan=2, sticky=tk.EW, pady=5)

        clear_button = ttk.Button(root, text="Clear", command=self.on_clear)
        clear_button.grid(column=0, row=6, columnspan=2, sticky=tk.EW, pady=5)

        # Results
        ttk.Label(root, text="Payment Every Month:").grid(column=0, row=7, sticky=tk.W)
        ttk.Label(root, textvariable=self.monthly_payment_var).grid(column=1, row=7, sticky=tk.E)

        ttk.Label(root, text="Total of Payments:").grid(column=0, row=8, sticky=tk.W)
        ttk.Label(root, textvariable=self.total_payments_var).grid(column=1, row=8, sticky=tk.E)

        ttk.Label(root, text="Total Interest:").grid(column=0, row=9, sticky=tk.W)
        ttk.Label(root, textvariable=self.total_interest_var).grid(column=1, row=9, sticky=tk.E)

        # Configure the grid
        root.columnconfigure(1, weight=1)

        # Set minimum size of the window
        root.minsize(300, 250)

        # Run the application
        root.mainloop()

    # Function to calculate the loan details
    def calculate_loan_details(self, principal, annual_interest_rate, years, months=0):
        # Determine the number of compounding periods per year
        compound_frequency = {'Annually': 1, 'Quarterly': 4, 'Monthly': 12}
        periods = compound_frequency[self.compound_var.get()]

        monthly_interest_rate = (annual_interest_rate / 100) / periods
        total_payments = (years * periods) + (months if periods == 12 else 0)
        monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
        
        total_paid = monthly_payment * total_payments
        total_interest = total_paid - principal
        return monthly_payment, total_paid, total_interest

    # Function to handle the calculate button click
    def on_calculate(self):
        
        principal = float(self.principal_var.get().replace('$', '').replace(',', ''))
        annual_interest_rate = float(self.interest_rate_var.get().strip('%'))
        years = int(self.years_var.get())
        months = int(self.months_var.get())

        monthly_payment, total_paid, total_interest = self.calculate_loan_details(principal, annual_interest_rate, years, months)
            
        self.monthly_payment_var.set(f"${monthly_payment:,.2f}")
        self.total_payments_var.set(f"${total_paid:,.2f}")
        self.total_interest_var.set(f"${total_interest:,.2f}")
            
            # Update the pie chart
        self.display_pie_chart()
     

    # Function to handle the clear button click
    def on_clear(self):
        self.principal_var.set("$100,000")
        self.interest_rate_var.set("6%")
        self.years_var.set("10")
        self.months_var.set("0")
        self.compound_var.set("Monthly (APR)")
        self.payback_var.set("Every Month")
        self.monthly_payment_var.set("")
        self.total_payments_var.set("")
        self.total_interest_var.set("")

    def display_pie_chart(self):
        principal_str = self.principal_var.get().replace('$', '').replace(',', '')
        total_interest_str = self.total_interest_var.get().replace('$', '').replace(',', '')
        
        # Check if both values are available
        if principal_str and total_interest_str:
            principal = float(principal_str)
            total_interest = float(total_interest_str)
            
            # Create a pie chart data
            values = [principal, total_interest]
            labels = ['Principal', 'Total Interest']
            # Create a Matplotlib figure and axes
            fig, ax = plt.subplots()
            # Plot the pie chart
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            # Set aspect ratio to be equal so that pie is drawn as a circle
            ax.axis('equal')
            # Create a Tkinter canvas and add the Matplotlib figure in it
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            # Place the canvas in the Tkinter window
            canvas.get_tk_widget().grid(column=0, row=10, columnspan=2, sticky=tk.EW, pady=5)
        else:
            messagebox.showerror("Invalid Input", "Please calculate your interest first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoanCalculatorApp(root)
    root.mainloop()
