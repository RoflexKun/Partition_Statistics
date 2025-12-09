import os


class PartitionStatistics:

    def __init__(self, user_input):
        self.partition_letter = user_input.strip() + ":\\"
        self.extension_dict = {}
        self.number_directories = 0
        self.number_files = 0
        self.total_byte_size = 0
        self.extension_count = {}
        self.extension_size = {}
        self.extension_count_sorted_list = []
        self.extension_size_sorted_list = []

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
        """
        for extension, files in self.extension_dict.items():
            print("Extension: " + self._force_encoding(extension))
            for file_path, size in files.items():
                print("\tFile: " + self._force_encoding(file_path))
                print("\tSize: " + str(size))
        """

        self.sort_extensions_by_count()
        self.sort_extensions_by_size()
        self.display_percentage()

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

    def display_percentage(self):
        print("Percentage by number of files:\n")
        other_percentage = 0.00
        for extension, count in self.extension_count_sorted_list:
            if self.extension_count[extension]/self.number_files * 100 >= 0.1:
                print(f"{extension}: {self.extension_count[extension]/self.number_files * 100}%")
            else:
                other_percentage += self.extension_count[extension]/self.number_files * 100
        print("Other:", str(other_percentage) + '%', '\n')

        other_percentage = 0.00
        print("Percentage by size:\n")
        for extension, count in self.extension_size_sorted_list:
            if self.extension_size[extension]/self.total_byte_size * 100 >= 0.1:
                print(f"{extension}: {count/self.total_byte_size * 100}%")
            else:
                other_percentage += self.extension_size[extension]/self.total_byte_size * 100
        print("Other:", str(other_percentage) + '%', '\n')


    def _force_encoding(self, text):
        try:
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            return text.encode('utf-8', errors='replace').decode('utf-8')