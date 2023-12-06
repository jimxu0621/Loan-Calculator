import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LoanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Calculator")

        # Variables for input fields with default values
        self.default_due_amount = 100000.0
        self.default_interest_rate = 6.0
        self.default_loan_years = 10
        self.default_loan_months = 0
        self.default_compound_frequency = "Monthly"

        # Use StringVar for due_amount to allow formatting with commas
        self.due_amount_var = tk.StringVar(value=f"{self.default_due_amount:,.2f}")
        self.interest_rate_var = tk.StringVar(value=f"{self.default_interest_rate:.2f}")
        self.loan_years_var = tk.StringVar(value=str(self.default_loan_years))
        self.loan_months_var = tk.StringVar(value=str(self.default_loan_months))
        self.compound_frequency_var = tk.StringVar(value=self.default_compound_frequency)

        # Create and place input fields, results, and pie chart
        self.create_widgets()

    def create_widgets(self):
        # Create frame for input fields and results
        input_frame = ttk.Frame(self.root)
        input_frame.pack(side=tk.LEFT, padx=5, pady=5)

        # Input fields
        tk.Label(input_frame, text="Amount Due ($):", font=('Menlo', 12)).grid(row=0, column=0, sticky=tk.W)
        entry_due_amount = tk.Entry(input_frame, textvariable=self.due_amount_var, font=('Menlo', 12))
        entry_due_amount.grid(row=0, column=1, sticky=tk.W)

        tk.Label(input_frame, text="Interest Rate (%):", font=('Menlo', 12)).grid(row=1, column=0, sticky=tk.W)
        entry_interest_rate = tk.Entry(input_frame, textvariable=self.interest_rate_var, font=('Menlo', 12))
        entry_interest_rate.grid(row=1, column=1, sticky=tk.W)

        tk.Label(input_frame, text="Loan Term:", font=('Menlo', 12)).grid(row=2, column=0, sticky=tk.W)
        entry_loan_years = tk.Entry(input_frame, textvariable=self.loan_years_var, width=3, font=('Menlo', 12))
        entry_loan_years.grid(row=2, column=1, sticky=tk.EW)
        tk.Label(input_frame, text="Years", font=('Menlo', 12)).grid(row=2, column=2, sticky=tk.W, padx=(2, 2))

        entry_loan_months = tk.Entry(input_frame, textvariable=self.loan_months_var, width=3, font=('Menlo', 12))
        entry_loan_months.grid(row=2, column=3, sticky=tk.W)
        tk.Label(input_frame, text="Months", font=('Menlo', 12)).grid(row=2, column=4, sticky=tk.W)

        tk.Label(input_frame, text="Compound Frequency:", font=('Menlo', 12)).grid(row=3, column=0, sticky=tk.W)
        combobox_compound_frequency = ttk.Combobox(input_frame, values=["Monthly", "Quarterly", "Annually"],
                                                   textvariable=self.compound_frequency_var, font=('Menlo', 12))
        combobox_compound_frequency.grid(row=3, column=1, columnspan=4, sticky=tk.W)

        # Results labels
        self.result_label_1 = tk.Label(input_frame, text="", font=('Menlo', 12))
        self.result_label_1.grid(row=4, column=0, columnspan=5, pady=5, sticky=tk.EW)
        self.result_label_2 = tk.Label(input_frame, text="", font=('Menlo', 12))
        self.result_label_2.grid(row=5, column=0, columnspan=5, pady=5, sticky=tk.EW)

        # Calculate and Reset buttons
        self.calculate_button = tk.Button(input_frame, text="Calculate", command=self.calculate, font=('Menlo', 12))
        self.calculate_button.grid(row=6, column=0, columnspan=5, pady=2, sticky=tk.EW)

        self.reset_button = tk.Button(input_frame, text="Reset", command=self.reset_defaults, font=('Menlo', 12))
        self.reset_button.grid(row=7, column=0, columnspan=5, pady=2, sticky=tk.EW)

        # Create and place matplotlib figure for the pie chart
        self.figure, self.ax = Figure(), None
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, padx=5, pady=5)

        # Trace changes in the due_amount_var and format with commas
        self.due_amount_var.trace_add('write', self.format_due_amount)

    def format_due_amount(self, *args):
        # Remove commas and format as a float
        input_value = self.due_amount_var.get().replace(',', '')
        try:
            float_value = float(input_value)
        except ValueError:
            float_value = 0.0
        # Update the variable with the formatted string
        self.due_amount_var.set(f"{float_value:,.2f}")

    def calculate(self):
        # Check for blank or invalid input fields
        if not self.validate_input():
            return

        due_amount = float(self.due_amount_var.get().replace(',', ''))
        interest_rate = float(self.interest_rate_var.get()) / 100 / 12
        loan_years = int(self.loan_years_var.get())
        loan_months = int(self.loan_months_var.get())
        compound_frequency = self.compound_frequency_var.get()

        # Calculate total loan term in months
        loan_term = loan_years * 12 + loan_months

        # Adjust interest rate based on compound frequency
        if compound_frequency == "Quarterly":
            interest_rate /= 4
        elif compound_frequency == "Annually":
            interest_rate /= 12

        # Calculate amount received when the loan starts
        amount_received_at_start = due_amount / (1 + interest_rate) ** loan_term

        # Calculate monthly payment
        monthly_payment = due_amount * (interest_rate / (1 - (1 + interest_rate) ** -loan_term))
        #monthly_payment = due_amount / ((1 + interest_rate) ** loan_term)

        # Calculate interest and principal amounts
        total_payment = monthly_payment * loan_term
        interest_paid = total_payment - due_amount
        principal_paid = due_amount

        # Display results
        self.result_label_1.config(text=f"Amount Received at Start: ${amount_received_at_start:.2f}")
        self.result_label_2.config(text=f"Total Interest Paid: ${interest_paid:.2f}")

        # Display the pie chart
        self.display_pie_chart(principal_paid, interest_paid)

    def validate_input(self):
        # Check for blank or invalid input fields
        if not self.due_amount_var.get() or not self.interest_rate_var.get() or not self.loan_years_var.get():
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return False

        try:
            # Check if the values are valid numeric types
            float(self.due_amount_var.get().replace(',', ''))
            float(self.interest_rate_var.get())
            int(self.loan_years_var.get())
            int(self.loan_months_var.get())
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")
            return False

    def reset_defaults(self):
        # Reset input fields to default values
        self.due_amount_var.set(f"{self.default_due_amount:,.2f}")  # Reset with commas
        self.interest_rate_var.set(f"{self.default_interest_rate:.2f}")
        self.loan_years_var.set(str(self.default_loan_years))
        self.loan_months_var.set(str(self.default_loan_months))
        self.compound_frequency_var.set(self.default_compound_frequency)

        # Clear result labels
        self.result_label_1.config(text="")
        self.result_label_2.config(text="")

        # Reset the pie chart
        self.display_pie_chart(0, 0)

    def display_pie_chart(self, principal_paid, interest_paid):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        labels = ['Principal', 'Interest']
        sizes = [principal_paid, interest_paid]
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=50)
        self.ax.axis('equal')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanApp(root)
    root.mainloop()
