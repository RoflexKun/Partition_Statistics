from partition_statistics import PartitionStatistics
from chart_generator import ChartGenerator
from tkinter.font import Font
from PIL import Image, ImageTk

import tkinter as tk
import os
import string

def statistics_window(partition_statistics, chart_generator):
    window = tk.Tk()
    window.title("Partition Statistics")
    window.geometry("1280x720")
    window.resizable(False, False)
    window.config(background="#f0f0f0")

    # Custom font for different widgets
    custom_button_font = Font(family="Segoe UI", size=10, weight="bold")
    custom_label_font = Font(family="Segoe UI", size=10, weight="bold")
    custom_list_font = Font(family="Consolas", size=10)
    # Graphic settings for the file type count settings
    count_panel = tk.LabelFrame(window, text="File count settings", padx=10, pady=10, background="white", font=custom_label_font)
    count_panel.pack(side="right", fill="y", padx=20, pady=20)

    extensions_count_panel_frame = tk.Frame(count_panel, background="white")
    extensions_count_panel_frame.pack(fill="both", expand=True, pady=5)

    scrollbar = tk.Scrollbar(extensions_count_panel_frame)
    scrollbar.pack(side="right", fill="y")

    extension_count_list = tk.Listbox(extensions_count_panel_frame, yscrollcommand=scrollbar.set, selectmode="multiple", height=10, width=20, font=custom_list_font, activestyle="none", bd=0, highlightthickness=1, relief="solid")
    extension_count_list.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=extension_count_list.yview)

    for extension in partition_statistics.get_extensions_count():
        extension_count_list.insert(tk.END, extension)

    spinbox_count = tk.Spinbox(count_panel, from_=1, to=len(partition_statistics.get_extensions_count()), textvariable=tk.StringVar(value=str(len(partition_statistics.get_extensions_count()))), width=5, font=custom_list_font)
    spinbox_count.pack(anchor="w", pady=(5, 0))

    # Graphic settings for the file type size settings
    size_panel = tk.LabelFrame(window, text="File size settings", padx=10, pady=10, background="white", font=custom_label_font)
    size_panel.pack(side='left', fill="y", padx=20, pady=20)

    extension_size_panel_frame = tk.Frame(size_panel, background="white")
    extension_size_panel_frame.pack(fill="both", expand=True, pady=5)

    scrollbar = tk.Scrollbar(extension_size_panel_frame)
    scrollbar.pack(side="right", fill="y")

    extension_size_list = tk.Listbox(extension_size_panel_frame, yscrollcommand=scrollbar.set, selectmode="multiple", height=10, width=20, font=custom_list_font, activestyle="none", bd=0, highlightthickness=1, relief="solid")
    extension_size_list.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=extension_size_list.yview)

    for extension in partition_statistics.get_extensions_size():
        extension_size_list.insert(tk.END, extension)

    spinbox_size = tk.Spinbox(size_panel, from_=1, to=len(partition_statistics.get_extensions_size()), textvariable=tk.StringVar(value=str(len(partition_statistics.get_extensions_size()))), width=5, font=custom_list_font)
    spinbox_size.pack(anchor="w", pady=(5, 0))

    #Graphic settings for buttons to display the charts
    bottom_panel = tk.Frame(window, borderwidth=1, relief="raised", background="white")
    bottom_panel.pack(side="bottom", fill="x", padx=5, pady=10)

    button_style = {"font": custom_button_font, "height": 2, "bg": "#e1e1e1", "bd": 1, "relief": "raised"}

    file_type_count_chart = tk.Button(bottom_panel, text="Generate Count Chart", command=lambda: show_count_pie_chart(), **button_style)
    file_type_count_chart.pack(side="left",padx=30,pady=15)

    file_type_size_chart = tk.Button(bottom_panel, text="Generate Size Chart", command=lambda: show_size_pie_chart(), **button_style)
    file_type_size_chart.pack(side="left",padx=35,pady=15)

    file_type_count_top_n_chart = tk.Button(bottom_panel, text="Top-N Count Analysis", command=lambda: show_count_bar_chart(), **button_style)
    file_type_count_top_n_chart.pack(side="left",padx=35,pady=15)

    file_type_size_top_n_chart = tk.Button(bottom_panel, text="Top-N Size Analysis", command=lambda: show_size_bar_chart(), **button_style)
    file_type_size_top_n_chart.pack(side="left",padx=30,pady=15)

    # Graphic settings for the image that will be showcased in the middle of the GUI
    center_panel = tk.Frame(window, background="#f0f0f0")
    center_panel.pack(side="top", fill="both", expand=True)

    chart_label = tk.Label(center_panel, text="Select a chart to generate", background="#f0f0f0", font=custom_label_font)
    chart_label.pack(expand=True)

    def update_chart_display(filename):
        path = os.path.join("charts", filename)
        if os.path.exists(path):
            pil_image = Image.open(path)
            pil_image = pil_image.resize((650, 550), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(pil_image)

            chart_label.config(image=photo)
            chart_label.image = photo
        else:
            chart_label.config(text="Error: Chart file not found.", image="")

    def show_count_pie_chart():
        selection_indexes = extension_count_list.curselection()
        selection = None
        if selection_indexes:
            selection = []
        for i in selection_indexes:
            selection.append(extension_count_list.get(i))

        chart_generator.generate_count_pie_chart(selection)
        update_chart_display("pie_chart_count.png")

    def show_size_pie_chart():
        selection_indexes = extension_size_list.curselection()
        selection = None
        if selection_indexes:
            selection = []
        for i in selection_indexes:
            selection.append(extension_size_list.get(i))
        chart_generator.generate_size_pie_chart(selection)
        update_chart_display("pie_chart_size.png")

    def show_count_bar_chart():
        chart_generator.generate_count_bar_chart(int(spinbox_count.get()))
        update_chart_display("bar_chart_count.png")

    def show_size_bar_chart():
        chart_generator.generate_size_bar_chart(int(spinbox_size.get()))
        update_chart_display("bar_chart_size.png")

    window.mainloop()

if __name__ == '__main__':

    def check_partition_valid(user_input):
        if user_input.strip() == "":
            return False
        elif len(user_input.strip()) > 1:
            return False
        elif user_input.strip() not in string.ascii_letters:
            return False
        else:
            partition_path = user_input.strip() + ":\\"
            if not os.path.isdir(partition_path):
                return False

        return True

    while True:
        user_input = input("Please enter a partition letter: ")

        if check_partition_valid(user_input):
            break
        else:
            print("Invalid Partition Letter.")


    partition_statistics = PartitionStatistics(user_input)
    partition_statistics.get_partition_statistics()

    chart_generator = ChartGenerator(partition_statistics.get_ordered_percentage_count(), partition_statistics.get_ordered_percentage_size())
    statistics_window(partition_statistics, chart_generator)


