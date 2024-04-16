import tkinter as tk

def load_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_template(file_path, template):
    with open(file_path, 'w') as file:
        file.write(template)

def update_text():
    template_content = text_widget.get(1.0, tk.END)
    for php_variable, textarea in php_textareas.items():
        start_index = template_content.find(php_variable)
        if start_index != -1:
            end_index = start_index + len(php_variable)
            value = textarea.get(1.0, tk.END).strip()
            template_content = template_content[:start_index] + value + template_content[end_index:]
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, template_content)

template_file = "template.txt"
template = load_template(template_file)

root = tk.Tk()
root.title("PHP Template Editor")

text_widget = tk.Text(root, wrap="word", width=80, height=20)
text_widget.pack(fill="both", expand=True)
text_widget.insert(tk.END, template)

php_textareas = {}

start_index = 0
while True:
    start_index = template.find("$", start_index)
    if start_index == -1:
        break
    end_index = template.find(" ", start_index)
    php_variable = template[start_index:end_index].strip()
    php_textareas[php_variable] = tk.Text(root, wrap="word", width=80, height=5)
    php_textareas[php_variable].insert(tk.END, "")
    php_textareas[php_variable].pack()
    start_index = end_index

update_button = tk.Button(root, text="Update Template", command=update_text)
update_button.pack()

root.mainloop()
