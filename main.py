class Proccess:
    def __init__(self) -> None:
        """
        Initializing a class with default input and output file paths.
        """
        self.input_file_path = "./input_data.txt"
        self.output_file_path = "./output_data.txt"

    def main(self) -> None:
        """
        Main function to execute the process.
        Reads input file, sorts the nested tree, and writes the sorted tree to the output file.
        """
        nested_tree = self.read_file()
        nested_tree = self.sort_nested_tree(nested_tree)
        self.write_sorted_tree_to_file(nested_tree)

    def __call__(self) -> None:
        """
        Callable method to run the main function when an instance is called.
        """
        self.main()

    def read_file(self) -> dict:
        """
        Reads the input file and processes each line to build a nested tree structure.
        Returns the nested tree.
        """
        nested_tree = {}

        with open(self.input_file_path, 'r') as file:
            for line in file:
                self.process_line(line, nested_tree)
        
        return nested_tree
    
    def process_line(self, line, nested_tree) -> None:
        """
        Processes a line from the input file and updates the nested tree accordingly.
        """
        names = line.strip().split('\\')
        current_dictionary = nested_tree

        for i, name in enumerate(names):
            if name not in current_dictionary:
                self.update_tree(current_dictionary, name)

            if i < len(names) - 1:
                current_dictionary = current_dictionary[name]

    def update_tree(self, current_dictionary, name) -> None:
        """
        Updates the current dictionary with a new nested dictionary or a file size.
        """
        parts = name.split(' ')

        if len(parts) == 1:
            current_dictionary[name] = {}
        elif len(parts) == 2:
            size_file = int(parts[1])
            current_dictionary[parts[0]] = size_file
            
    def sort_nested_tree(self, nested_tree) -> dict:
        """
        Sorts the nested tree, sorting folders alphabetically and files by size in reverse order.
        """
        folders = self.sort_folders(nested_tree)
        files = self.sort_files(nested_tree)

        result = {}
        result.update(folders)
        result.update(files)
        return result

    def sort_folders(self, nested_tree) -> dict:
        """
        Sorts folders alphabetically in the nested tree.
        Returns a dictionary with sorted folders.
        """
        result = sorted(
            ((key, self.sort_nested_tree(value)) for key, value in nested_tree.items() if isinstance(value, dict)),
            key=lambda x: x[0]
        )
        return dict(result)

    def sort_files(self, nested_tree) -> dict:
        """
        Groups and sorts files by size in the nested tree.
        Returns a dictionary with sorted files.
        """
        grouped_by_value = {}
        for key, value in nested_tree.items():
            if isinstance(value, int):
                grouped_by_value.setdefault(value, []).append(key)
        
        sorted_groups = {value: sorted(keys) for value, keys in grouped_by_value.items()}

        result = {}
        for value in sorted(sorted_groups.keys(), reverse=True):
            result.update({key: value for key in sorted_groups[value]})

        return result
    
    def write_sorted_tree_to_file(self, nested_tree) -> None:
        """
        Writes the sorted nested tree to the output file.
        """
        with open(self.output_file_path, 'w') as writer:
            self.write_nested_tree(nested_tree, writer)

    def write_nested_tree(self, nested_tree, writer, indent="") -> None:
        """
        Recursively writes the nested tree to the output file with proper indentation.
        """
        for key, value in nested_tree.items():
            writer.write(f"{indent}{key}\n")

            if isinstance(value, dict):
                self.write_nested_tree(value, writer, indent + "  ")

proccess = Proccess()
proccess()