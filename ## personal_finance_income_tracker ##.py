# personal_finance_income_tracker.py
# Author: Aminat Rahim
# Date written: 04-06-2025
# Purpose: A Python Tkinter GUI application for tracking personal finance income.

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ===============================
# Data Storage and Retrieval
# ===============================
INCOME_FILE = "income_data.txt"

def save_income(income_details):
    with open(INCOME_FILE, "a", encoding="utf-8") as f:
        f.write(income_details + "\n")

def get_income():
    try:
        with open(INCOME_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []

def analyze_income():
    incomes = get_income()
    sources = []
    amounts = []
    for income in incomes:
        try:
            parts = income.split(", ")
            source = parts[0].split(": ")[1]
            amount = float(parts[1].split(": ")[1])
            sources.append(source)
            amounts.append(amount)
        except (IndexError, ValueError):
            print(f"Skipping invalid income entry: {income}")
            continue
    return sources, amounts

# ===============================
# Main Application Class
# ===============================
class IncomeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Income Tracker")
        self.root.geometry("600x400")
        self.display_image(
            "https://thumbs.dreamstime.com/b/growing-money-plant-coins-finance-investment-concept-generative-ai-business-274026331.jpg",
            alt_text="Finance Logo",
            size=(150, 150),
        )
        self.create_main_menu()

    def display_image(self, url, alt_text="", size=(50, 50)):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize(size, Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.root, image=img_tk)
            label.image = img_tk
            label.pack(pady=10)
            label.tooltip_text = alt_text
        except Exception as e:
            print(f"Image error: {e}")
            tk.Label(self.root, text=f"[{alt_text}]").pack(pady=10)

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Personal Finance Income Tracker", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Track your income!", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Enter Income", width=25, command=self.enter_income).pack(pady=10)
        tk.Button(self.root, text="View Income", width=25, command=self.view_income).pack(pady=10)
        tk.Button(self.root, text="Analyze Income", width=25, command=self.analyze_income_data).pack(pady=10)
        tk.Button(self.root, text="Exit", width=25, command=self.exit_app).pack(pady=10)

    def enter_income(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Income", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Source:").pack()
        source_entry = tk.Entry(self.root)
        source_entry.pack()
        tk.Label(self.root, text="Amount ($):").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()
        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()
        tk.Button(self.root, text="Save Income", command=lambda: self.save_income(source_entry, amount_entry, date_entry)).pack(pady=15)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)

    def save_income(self, source_entry, amount_entry, date_entry):
        source = source_entry.get().strip()
        amount_str = amount_entry.get().strip()
        date_str = date_entry.get().strip()

        if not source or not amount_str or not date_str:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid amount: {e}")
            return

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        income_details = f"Source: {source}, Amount: {amount:.2f}, Date: {date_str}"
        save_income(income_details)
        messagebox.showinfo("Saved", f"Your income has been saved!\n{income_details}")
        self.create_main_menu()

    def view_income(self):
        self.clear_window()
        tk.Label(self.root, text="Recorded Income", font=("Arial", 16)).pack(pady=10)
        incomes = get_income()
        if not incomes:
            tk.Label(self.root, text="No income has been recorded yet.").pack(pady=10)
        else:
            text_area = tk.Text(self.root, width=50, height=15, wrap=tk.WORD)
            text_area.pack(pady=10)
            for income in incomes:
                text_area.insert(tk.END, income + "\n")
            text_area.config(state=tk.DISABLED)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=15)

    def analyze_income_data(self):
        self.clear_window()
        tk.Label(self.root, text="Income Analysis", font=("Arial", 16)).pack(pady=10)
        sources, amounts = analyze_income()
        if not sources:
            tk.Label(self.root, text="No income data available for analysis.").pack(pady=10)
            tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=15)
            return
        fig, ax = plt.subplots()
        ax.bar(sources, amounts)
        ax.set_xlabel("Income Source")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Income by Source")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        widget = canvas.get_tk_widget()
        widget.pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=15)

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ===============================
# Run the Application
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = IncomeTrackerApp(root)
    root.mainloop()
