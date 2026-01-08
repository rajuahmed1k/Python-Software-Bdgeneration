import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import json
import os

class ProBusinessApp2026:
    def _init_(self, root):
        self.root = root
        self.root.title("Pro Order Manager v2.0")
        self.root.geometry("600x850")
        self.root.configure(bg="#eceff1")

        self.db_file = "orders_data.json"
        self.all_data = self.load_data()
        
        # UI Header
        header = tk.Frame(root, bg="#263238", height=80)
        header.pack(fill="x")
        tk.Label(header, text="বিজনেস ড্যাশবোর্ড ২০২৬", font=("Arial", 18, "bold"), fg="white", bg="#263238").pack(pady=20)

        # Dashboard Stats
        self.stat_frame = tk.Frame(root, bg="#eceff1")
        self.stat_frame.pack(pady=10)
        self.update_dashboard()

        # Input Section
        input_box = tk.LabelFrame(root, text=" নতুন এন্ট্রি যোগ করুন ", font=("Arial", 10, "bold"), bg="white", padx=15, pady=15)
        input_box.pack(pady=10, padx=20, fill="x")

        tk.Label(input_box, text="কাস্টমার নাম:", bg="white").grid(row=0, column=0, sticky="w")
        self.name_ent = tk.Entry(input_box, width=25)
        self.name_ent.grid(row=0, column=1, pady=5)

        tk.Label(input_box, text="অর্ডার টাইপ:", bg="white").grid(row=1, column=0, sticky="w")
        self.type_ent = ttk.Combobox(input_box, values=["Delivery", "Return"], state="readonly", width=22)
        self.type_ent.current(0)
        self.type_ent.grid(row=1, column=1, pady=5)

        tk.Label(input_box, text="টাকার পরিমাণ:", bg="white").grid(row=2, column=0, sticky="w")
        self.amt_ent = tk.Entry(input_box, width=25)
        self.amt_ent.grid(row=2, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(root, bg="#eceff1")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="এন্ট্রি সেভ করুন", command=self.add_entry, bg="#43a047", fg="white", width=15, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Excel ডাউনলোড", command=self.export_excel, bg="#1e88e5", fg="white", width=15, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        
        # Delete Section
        delete_frame = tk.Frame(root, bg="#eceff1")
        delete_frame.pack(pady=5)
        tk.Label(delete_frame, text="মুছুন (SL):", bg="#eceff1").grid(row=0, column=0)
        self.del_ent = tk.Entry(delete_frame, width=5)
        self.del_ent.grid(row=0, column=1, padx=5)
        tk.Button(delete_frame, text="Delete", command=self.delete_entry, bg="#e53935", fg="white").grid(row=0, column=2)

        # Data Display
        self.display = tk.Text(root, height=15, width=70, font=("Courier New", 9), state='disabled', bg="#ffffff")
        self.display.pack(pady=10, padx=10)

        self.refresh_display()

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def save_to_file(self):
        with open(self.db_file, "w") as f:
            json.dump(self.all_data, f)

    def update_dashboard(self):
        for widget in self.stat_frame.winfo_children():
            widget.destroy()
        
        deliv = sum(d['Amount'] for d in self.all_data if d['Type'] == "Delivery")
        ret = sum(d['Amount'] for d in self.all_data if d['Type'] == "Return")
        
        tk.Label(self.stat_frame, text=f"মোট ডেলিভারি: {deliv} TK", font=("Arial", 10, "bold"), fg="#2e7d32", padx=10).grid(row=0, column=0)
        tk.Label(self.stat_frame, text=f"মোট রিটার্ন: {ret} TK", font=("Arial", 10, "bold"), fg="#c62828", padx=10).grid(row=0, column=1)
        tk.Label(self.stat_frame, text=f"নিট ক্যাশ: {deliv-ret} TK", font=("Arial", 10, "bold"), fg="#1565c0", padx=10).grid(row=0, column=2)

    def add_entry(self):
        name, o_type, amt = self.name_ent.get(), self.type_ent.get(), self.amt_ent.get()
        if not name or not amt:
            messagebox.showwarning("Warning", "সব তথ্য দিন!")
            return
        
        try:
            val = float(amt)
            sl = len(self.all_data) + 1
            date = datetime.now().strftime("%d/%m %H:%M")
            self.all_data.append({"SL": sl, "Date": date, "Name": name, "Type": o_type, "Amount": val})
            self.save_to_file()
            self.refresh_display()
            self.update_dashboard()
            self.name_ent.delete(0, tk.END)
            self.amt_ent.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "টাকা সঠিক সংখ্যায় লিখুন")

    def delete_entry(self):
        sl = self.del_ent.get()
        if sl:
            self.all_data = [d for d in self.all_data if str(d['SL']) != sl]
            # রে-ইনডেক্সিং সিরিয়াল
            for i, d in enumerate(self.all_data): d['SL'] = i + 1
            self.save_to_file()
            self.refresh_display()
            self.update_dashboard()
            self.del_ent.delete(0, tk.END)

    def refresh_display(self):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.display.insert(tk.END, f"{'SL':<4} {'Date':<12} {'Customer':<15} {'Type':<10} {'Amount':<10}\n")
        self.display.insert(tk.END, "-"*60 + "\n")
        for d in self.all_data:
            self.display.insert(tk.END, f"{d['SL']:<4} {d['Date']:<12} {d['Name'][:14]:<15} {d['Type']:<10} {d['Amount']:<10}\n")
        self.display.config(state='disabled')

    def export_excel(self):
        if not self.all_data: return
        df = pd.DataFrame(self.all_data)
        path = f"Report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        df.to_excel(path, index=False)
        messagebox.showinfo("Exported", f"ফাইল সেভ হয়েছে: {path}")

if _name_ == "_main_":
    root = tk.Tk()
    app = ProBusinessApp2026(root)
    root.mainloop()
