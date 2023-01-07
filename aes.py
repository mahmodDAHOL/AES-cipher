import codecs
import random

IV = "".join([str(random.randrange(0, 2)) for _ in range(128)])
sub_key_numbers = 10

# this function takes two binary string and do xor operation on them
def xor(s1, s2):
    if len(s1) > len(s2):
        s2 = (len(s1)-len(s2))*"0" + s1
    if len(s1) < len(s2):
        s1 = (len(s2)-len(s1))*"0" + s2
    return "".join(map(str, list(int(a) ^ int(b) for a, b in zip(s1, s2))))

# this function takes two binary string and do and operation on them
def bit_and(a, b):
    result = ""
    for i, j in zip(a, b):
        if i == "1" and j == "1":
            result += "1"
        else:
            result += "0"

    return result

def multiply(x, y):
    p = "100011011"             # mpy modulo x^8+x^4+x^3+x+1
    m = "000000000"                       # m will be product
    x = "0"+x
    y = "0"+y
    for i in range(8):
        m = m[1:] + m[0]
        if bit_and(m, "100000000") != "000000000":
            m = xor(m, p)
        if bit_and(y, "010000000") != "000000000":
            m = xor(m, x)
        y = y[1:] + y[0]
    return m


# this function take binary as a string and return string in hexadecimal
def bin_to_hex(n):
    if n == "0000":
        return "0"
    bnum = int(n)
    temp = 0
    mul = 1
    count = 1
    hexaDeciNum = ['0'] * 100

    i = 0
    while bnum != 0:
        rem = bnum % 10
        temp = temp + (rem*mul)
        if count % 4 == 0:
            if temp < 10:
                hexaDeciNum[i] = chr(temp+48)
            else:
                hexaDeciNum[i] = chr(temp+55)
            mul = 1
            temp = 0
            count = 1
            i = i+1
        # group of 4 is not completed
        else:
            mul = mul*2
            count = count+1
        bnum = int(bnum/10)

    # check if at end the group of 4 is not
    # completed
    if count != 1:
        hexaDeciNum[i] = chr(temp+48)

    # check at end the group of 4 is completed
    if count == 1:
        i = i-1

    result = ""
    while i >= 0:
        result += hexaDeciNum[i]
        i = i-1
    return result

# this function takes one hexadecimal string and return binary number as string
def hex_to_binary(hex_digits):
    binary_digits = ""
    for hex_digit in hex_digits:
        binary_digits += bin(int(hex_digit, 16))[2:].zfill(4)

    return binary_digits

def hex_matrix_to_bin(matrix):
    rows = []
    for row in matrix:
        rows.append([hex_to_binary(x) for x in row])
    return rows

def bin_matrix_to_hex(matrix):
    rows = []
    for row in matrix:
        rows.append([bin_to_hex(x) for x in row])
    return rows

