import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DeferredLoan:
    def __init__(self, root):
        self.root = root
        self.root.title("Lump Sum Loan Calculator")

        self.principal_var = tk.StringVar(value="1000")
        self.interest_rate_var = tk.StringVar(value="6")
        self.years_var = tk.StringVar(value="5")
        self.months_var = tk.StringVar(value="0")
        self.total_payments_var = tk.StringVar()
        self.total_interest_var = tk.StringVar()

        ttk.Label(root, text="Loan Amount").grid(column=0, row=0, sticky=tk.W)
        principal_entry = ttk.Entry(root, textvariable=self.principal_var)
        principal_entry.grid(column=1, row=0, sticky=tk.EW)

        ttk.Label(root, text="Loan Term (years)").grid(column=0, row=1, sticky=tk.W)
        years_entry = ttk.Entry(root, textvariable=self.years_var, width=5)
        years_entry.grid(column=1, row=1, sticky=tk.EW, padx=(5, 2))

        ttk.Label(root, text="Loan Term (months)").grid(column=0, row=2, sticky=tk.W)
        months_entry = ttk.Entry(root, textvariable=self.months_var, width=5)
        months_entry.grid(column=1, row=2, sticky=tk.EW, padx=(5, 2))

        ttk.Label(root, text="Interest Rate").grid(column=0, row=3, sticky=tk.W)
        interest_rate_entry = ttk.Entry(root, textvariable=self.interest_rate_var)
        interest_rate_entry.grid(column=1, row=3, sticky=tk.EW)

        calculate_button = ttk.Button(root, text="Calculate", command=self.on_calculate)
        calculate_button.grid(column=0, row=4, columnspan=2, sticky=tk.EW, pady=5)

        pie_chart_button = ttk.Button(root, text="Show Pie Chart", command=self.pie_chart)
        pie_chart_button.grid(column=0, row=5, columnspan=2, sticky=tk.EW, pady=5)

        clear_button = ttk.Button(root, text="Clear", command=self.on_clear)
        clear_button.grid(column=0, row=6, columnspan=2, sticky=tk.EW, pady=5)

        ttk.Label(root, text="Amount Due at Loan Maturity").grid(column=0, row=7, sticky=tk.W)
        ttk.Label(root, textvariable=self.total_payments_var).grid(column=1, row=7, sticky=tk.E)

        ttk.Label(root, text="Total Interest").grid(column=0, row=8, sticky=tk.W)
        ttk.Label(root, textvariable=self.total_interest_var).grid(column=1, row=8, sticky=tk.E)

        root.columnconfigure(1, weight=1)
        root.minsize(300, 250)

    def calculate_loan_details(self, principal, annual_interest_rate, years, months=0):
        total_years = years + (months / 12)
        total_paid = principal * ((1 + (annual_interest_rate / 100)) ** total_years)
        total_interest = total_paid - principal
        return total_paid, total_interest

    def on_calculate(self):
        try:
            principal = float(self.principal_var.get().replace('$', '').replace(',', ''))
            annual_interest_rate = float(self.interest_rate_var.get().strip('%'))
            years = int(self.years_var.get())
            months = int(self.months_var.get())

            total_paid, total_interest = self.calculate_loan_details(principal, annual_interest_rate, years, months)

            self.total_payments_var.set(f"${total_paid:,.2f}")
            self.total_interest_var.set(f"${total_interest:,.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def on_clear(self):
        self.principal_var.set("1000")
        self.interest_rate_var.set("6")
        self.years_var.set("5")
        self.months_var.set("0")
        self.total_payments_var.set("")
        self.total_interest_var.set("")

    def pie_chart(self):
        try:
            principal = float(self.principal_var.get().replace('$', '').replace(',', ''))
            total_interest = float(self.total_interest_var.get().replace('$', '').replace(',', ''))

            values = [principal, total_interest]
            labels = ['Principal', 'Total Interest']

            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')

            pie_chart_window = tk.Toplevel(self.root)
            pie_chart_window.title("Pie Chart")

            canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please calculate your interest first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeferredLoan(root)
    root.mainloop()
