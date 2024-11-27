import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

def encrypt_pdf():

    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Ошибка", "Файл не выбран!")
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
            messagebox.showinfo("Успех")
        entry.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Что-то пошло не так: {e}")
        
#writing text from PDF file to text file
def extract_text():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Ошибка", "Файл не выбран!")
        return

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = "".join([page.extract_text() for page in reader.pages])

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            messagebox.showinfo("Успех", "Текст извлечён и сохранён!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Что-то пошло не так: {e}")

#Merge 2 PDF files
def merge_pdfs():
    pdf_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_paths:
        messagebox.showerror("Ошибка", "Файлы не выбраны!")
        return

    try:
        merger = PyPDF2.PdfMerger()
        for pdf in pdf_paths:
            merger.append(pdf)

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if save_path:
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Успех", "PDF-файлы объединены!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Что-то пошло не так: {e}")

#Split files in pages
def split_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        messagebox.showerror("Ошибка", "Файл не выбран!")
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
        messagebox.showinfo("Успех", "PDF разделён по страницам!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Что-то пошло не так: {e}")

#Main function
def main():
    root = tk.Tk()
    root.title("PDF Manager")
    root.geometry("700x600") 

    tk.Label(root, text="Welcome to PDF Manager!", font=("Arial", 44), foreground="black").pack(pady=30)

    tk.Button(root, text="Extract text from chosen PDF", command=extract_text, background="black", cursor="spider").pack(pady=20, anchor='c')
    tk.Button(root, text="Merge chosen PDFs", command=merge_pdfs, background="black", cursor="spider").pack(pady=20, anchor='c')
    tk.Button(root, text="Split PDF", command=split_pdf, background="black", cursor="spider").pack(pady=20, anchor='c')
    
    #encrypt pdf with password
    global entry
    
    entry_label = tk.Label(root, text="Write password you want.")
    entry_label.pack(pady=10, anchor='c')
    entry = tk.Entry(root)
    entry.pack(pady=20, anchor='c')
    tk.Button(root, text="Encrypt PDF file", command=encrypt_pdf, background="black", cursor="spider").pack(pady=20, anchor='c')
    
    root.mainloop()

#calling main function
main()
