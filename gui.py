# In the __init__ method, add these new input fields after
from tkinter import ttk, messagebox
import tkinter as tk
import sys
from aladdin_backpack import AladdinBackpack

class AladdinGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Aladdin's Backpack Optimizer")
        self.master.geometry("1000x700")
        self.master.configure(bg='#f0f0f0')
        
        # Apply a theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background='#f0f0f0')
        style.configure('Custom.TLabelframe', background='#f0f0f0')
        style.configure('Run.TButton', 
                       padding=10, 
                       font=('Arial', 10, 'bold'),
                       background='#4CAF50')
        
        # Create main frame with padding
        main_frame = ttk.Frame(master, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title Label
        title_label = ttk.Label(main_frame, 
                               text="Aladdin's Backpack Optimizer",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # Left Frame (Input Parameters)
        left_frame = ttk.LabelFrame(main_frame, text="Parameters", 
                                  padding="15",
                                  style='Custom.TLabelframe')
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.N), padx=5, pady=5)
        
        # Input fields with validation
        self.create_input_field(left_frame, "Number of Items:", "num_items", 0, "5", 1, 100)
        self.create_input_field(left_frame, "Generations:", "generations", 1, "5", 1, 1000)
        self.create_input_field(left_frame, "Backpack Size:", "backpack_size", 2, "20", 1, 1000)
        self.create_input_field(left_frame, "Min Weight:", "weight_min", 3, "1", 1, 100)
        self.create_input_field(left_frame, "Max Weight:", "weight_max", 4, "10", 1, 100)
        self.create_input_field(left_frame, "Min Value:", "value_min", 5, "1", 1, 100)
        self.create_input_field(left_frame, "Max Value:", "value_max", 6, "30", 1, 100)
        self.create_input_field(left_frame, "Min Fragility:", "fragility_min", 7, "1", 1, 10)
        self.create_input_field(left_frame, "Max Fragility:", "fragility_max", 8, "5", 1, 10)
        self.create_input_field(left_frame, "Mutation Probability:", "mutation_prob", 9, "0.3", 0, 1)
        
        
        # Buttons frame
        button_frame = ttk.Frame(left_frame, style='Custom.TFrame')
        button_frame.grid(row=11, column=0, columnspan=2, pady=10)
        
        # Run button with icon (if available)
        self.run_button = ttk.Button(button_frame, 
                                   text="Run Optimization",
                                   command=self.run_optimization,
                                   style='Run.TButton')
        self.run_button.grid(row=0, column=0, padx=5)
        
        # Clear button
        self.clear_button = ttk.Button(button_frame,
                                     text="Clear Results",
                                     command=self.clear_output)
        self.clear_button.grid(row=0, column=1, padx=5)
        
        # Right Frame (Output)
        right_frame = ttk.LabelFrame(main_frame, text="Results", 
                                   padding="15",
                                   style='Custom.TLabelframe')
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Output text area with scrollbar
        self.output = tk.Text(right_frame, 
                            height=50, 
                            width=80,
                            font=('Consolas', 10),
                            bg='white',
                            wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", 
                                command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.grid(row=0, column=0, padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, 
                             textvariable=self.status_var,
                             relief=tk.SUNKEN,
                             anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def create_input_field(self, parent, label_text, var_name, row, default, min_val, max_val):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(parent, width=20)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        setattr(self, var_name, entry)
        
        # Add validation
        vcmd = (self.master.register(lambda P: self.validate_input(P, min_val, max_val)), '%P')
        entry.configure(validate='key', validatecommand=vcmd)

    def validate_input(self, P, min_val, max_val):
        if P == "":
            return True
        try:
            value = int(P)
            return min_val <= value <= max_val
        except ValueError:
            return False

    def run_optimization(self):
        try:
            self.run_button.state(['disabled'])
            self.status_var.set("Running optimization...")
            
            # Get input values
            num_items = int(self.num_items.get())
            generations = int(self.generations.get())
            backpack_size = int(self.backpack_size.get())
            weight_min = int(self.weight_min.get())
            weight_max = int(self.weight_max.get())
            value_min = int(self.value_min.get())
            value_max = int(self.value_max.get())
            fragility_min = int(self.fragility_min.get())
            fragility_max = int(self.fragility_max.get())
            mutation_prob = float(self.mutation_prob.get())

            aladdin = AladdinBackpack(
                num_items=num_items,
                generations=generations,
                backpack_size=backpack_size,
                weight_range=(weight_min, weight_max),
                value_range=(value_min, value_max),
                fragility_range=(fragility_min, fragility_max),
                mutation_probability=mutation_prob
            )
            
            best_solution, weight_list, value_list, fragility_list = aladdin.run()
            
            # Display results in a better format
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "✨ Optimization Results ✨\n\n")
            
            # Header
            header = f"{'Item':^6} | {'Selected':^8} | {'Weight':^8} | {'Value':^8} | {'Fragility':^9}\n"
            separator = "-" * 46 + "\n"
            
            self.output.insert(tk.END, header)
            self.output.insert(tk.END, separator)
            
            # Item details
            total_weight = 0
            total_value = 0
            for i, (selected, weight, value, fragility) in enumerate(
                zip(best_solution, weight_list, value_list, fragility_list)
            ):
                row = f"{i+1:^6} | {('✓' if int(selected) else '✗'):^8} | {weight:^8.2f} | {value:^8.2f} | {fragility:^9.2f}\n"
                self.output.insert(tk.END, row)
                if int(selected):
                    total_weight += weight
                    total_value += value
            
            # Summary
            self.output.insert(tk.END, separator)
            self.output.insert(tk.END, f"\nTotal Weight: {total_weight:.2f}")
            self.output.insert(tk.END, f"\nTotal Value: {total_value:.2f}")
            
            self.status_var.set("Optimization completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error occurred during optimization")
        finally:

            self.run_button.state(['!disabled'])


    def clear_output(self):
        self.output.delete(1.0, tk.END)
        self.status_var.set("Results cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = AladdinGUI(root)
    root.mainloop()
