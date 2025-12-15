import os
import matplotlib.pyplot as plt

class ChartGenerator:

    def __init__(self, extension_count_list, extension_size_list):
        self.extension_count_list = extension_count_list
        self.extension_size_list = extension_size_list

        if not os.path.exists('charts'):
            os.makedirs('charts')

    def _process_data(self, extension_percentage_list, selection=None):
        labels = []
        percentages = []
        if selection is None:
            for dict in extension_percentage_list:
                for extension, percentage in dict.items():
                    labels.append(extension)
                    percentages.append(percentage)
        else:
            other_percentage = 100.00
            for extension_selected in selection:
                for dict in extension_percentage_list:
                    for extension, percentage in dict.items():
                        if extension == extension_selected:
                            labels.append(extension)
                            percentages.append(percentage)
                            other_percentage -= percentage

            labels.append('other')
            percentages.append(other_percentage)

        return labels, percentages

    def generate_pie_chart(self, extension_percentage_list, selection, title, file_name):
        labels, percentages = self._process_data(extension_percentage_list, selection)

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
        plt.close()
        
    def generate_bar_chart(self, top_n, extension_percentage_list, title, file_name):
        labels, percentages = self._process_data(extension_percentage_list)

        limit = min(top_n, len(labels))
        labels = labels[:limit]
        percentages = percentages[:limit]

        plt.figure(figsize=(12, 12))

        bars = plt.bar(labels, percentages, color='skyblue', edgecolor='black')

        plt.title(title)
        plt.xlabel("Extensions", fontsize=12)
        plt.ylabel("Percentage (%)", fontsize=12)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.2f}%',
                ha='center',
                va='bottom',
                fontsize=9
            )

        plt.xticks(rotation=45)

        save_path = os.path.join('charts', file_name)
        plt.savefig(save_path, bbox_inches='tight')

        plt.tight_layout()
        plt.close()

    def generate_count_bar_chart(self, top_n):
        self.generate_bar_chart(
            top_n,
            self.extension_count_list,
            "Top-N file types by Count",
            "bar_chart_count.png"
        )

    def generate_size_bar_chart(self, top_n):
        self.generate_bar_chart(
            top_n,
            self.extension_size_list,
            "Top-N file types by Size",
            "bar_chart_size.png"
        )

    def generate_count_pie_chart(self, selection):
        self.generate_pie_chart(
            self.extension_count_list,
            selection,
            "File type distribution by Count",
            "pie_chart_count.png"
        )

    def generate_size_pie_chart(self, selection):
        self.generate_pie_chart(
            self.extension_size_list,
            selection,
            "File type distribution by Size",
            "pie_chart_size.png"
        )
