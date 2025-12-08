import os


class PartitionStatistics:

    def __init__(self, user_input):
        self.partition_letter = user_input.strip() + ":\\"
        self.extension_dict = {}
        self.number_directories = 0
        self.number_files = 0

    def get_partition_statistics(self):

        for root, dirs, files in os.walk(self.partition_letter):
            self.number_directories += 1

            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    size_bytes = os.path.getsize(file_path)
                    if file.rfind('.') != -1:
                        extension = file[file.rfind('.') + 1 : ].lower()
                    else:
                        extension = '<no-ext>'
                    if extension not in self.extension_dict.keys():
                        self.extension_dict[extension] = {}
                    self.extension_dict[extension][file_path] = size_bytes
                    self.number_files += 1
                except (OSError, PermissionError) as e:
                    file_path = os.path.join(root, file)
                    print(f"No permission to open file: {file_path}")
                    continue

        print("Number of directories: " + str(self.number_directories))
        print("Number of files: " + str(self.number_files))
        for extension, files in self.extension_dict.items():
            print("Extension: " + self._force_encoding(extension))
            for file_path, size in files.items():
                print("\tFile: " + self._force_encoding(file_path))
                print("\tSize: " + str(size))


    def _force_encoding(self, text):
        try:
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            return text.encode('utf-8', errors='replace').decode('utf-8')