Sbox = [
    ["63", "7C", "77", "7B", "F2", "6B", "6F", "C5",
        "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
    ["CA", "82", "C9", "7D", "FA", "59", "47", "F0",
        "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
    ["B7", "FD", "93", "26", "36", "3F", "F7", "CC",
        "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
    ["04", "C7", "23", "C3", "18", "96", "05", "9A",
        "07", "12", "80", "E2", "EB", "27", "B2", "75"],
    ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0",
        "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
    ["53", "D1", "00", "ED", "20", "FC", "B1", "5B",
        "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
    ["D0", "EF", "AA", "FB", "43", "4D", "33", "85",
        "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
    ["51", "A3", "40", "8F", "92", "9D", "38", "F5",
        "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
    ["CD", "0C", "13", "EC", "5F", "97", "44", "17",
        "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
    ["60", "81", "4F", "DC", "22", "2A", "90", "88",
        "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
    ["E0", "32", "3A", "0A", "49", "06", "24", "5C",
        "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
    ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9",
        "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
    ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6",
        "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
    ["70", "3E", "B5", "66", "48", "03", "F6", "0E",
        "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
    ["E1", "F8", "98", "11", "69", "D9", "8E", "94",
        "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
    ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]]

Sbox_inv = [["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
            ["7C", "E3", "39", "82", "9B", "2F", "FF", "87",
                "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
            ["54", "7B", "94", "32", "A6", "C2", "23", "3D",
                "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
            ["08", "2E", "A1", "66", "28", "D9", "24", "B2",
                "76", "5B", "A2", "49", "6D", "8B", "D1", "25"],
            ["72", "F8", "F6", "64", "86", "68", "98", "16",
                "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
            ["6C", "70", "48", "50", "FD", "ED", "B9", "DA",
                "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
            ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A",
                "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
            ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02",
                "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
            ["3A", "91", "11", "41", "4F", "67", "DC", "EA",
                "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
            ["96", "AC", "74", "22", "E7", "AD", "35", "85",
                "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
            ["47", "F1", "1A", "71", "1D", "29", "C5", "89",
                "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
            ["FC", "56", "3E", "4B", "C6", "D2", "79", "20",
                "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
            ["1F", "DD", "A8", "33", "88", "07", "C7", "31",
                "B1", "12", "10", "59", "27", "80", "EC", "5F"],
            ["60", "51", "7F", "A9", "19", "B5", "4A", "0D",
                "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
            ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0",
                "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
            ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"]]


# this function takes two integer (index of row, index of column) then return correspond field in s-box table
def get_sbox_entry(row_index, column_index, s_box):
    lower_case_hex = s_box[row_index][column_index]
    upper_case_hex = "".join([string.capitalize()
                             for string in lower_case_hex])
    return upper_case_hex

# this function takes word (8 hexadecimal string) it may be in form of matrix or string, then lookup values in s-box table
def byte_substitution(word_or_matrix, s_box):
    hex_order = "0123456789ABCDEF"
    if type(word_or_matrix) == list:
        substituted_matrix = []

        for row_index in range(4):
            row = []
            for column_index in range(4):
                field = word_or_matrix[row_index][column_index]
                field_to_hex = [bin_to_hex(field[i:i+4])
                                for i in range(0, 8, 4)]
                if len(field_to_hex) < 2:
                    field_to_hex = "0" + field_to_hex
                substituted_field = get_sbox_entry(
                    int(hex_order.index(field_to_hex[0])), int(hex_order.index(field_to_hex[1])), s_box)

                row.append(substituted_field)
            substituted_matrix.append(row)

        return substituted_matrix
    else:
        substituted_word = ''
        for i in range(4):
            word = word_or_matrix[8*i: 8*(i+1)]
            substituted_field = get_sbox_entry(
                int(hex_order.index(bin_to_hex(word[:4]))), int(hex_order.index(bin_to_hex(word[4:]))), s_box)
            substituted_word += substituted_field

        return substituted_word

####################################################################################################
###########################################KEY DERIVATION###########################################
####################################################################################################

# this function takes word (8 hexadecimal string) and return  it after shift it byte to left
def byte_left_shift(word_from_key):
    new_word = word_from_key[8:] + word_from_key[:8]
    return new_word

# this function take word and round number and apply g-Function on it
def g_Function(word_from_key, round):
    # Round Coefficients
    round_coefficient = ["01000000", "02000000", "04000000", "08000000",
                         "10000000", "20000000", "40000000", "80000000", "1B000000", "36000000"]
    lefted_shift_word = byte_left_shift(word_from_key)
    substituted_word = byte_substitution(lefted_shift_word, Sbox)
    result = xor(hex_to_binary(substituted_word),
                 hex_to_binary(round_coefficient[round]))

    return result

# this function takes words of key and return all 11 round keys
def generate_round_keys(key_words):
    round_keys = []
    round_keys.append(key_words)

    for round in range(0, sub_key_numbers):
        words = []
        g_function_result = g_Function("".join(round_keys[round][3]), round)
        first_word_in_pre_round = round_keys[round][0]

        first_word_in_curr_round = xor(
            first_word_in_pre_round,  g_function_result)
        words.append(first_word_in_curr_round)

        for j in range(1, 4):
            words.append(xor(round_keys[round]
                         [j], words[j-1]))
        round_keys.append(words)
    return round_keys

# this function takes state matrix and return it after shift its rows
def shift_rows(fbf_matrix):
    rows = []
    for r in range(4):
        rows.append(fbf_matrix[r])
        rows[r] = fbf_matrix[r][r:] + fbf_matrix[r][:r]
    fbf_matrix = rows
    return fbf_matrix

# this function takes state matrix and return it after shift its rows
def inv_shift_rows(fbf_matrix):
    rows = []
    for r in range(4):
        rows.append(fbf_matrix[r])
        rows[r] = fbf_matrix[r][-r:] + fbf_matrix[r][:-r]
    fbf_matrix = rows
    return fbf_matrix


mix_column_matrix = [
    ["02", "03", "01", "01"],
    ["01", "02", "03", "01"],
    ["01", "01", "02", "03"],
    ["03", "01", "01", "02"]]

inv_mix_column_matrix = [
    ["0E", "0B", "0D", "09"],
    ["09", "0E", "0B", "0D"],
    ["0D", "09", "0E", "0B"],
    ["0B", "0D", "09", "0E"]]


def gf_multiplication(a, b):

    if b == "01":
        return a

    tmp = a[1:] + "0"
    if b == "02":
        return tmp if a[0] == "0" else xor(tmp, "00011011")
    if b == "03":
        return xor(gf_multiplication(a, "02"), a)


def mix_columns(mc_matrix, fbf_matrix):
    result_matrix = []
    fbf_matrix_cols = [[row[i] for row in fbf_matrix] for i in range(4)]
    mc_matrix_rows = mc_matrix
    for mc_matrix_row in mc_matrix_rows:
        rows = []
        for fbf_matrix_col in fbf_matrix_cols:

            sum = gf_multiplication(
                hex_to_binary(fbf_matrix_col[0]), mc_matrix_row[0])
            for i in range(1, 4):
                hex = gf_multiplication(hex_to_binary(
                    fbf_matrix_col[i]), mc_matrix_row[i])

                sum = xor(sum, hex)
            rows.append(sum)
        result_matrix.append(rows)
    return result_matrix


def inv_mix_columns(inv_mc_matrix, fbf_matrix):
    result_matrix = []
    fbf_matrix_cols = [[row[i] for row in fbf_matrix] for i in range(4)]
    mc_matrix_rows = inv_mc_matrix
    for mc_matrix_row in mc_matrix_rows:
        rows = []
        for fbf_matrix_col in fbf_matrix_cols:
            a = fbf_matrix_col[0]
            b = hex_to_binary(mc_matrix_row[0])
            sum = multiply(a, b)[-8:]
            for i in range(1, 4):
                a = fbf_matrix_col[i]
                b = hex_to_binary(mc_matrix_row[i])
                x = multiply(a, b)[-8:]

                sum = xor(sum, x)
            rows.append(sum)
        result_matrix.append(rows)
    return result_matrix

# this function 128 bit binary and put them in a matrix, 8 bit for each cell in this matrix
def bin_to_matrix(binary):
    words = []
    for x in zip(binary[0::8], binary[1::8], binary[2::8], binary[3::8], binary[4::8], binary[5::8], binary[6::8], binary[7::8]):
        word = "".join(x)
        words.append(word)

    matrix = []
    for j in range(4):
        row = []
        for i in range(j, 16, 4):
            row.append(words[i])

        matrix.append(row)
    return matrix

# this function 128 bit binary and put them in a matrix, 8 bit for each cell in this matrix
def hex_to_matrix(hex_):
    words = []
    for x in zip(hex_[0::2], hex_[1::2]):
        word = "".join(x)
        words.append(word)

    matrix = []
    for j in range(4):
        row = []
        for i in range(j, 16, 4):
            row.append(words[i])

        matrix.append(row)
    return matrix

# this function do xor for each element in key matrix and corespond field in message matrix
def add_round_key(fbf_matrix, k_matrix):
    matrix = []
    for row in range(4):
        rows = []
        for col in range(4):
            rows.append(xor(k_matrix[row][col], fbf_matrix[row][col]))
        matrix.append(rows)
    return matrix

def block_encrypt(message, round_keys):
    
    bin_message = hex_to_binary(message)
    message_matrix = bin_to_matrix(bin_message)
    message_key_added = add_round_key(message_matrix, bin_to_matrix("".join(round_keys[0])))
    for i in range(1, sub_key_numbers+1):
        substituted = byte_substitution(message_key_added, Sbox)
        rows_shited = shift_rows(substituted)
        if i != sub_key_numbers:
            columns_mixed = mix_columns(mix_column_matrix, rows_shited)
            message_key_added = add_round_key(
                columns_mixed, bin_to_matrix("".join(round_keys[i])))

        else:
            substituted = byte_substitution(message_key_added, Sbox)
            rows_shited = shift_rows(substituted)

            rows_shited = hex_matrix_to_bin(rows_shited)

            message_key_added = add_round_key(
                rows_shited, bin_to_matrix("".join(round_keys[i])))
    encrypted_message_cols = [[row[i]
                               for row in message_key_added] for i in range(4)]
    encrypted_message = "".join(["".join(col)
                                for col in encrypted_message_cols])
    return encrypted_message
    
def block_decrypt(encrypted, round_keys):

    encrypted_as_bin = hex_to_binary(encrypted)
    encrypted_matrix = bin_to_matrix(encrypted_as_bin)

    encrypted_key_added = add_round_key(
        encrypted_matrix, bin_to_matrix("".join(round_keys[-1])))

    rows_shited = inv_shift_rows(encrypted_key_added)

    substituted = byte_substitution(rows_shited, Sbox_inv)
    substituted = hex_matrix_to_bin(substituted)
    encrypted_key_added = add_round_key(
        substituted, bin_to_matrix("".join(round_keys[-2])))
    columns_mixed = inv_mix_columns(inv_mix_column_matrix, encrypted_key_added)

    for i in range(sub_key_numbers-2, -1, -1):
        rows_shited = inv_shift_rows(columns_mixed)
        substituted = byte_substitution(rows_shited, Sbox_inv)

        if i != 0:

            substituted = hex_matrix_to_bin(substituted)
            encrypted_key_added = add_round_key(
                substituted, bin_to_matrix("".join(round_keys[i])))
            columns_mixed = inv_mix_columns(
                inv_mix_column_matrix, encrypted_key_added)

        else:

            substituted = hex_matrix_to_bin(substituted)
            encrypted_key_added = add_round_key(
                substituted, bin_to_matrix("".join(round_keys[i])))
    encrypted_message_cols = [[row[i]
                               for row in encrypted_key_added] for i in range(4)]
    message = "".join(["".join(col) for col in encrypted_message_cols])
    return message

def encrypte(mail, key, mode="ebc"):

    mail_as_hex = mail.encode('utf-8').hex()
    blocks = [mail_as_hex[i:i+32] for i in range(0, len(mail_as_hex), 32)]
    blocks[-1] = blocks[-1] + (len(blocks[-1]) % 32) * "a"  # padding with (a)
    bin_key = hex_to_binary(key)

    key_words = [bin_key[:1*32], bin_key[1*32:2*32],
                 bin_key[2*32:3*32], bin_key[3*32:4*32]]
    round_keys = generate_round_keys(key_words)

    encrypted_mail = ""

    if mode == "ebc":
        for block in blocks:
            encrypted_block = block_encrypt(block, round_keys)

            hex_encrypted_message = "".join(
                [bin_to_hex(encrypted_block[i:i+4]) for i in range(0, 128, 4)])
            encrypted_mail += hex_encrypted_message

        return encrypted_mail, round_keys

    if mode == "cbc":
        added_IV = xor(hex_to_binary(blocks[0]), IV)
        encrypted_block = block_encrypt(bin_to_hex(added_IV), round_keys)
        hex_encrypted_message = "".join(
            [bin_to_hex(encrypted_block[i:i+4]) for i in range(0, 128, 4)])

        encrypted_mail += hex_encrypted_message

        for block in blocks[1:]:
            added_with_pre_c = xor(hex_to_binary(block), encrypted_block)
            encrypted_block = block_encrypt(hex_to_binary(added_with_pre_c), round_keys)

            hex_encrypted_message = "".join(
                [bin_to_hex(encrypted_block[i:i+4]) for i in range(0, 128, 4)])
            encrypted_mail += hex_encrypted_message

        return encrypted_mail, round_keys

def decrypte(encrypted_mail_as_hex, round_keys, mode="ebc"):

    decrypted_mail = ""
    blocks = [encrypted_mail_as_hex[i:i+32] for i in range(0, len(encrypted_mail_as_hex), 32)]

    if mode == "ebc":
        for block in blocks:
            decrypted_block = block_decrypt(block, round_keys)

            hex_decrypted_message = "".join(
                [bin_to_hex(decrypted_block[i:i+4]) for i in range(0, 128, 4)])
            decrypted_mail += hex_decrypted_message

        return decrypted_mail

    if mode == "cbc":
        decrypted_block = block_decrypt(blocks[0], round_keys)
        added_IV = xor(decrypted_block, IV)
        hex_decrypted_message = "".join(
            [bin_to_hex(added_IV[i:i+4]) for i in range(0, 128, 4)])
        decrypted_mail += hex_decrypted_message

        for block in blocks[1:]:
            i = 1
            decrypted_block = block_decrypt(block, round_keys)
            added_IV = xor(decrypted_block, hex_to_binary(blocks[i]))

            hex_decrypted_message = "".join([bin_to_hex(added_IV[i:i+4]) for i in range(0, 128, 4)])
            decrypted_mail += hex_decrypted_message
            i += 1
        return decrypted_mail

mail = "hello there i am IT student"
key = "2b7e151628aed2a6abf7158809cf4f3c"
encrypted_mail, round_keys = encrypte(mail, key)
decrypted_mail = decrypte(encrypted_mail, round_keys).strip("A")
original_message = codecs.decode(decrypted_mail, 'hex').decode("ASCII")
print(f"{encrypted_mail=}")
print(f"{original_message=}")

