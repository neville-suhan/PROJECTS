import tkinter as tk 
from tkinter import messagebox, scrolledtext, ttk
import mysql.connector 

def get_recommendations(): 
    # Get category from dropdown or text input
    category = category_var.get() if category_var.get() else category_entry.get().strip()
    
    if not category: 
        messagebox.showwarning("Input Error", "Please select or enter a category!") 
        return 

    try:
        # Database connection with auth_plugin fix
        conn = mysql.connector.connect( 
            host="127.0.0.1", 
            user="root", 
            password="123456",  # Change this to your MySQL password
            database="food_db",
            auth_plugin='mysql_native_password'
        ) 
        cursor = conn.cursor() 

        # Query to get food recommendations
        query = """ 
        SELECT f.food_name, f.description, f.rating
        FROM foods f
        JOIN categories c ON f.category_id = c.id  
        WHERE c.category_name = %s 
        ORDER BY f.rating DESC 
        LIMIT 5 
        """ 
        cursor.execute(query, (category,)) 
        results = cursor.fetchall() 
        cursor.close()
        conn.close() 

        # Display results
        output_text.delete(1.0, tk.END) 
        if results: 
            output_text.insert(tk.END, f"🍽️ Top {category} Food Recommendations:\n")
            output_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for i, (food_name, description, rating) in enumerate(results, 1): 
                output_text.insert(tk.END, f"{i}. {food_name}\n") 
                output_text.insert(tk.END, f"   📝 {description}\n") 
                output_text.insert(tk.END, f"   ⭐ Rating: {rating}/5\n\n") 
        else: 
            output_text.insert(tk.END, f"❌ No {category} food found!\n\n")
            output_text.insert(tk.END, "Available categories:\n")
            output_text.insert(tk.END, "• Indian\n• Chinese\n• Italian\n")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", 
                           f"Database connection failed!\n\n"
                           f"Error: {err}\n\n"
                           f"Please check:\n"
                           f"1. MySQL server is running\n"
                           f"2. Database 'food_db' exists\n"
                           f"3. Username and password are correct\n"
                           f"4. Tables are created with sample data")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
        
        
                   
        
        
        
# BACK END LOGIC
def load_all_foods():
    """Load and display all foods from database"""
    try:
        conn = mysql.connector.connect( 
            host="127.0.0.1", 
            user="root", 
            password="123456",  # Change this to your MySQL password
            database="food_db",
            auth_plugin='mysql_native_password'
        ) 
        cursor = conn.cursor() 

        query = """ 
        SELECT c.category_name, f.food_name, f.description, f.rating
        FROM foods f
        JOIN categories c ON f.category_id = c.id  
        ORDER BY c.category_name, f.rating DESC
        """ 
        cursor.execute(query) 
        results = cursor.fetchall() 
        cursor.close()
        conn.close() 

        output_text.delete(1.0, tk.END)
        if results:
            output_text.insert(tk.END, "🍽️ All Available Foods:\n")
            output_text.insert(tk.END, "=" * 50 + "\n\n")
            
            current_category = ""
            for category_name, food_name, description, rating in results:
                if category_name != current_category:
                    current_category = category_name
                    output_text.insert(tk.END, f"\n🍴 {category_name.upper()} CUISINE:\n")
                    output_text.insert(tk.END, "-" * 30 + "\n")
                
                output_text.insert(tk.END, f"• {food_name} ({rating}⭐)\n")
                output_text.insert(tk.END, f"  {description}\n\n")
        else:
            output_text.insert(tk.END, "No food items found in database!")
            
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error loading foods: {err}")

# Create main window
root = tk.Tk() 
root.title("Food Recommendation System") 
root.geometry("700x600") 
root.config(bg="#f8f9fa") 

# Header
header = tk.Label(root, text="🍽️ Food Recommendation System", 
                 font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#2c3e50")
header.pack(pady=15)

# Input section
input_frame = tk.Frame(root, bg="#f8f9fa")
input_frame.pack(pady=10)

# Dropdown selection
tk.Label(input_frame, text="Select Category:", 
         font=("Arial", 12), bg="#f8f9fa").grid(row=0, column=0, padx=5, sticky="w")

category_var = tk.StringVar(value="")
category_dropdown = ttk.Combobox(input_frame, textvariable=category_var,
                                values=["", "Indian", "Chinese", "Italian"],
                                font=("Arial", 11), state="readonly", width=15)
category_dropdown.grid(row=0, column=1, padx=10)

# Or text input
tk.Label(input_frame, text="Or type category:", 
         font=("Arial", 10), bg="#f8f9fa", fg="#666").grid(row=1, column=0, padx=5, pady=(5,0), sticky="w")
category_entry = tk.Entry(input_frame, font=("Arial", 11), width=18) 
category_entry.grid(row=1, column=1, padx=10, pady=(5,0))

# Buttons frame
button_frame = tk.Frame(root, bg="#f8f9fa")
button_frame.pack(pady=15)

# Get recommendations button
get_btn = tk.Button(button_frame, text="Get Recommendations", font=("Arial", 12), 
                   bg="#28a745", fg="white", command=get_recommendations,
                   padx=15, pady=5)
get_btn.pack(side=tk.LEFT, padx=5)

# Show all foods button
show_all_btn = tk.Button(button_frame, text="Show All Foods", font=("Arial", 12), 
                        bg="#007bff", fg="white", command=load_all_foods,
                        padx=15, pady=5)
show_all_btn.pack(side=tk.LEFT, padx=5)

# Results area
output_text = scrolledtext.ScrolledText(root, height=18, width=80, 
                                       font=("Arial", 11), wrap=tk.WORD,
                                       bg="white", relief="solid", borderwidth=1)
output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Welcome message
welcome_message = """Welcome to Food Recommendation System! 🍽️

Available Categories:
• Indian - Butter Chicken, Paneer Tikka
• Chinese - Fried Rice, Spring Rolls  
• Italian - Pizza Margherita, Pasta Alfredo

How to use:
1. Select a category from dropdown OR type it in the text field
2. Click 'Get Recommendations' for category-specific results
3. Click 'Show All Foods' to see everything in the database

Try it now! Select a category and get recommendations.
"""

output_text.insert(tk.END, welcome_message)

# Bind Enter key to search
category_entry.bind('<Return>', lambda event: get_recommendations())

# Start the application
print("Starting Food Recommendation System...")
print("Make sure your MySQL server is running and 'food_db' database exists!")
root.mainloop()