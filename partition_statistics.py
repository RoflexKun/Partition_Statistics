import os


class PartitionStatistics:

    def __init__(self, user_input):
        self.partition_letter = "\\\\?\\" + user_input.strip() + ":\\"
        self.extension_dict = {}
        self.number_directories = 0
        self.number_files = 0
        self.total_byte_size = 0
        self.extension_count = {}
        self.extension_size = {}
        self.extension_count_sorted_list = []
        self.extension_size_sorted_list = []
        self.ordered_percentage_count = []
        self.ordered_percentage_size = []

    def get_partition_statistics(self):

        for root, dirs, files in os.walk(self.partition_letter):
            self.number_directories += 1

            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    size_bytes = os.path.getsize(file_path)
                    self.total_byte_size += size_bytes
                    if file.rfind('.') != -1:
                        extension = file[file.rfind('.') + 1 : ].lower()
                    else:
                        extension = '<no-ext>'
                    if extension not in self.extension_dict.keys():
                        self.extension_dict[extension] = []
                    self.extension_dict[extension].append({file_path: size_bytes})
                    self.number_files += 1
                except (OSError, PermissionError) as e:
                    file_path = os.path.join(root, file)
                    print(f"No permission to open file: {file_path}")
                    continue

        print("Number of directories: " + str(self.number_directories))
        print("Number of files: " + str(self.number_files))
        for extension, files in self.extension_dict.items():
            print("Extension: " + self._force_encoding(extension))
            for file_entry in files:
                for file_path, size in file_entry.items():
                    clean_path = file_path[4:]
                    print("\tFile: " + self._force_encoding(clean_path))
                    print("\tSize: " + str(size))

        self.sort_extensions_by_count()
        self.sort_extensions_by_size()
        self.compute_percentage()

    def sort_extensions_by_count(self):
        for ext in self.extension_dict.keys():
            self.extension_count[ext] = len(self.extension_dict[ext])

        self.extension_count_sorted_list = sorted(self.extension_count.items(), key=lambda x: x[1], reverse=True)

    def sort_extensions_by_size(self):
        for extension, files in self.extension_dict.items():
            extension_total_byte_size = 0
            for file in files:
                for file_path, byte_size in file.items():
                    extension_total_byte_size += byte_size
            self.extension_size[extension] = extension_total_byte_size

        self.extension_size_sorted_list = sorted(self.extension_size.items(), key=lambda x: x[1], reverse=True)
        print(self.extension_size)

    def order_extension(self, first_order=None, second_order=None) -> list:
        sorted_items = sorted(
            first_order.items(),
            key=lambda item: (item[1], second_order.get(item[0], 0)),
            reverse=True
        )

        temp_order_list = []
        for extension, percentage in sorted_items:
            temp_order_list.append({extension: percentage})

        return temp_order_list

    def compute_percentage(self):
        dict_count_percentage = {}
        for extension, count in self.extension_count_sorted_list:
            if self.extension_count[extension]/self.number_files * 100 >= 0.1:
                dict_count_percentage[extension] = self.extension_count[extension]/self.number_files * 100
            else:
                if 'other' not in dict_count_percentage.keys():
                    dict_count_percentage['other'] = self.extension_count[extension]/self.number_files * 100
                else:
                    dict_count_percentage['other'] += self.extension_count[extension]/self.number_files * 100

        dict_size_percentage = {}
        for extension, count in self.extension_size_sorted_list:
            if self.extension_size[extension]/self.total_byte_size * 100 >= 0.1:
                dict_size_percentage[extension] = self.extension_size[extension]/self.total_byte_size * 100
            else:
                if 'other' not in dict_size_percentage.keys():
                    dict_size_percentage['other'] = self.extension_size[extension]/self.total_byte_size * 100
                else:
                    dict_size_percentage['other'] += self.extension_size[extension]/self.total_byte_size * 100

        self.ordered_percentage_size = self.order_extension(dict_size_percentage, dict_count_percentage)
        self.ordered_percentage_count = self.order_extension(dict_count_percentage, dict_size_percentage)

        self.display_percentage()

    def display_percentage(self):
        print("Percentages based on count:")
        for dict in self.ordered_percentage_count:
            for extension, percentage in dict.items():
                print(f"{extension}: {percentage:.2f} %")

        print("Percentages based on size:")
        for dict in self.ordered_percentage_size:
            for extension, percentage in dict.items():
                print(f"{extension}: {percentage:.2f} %")

    def get_ordered_percentage_count(self):
        return self.ordered_percentage_count

    def get_ordered_percentage_size(self):
        return self.ordered_percentage_size

    def get_extensions_count(self) -> list:
        list_extensions = []
        for dict in self.ordered_percentage_count:
            for extension, percentage in dict.items():
                list_extensions.append(extension)
        return list_extensions

    def get_extensions_size(self) -> list:
        list_extensions = []
        for dict in self.ordered_percentage_size:
            for extension, percentage in dict.items():
                list_extensions.append(extension)
        return list_extensions

    def _force_encoding(self, text):
        try:
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            return text.encode('utf-8', errors='replace').decode('utf-8')