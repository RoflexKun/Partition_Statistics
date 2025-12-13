from partition_statistics import PartitionStatistics
from tkinter.font import Font

import tkinter as tk


def statistics_window(partition_statistics):
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

    spinbox = tk.Spinbox(count_panel, from_=1, to=len(partition_statistics.get_extensions_count()), textvariable=tk.StringVar(value=str(len(partition_statistics.get_extensions_count()))), width=5, font=custom_list_font)
    spinbox.pack(anchor="w", pady=(5, 0))

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

    spinbox = tk.Spinbox(size_panel, from_=1, to=len(partition_statistics.get_extensions_size()), textvariable=tk.StringVar(value=str(len(partition_statistics.get_extensions_size()))), width=5, font=custom_list_font)
    spinbox.pack(anchor="w", pady=(5, 0))

    #Graphic settings for buttons to display the charts
    bottom_panel = tk.Frame(window, borderwidth=1, relief="raised", background="white")
    bottom_panel.pack(side="bottom", fill="x", padx=5, pady=10)

    button_style = {"font": custom_button_font, "height": 2, "bg": "#e1e1e1", "bd": 1, "relief": "raised"}

    file_type_count_chart = tk.Button(bottom_panel, text="Generate Count Chart", command=lambda: print("Count Chart"), **button_style)
    file_type_count_chart.pack(side="left",padx=30,pady=15)

    file_type_size_chart = tk.Button(bottom_panel, text="Generate Size Chart", command=lambda: print("Size Chart"), **button_style)
    file_type_size_chart.pack(side="left",padx=35,pady=15)

    file_type_count_top_n_chart = tk.Button(bottom_panel, text="Top-N Count Analysis", command=lambda: print("Top-N Count"), **button_style)
    file_type_count_top_n_chart.pack(side="left",padx=35,pady=15)

    file_type_size_top_n_chart = tk.Button(bottom_panel, text="Top-N Count Analysis", command=lambda: print("Top-N Size"), **button_style)
    file_type_size_top_n_chart.pack(side="left",padx=30,pady=15)

    window.mainloop()

if __name__ == '__main__':
    user_input = input("Please enter a partition letter: ")
    partition_statistics = PartitionStatistics(user_input)
    partition_statistics.get_partition_statistics()
    statistics_window(partition_statistics)


