class HexFile:
    def __init__(self, filename: str, columns: int):
        super(__class__, self).__init__()
        self.columns = columns

        self.filename = filename
        self.file_content = bytes

        self.special_characters = ["\a", "\b", "\f", "\n", "\r", "\t", "\v", "\x00"]

        self.hex_array = []
        self.hex_array_len = 0

    def start(self):
        """
        This function begins the process of reading a file
        and converting it to hex
        """
        self._read_file()
        self._process_content()
        self._format_content()

    def decode_hex(self):
        """
        This function decodes the hex content of the file to ascii

        :return: The decoded text, already formatted
        """
        decoded_array = []

        for line in self.hex_array:
            line_array = []
            for hex_object in line:
                # Convert the hex byte into a normal byte
                byte_object = bytes.fromhex(hex_object)

                # Convert the byte into ascii
                try:
                    ascii_object = byte_object.decode("ascii")
                except UnicodeDecodeError:
                    ascii_object = "."

                # Replace the char with a dot if it's a special character
                if ascii_object in self.special_characters:
                    ascii_object = "."

                # Add the ascii char to the line array
                line_array.append(ascii_object)

            # add the line to the decoded array
            decoded_array.append(line_array)

        return decoded_array

    def _read_file(self):
        self.file_content = open(self.filename, "rb").readlines()

    def _process_content(self):
        # Convert the File Content into Hex

        # Go through every line and convert every byte into Hex
        for line in self.file_content:
            for byte in line:
                self.hex_array_len += 1
                hex_byte = hex(byte).replace("x", "").upper()
                if byte >= 16:
                    hex_byte = hex_byte.lstrip("0")
                self.hex_array.append(hex_byte)

    def _format_content(self):
        # Formats the Hex Array

        i = 0
        line = []
        new_array = []
        for byte in self.hex_array:
            if i == self.columns:
                new_array.append(line)
                line = []
                i = 0

            line.append(byte)
            i += 1

        if line:
            new_array.append(line)

        self.hex_array = new_array


if __name__ == "__main__":
    mukera = HexFile("vuejs.pdf", 16)
    print(mukera.decode_hex())
