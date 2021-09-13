vuejs_filename = "/home/kpc/PycharmProjects/security-proj-1/meta_data_analyzer/customhex/vuejs.pdf"
gephi_filename = "/home/kpc/PycharmProjects/security-proj-1/meta_data_analyzer/customhex/gephi.pdf"


def convert_to_hex(filename: str) -> str:
    hex_array = []
    count = 0
    file = open(filename, "rb").readlines()
    for line in file:
        for byte in line:
            hex_byte = hex(byte).replace("x", "").upper()
            if byte >= 16:
                hex_byte = hex_byte.lstrip("0")
            hex_array.append(hex_byte)
        count += 1
        if count == 10:
            break
    return ''.join(hex_array)


def read_pdf_xmp(filename: str) -> str:
    file = open(filename, "rb").readlines()
    # print_bool = False
    for line in file:
        # if line.__contains__('<x:xmpmeta'):
        #     print_bool = not print_bool
        # if print_bool:
        print(line)


print(read_pdf_xmp(vuejs_filename))
