import os
import matplotlib.pyplot as plt

class ChartGenerator:

    def __init__(self, extension_count_list, extension_size_list):
        self.extension_count_list = extension_count_list
        self.extension_size_list = extension_size_list

        if not os.path.exists('charts'):
            os.makedirs('charts')

    def _process_data(self, extension_percentage_list):
        labels = []
        percentages = []
        for dict in extension_percentage_list:
            for extension, percentage in dict.items():
                labels.append(extension)
                percentages.append(percentage)

        return labels, percentages

    def generate_pie_chart(self, exentsion_percentage_list, title, file_name):
        labels, percentages = self._process_data(exentsion_percentage_list)

        plt.figure(figsize=(12, 12))

        wedges, texts, autotexts = plt.pie(
            percentages,
            labels=labels,
            autopct='%1.2f%%',
            startangle=140,
            textprops=dict(color="black")
        )
        fix_labels = []
        for i in range(len(labels)):
            legend_labels = f"{labels[i]} ({percentages[i]:.2f}%)"
            fix_labels.append(legend_labels)
        plt.title(title)
        plt.legend(wedges, fix_labels, title="Extensions", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        save_path = os.path.join('charts', file_name)
        plt.savefig(save_path, bbox_inches='tight')

        plt.tight_layout()
        plt.show()

    def generate_count_pie_chart(self):
        self.generate_pie_chart(
            self.extension_count_list,
            "File type distribution by Count",
            "pie_chart_count.png"
        )

    def generate_size_pie_chart(self):
        self.generate_pie_chart(
            self.extension_size_list,
            "File type distribution by Size",
            "pie_chart_size.png"
        )
