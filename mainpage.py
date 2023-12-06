import tkinter as tk
import loanapp_updated2
import loan_calculator_piechart_three_dopdown
import deferred_loan 

def open_loan_app():
    # create a new window
    new_window = tk.Toplevel(root)
    # create an instance of the LoanApp class
    app = loanapp_updated2.LoanApp(new_window) # pass the new window as the master
    app.show() 
def open_amortized_cal():
    # create a new window
    new_window = tk.Toplevel(root)
    app = loan_calculator_piechart_three_dopdown.LoanCalculatorApp(new_window) # pass the new window as the master
    app.show() 
def open_deferred_loan():
    # create a new window
    new_window = tk.Toplevel(root)
    # create an instance of the LoanApp class
    app = deferred_loan.DeferredLoan(new_window) # pass the new window as the master
    app.show() 

# create the main window for showing three buttons
root = tk.Tk()
root.title("Loan Calculator")
root.geometry("300x300")

#Button for Amortized Loan Calculator
button = tk.Button(root, text="Open Amortized Loan Calculator", command=open_amortized_cal)
button.pack(pady=10)

#Button for Deferred Payment Loan Calculator
button = tk.Button(root, text="Open Deferred Payment Loan Calculator", command=open_deferred_loan)
button.pack(pady=10)

#Button for Bond Calculator
button = tk.Button(root, text="Open Bond Calculator", command=open_loan_app)
button.pack(pady=10)



# start the main loop
root.mainloop()
