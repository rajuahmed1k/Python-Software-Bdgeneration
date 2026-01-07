import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class UltimateBusinessManager:
    def _init_(self, root):
        self.root = root
        self.root.title("Pro Order Manager 2026")
        self.root.geometry("550x750")
        self.root.configure(bg="#f4f7f6")

        self.all_data = []
        self.serial_counter = 1

        # Title
        tk.Label(root, text="বিজনেস অর্ডার ট্র্যাকার", font=("Arial", 20, "bold"), bg="#f4f7f6", fg="#2c3e50").pack(pady=15)

        # Input Frame
        input_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        input_frame.pack(pady=5, padx=15, fill="x")

        # Inputs
        tk.Label(input_frame, text="কাস্টমার নাম:", bg="#fff").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(input_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="টাইপ:", bg="#fff").grid(row=1, column=0, sticky="w")
        self.type_var = ttk.Combobox(input_frame, values=["Delivery", "Return"], state="readonly", width=22)
        self.type_var.current(0)
        self.type_var.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="টাকার পরিমাণ:", bg="#fff").grid(row=2, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame, width=25)
        self.amount_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = tk.Frame(root, bg="#f4f7f6")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="এন্ট্রি যোগ করুন", command=self.add_entry, bg="#27ae60", fg="white", width=15, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Excel ডাউনলোড", command=self.export_to_excel, bg="#2980b9", fg="white", width=15, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="সব মুছুন", command=self.clear_all, bg="#e74c3c", fg="white", width=10).grid(row=0, column=2, padx=5)

        # Search Frame
        search_frame = tk.Frame(root, bg="#f4f7f6")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="খুঁজুন (নাম):", bg="#f4f7f6").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_data).grid(row=0, column=2)

        # Table/Display
        self.display = tk.Text(root, height=15, width=65, font=("Courier", 9), state='disabled', bg="#fdfdfd")
        self.display.pack(pady=10, padx=10)

        # Summary Frame
        self.summary_lbl = tk.Label(root, text="Delivery: 0 | Return: 0 | Net: 0", font=("Arial", 12, "bold"), fg="#16a085", bg="#f4f7f6")
        self.summary_lbl.pack(pady=10)

    def add_entry(self):
        name = self.name_entry.get().strip()
        o_type = self.type_var.get()
        amount = self.amount_entry.get().strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name or not amount:
            messagebox.showwarning("সতর্কতা", "নাম এবং পরিমাণ দিন")
            return

        try:
            amt = float(amount)
            data = {"SL": self.serial_counter, "Date": date, "Customer": name, "Type": o_type, "Amount": amt}
            self.all_data.append(data)
            self.serial_counter += 1
            self.refresh_display()
            self.update_summary()
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("ভুল", "টাকার ঘরে সঠিক সংখ্যা দিন")

    def refresh_display(self, data_list=None):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.display.insert(tk.END, f"{'SL':<4} {'Date':<17} {'Customer':<15} {'Type':<10} {'Amount':<8}\n")
        self.display.insert(tk.END, "-"*65 + "\n")
        
        target_list = data_list if data_list is not None else self.all_data
        for d in target_list:
            line = f"{d['SL']:<4} {d['Date']:<17} {d[ 'Customer'][:14]:<15} {d['Type']:<10} {d['Amount']:<8}\n"
            self.display.insert(tk.END, line)
        self.display.config(state='disabled')

    def update_summary(self):
        deliv = sum(d['Amount'] for d in self.all_data if d['Type'] == "Delivery")
        ret = sum(d['Amount'] for d in self.all_data if d['Type'] == "Return")
        net = deliv - ret
        self.summary_lbl.config(text=f"Deliv: {deliv} | Ret: {ret} | Net: {net} TK")

    def search_data(self):
        query = self.search_entry.get().lower()
        results = [d for d in self.all_data if query in d['Customer'].lower()]
        self.refresh_display(results)

    def export_to_excel(self):
        if not self.all_data:
            messagebox.showwarning("Empty", "ডাউনলোড করার মতো কোনো ডাটা নেই")
            return
        df = pd.DataFrame(self.all_data)
        fname = f"Report_{datetime.now().strftime('%d_%m_%Y_%H%M')}.xlsx"
        df.to_excel(fname, index=False)
        messagebox.showinfo("Success", f"এক্সেল ফাইল '{fname}' সেভ হয়েছে")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "সব ডাটা মুছে ফেলবেন?"):
            self.all_data = []
            self.serial_counter = 1
            self.refresh_display()
            self.update_summary()

if _name_ == "_main_":
    root = tk.Tk()
    app = UltimateBusinessManager(root)
    root.mainloop()
