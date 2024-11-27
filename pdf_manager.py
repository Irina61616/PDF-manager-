import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
import csv

#extract_tables
def extract_tables():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Error", "Choose a file!")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_tables = []
            for page in pdf.pages:
                tables = page.extract_tables()
                all_tables.extend(tables)

            if not all_tables:
                messagebox.showinfo("No Tables", "No tables found in the PDF.")
                return

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for table in all_tables:
                    for row in table:
                        writer.writerow(row)
            messagebox.showinfo("Tables Extracted", "Tables have been successfully extracted!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
#search keyword in pdf
def search_keyword():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Error", "Choose a file!")
        return

    keyword = entry_keyword.get().strip()
    if not keyword:
        messagebox.showerror("Error", "Enter a keyword!")
        return

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            found_pages = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if keyword.lower() in text.lower():
                    found_pages.append(page_num + 1)

        if found_pages:
            messagebox.showinfo("Keyword Found", f"Keyword '{keyword}' found on pages: {found_pages}")
        else:
            messagebox.showinfo("Keyword Not Found", f"Keyword '{keyword}' not found in the PDF.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

def encrypt_pdf():

    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Error", "Choose file!")
        return
    
    try:
        writer = PyPDF2.PdfWriter()

        with open(pdf_path, 'rb') as f_in:
            reader = PyPDF2.PdfReader(f_in)
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

        writer.encrypt(entry.get())

        with open(pdf_path, 'wb') as f_out:
            writer.write(f_out)
            messagebox.showinfo("Done")
        entry.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

#decrypt pdf
def decrypt_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Error", "Choose file!")
        return
    
    try:
        
        writer = PyPDF2.PdfWriter()
        
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if reader.is_encrypted:
                reader.decrypt(decrypt_entry.get())
            for page in reader.pages:
                writer.add_page(page)
            
        save_path = filedialog.asksaveasfilename(defaultextension=(".pdf"), filetypes=(["PDF Files", "*.pdf"])) 
        if save_path:
            with open(save_path, 'w') as decrypted_file:
                writer.write(decrypted_file)
        
        messagebox.showinfo("Done")
        decrypt_entry.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong!!: {e}")

#writing text from PDF file to text file
def extract_text():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Error", "Choose file!")
        return

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = "".join([page.extract_text() for page in reader.pages])

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            messagebox.showinfo("Text is extracted!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

#Merge 2 PDF files
def merge_pdfs():
    pdf_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_paths:
        messagebox.showerror("Error", "Choose file!")
        return

    try:
        merger = PyPDF2.PdfMerger()
        for pdf in pdf_paths:
            merger.append(pdf)

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if save_path:
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("PDF`s are merged!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

#Split files in pages
def split_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Error", "Choose file!")
        return

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for i, page in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)

                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"page_{i + 1}.pdf", filetypes=[("PDF Files", "*.pdf")])
                if save_path:
                    with open(save_path, 'wb') as output_file:
                        writer.write(output_file)
        messagebox.showinfo("PDF is splited!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

#Main function
def main():
    root = tk.Tk()
    root.title("PDF Manager")
    root.geometry("700x600") 

    tk.Label(root, text="Welcome to PDF Manager!", font=("Arial", 44), foreground="black").pack(pady=30)

    tk.Button(root, text="Extract text from chosen PDF", command=extract_text, background="black", cursor="spider").pack(pady=20, anchor='c')
    tk.Button(root, text="Merge chosen PDFs", command=merge_pdfs, background="black", cursor="spider").pack(pady=20, anchor='c')
    tk.Button(root, text="Split PDF", command=split_pdf, background="black", cursor="spider").pack(pady=20, anchor='c')
    tk.Button(root, text="Extract Tables from PDF", command=extract_tables, background="gray", font=("Arial", 12), cursor="spider").pack(pady=10, anchor='c')
    
    #encrypt pdf with password
    global entry
    
    entry_label = tk.Label(root, text="Write password you want.")
    entry_label.pack(pady=10, anchor='c')
    entry = tk.Entry(root)
    entry.pack(pady=20, anchor='c')
    tk.Button(root, text="Encrypt PDF file", command=encrypt_pdf, background="black", cursor="spider").pack(pady=20, anchor='c')

    #decrypt pdf
    tk.Label(root, text="Enter password to decrypt:").pack(pady=10, anchor='c')
    global decrypt_entry
    decrypt_entry = tk.Entry(root, show="*")
    decrypt_entry.pack(pady=5, anchor='c')
    tk.Button(root, text="decrypt PDF", command=decrypt_pdf, background="gray", font=("Arial", 12), cursor="spider").pack(pady=10, anchor='c')

    #find keyword in pdf file
    tk.Label(root, text="Enter Keyword to Search:").pack(pady=10, anchor='c')
    global entry_keyword
    entry_keyword = tk.Entry(root)
    entry_keyword.pack(pady=5, anchor='c')
    tk.Button(root, text="Search for Keyword", command=search_keyword, background="gray", font=("Arial", 12), cursor="spider").pack(pady=10, anchor='c')

    root.mainloop()

#calling main function
main()
