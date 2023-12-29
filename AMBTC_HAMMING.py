from PIL import Image
import math

def code_embedding(CW,S):
    matrix_multiplication = binary_matrix_multiply(CW)
    z = xor_binary(matrix_multiplication,S)
    print(z)
    table_HM={'001':0, '010':1, '011':2, '100':3, '101':4, '110':5, '111':6}
    ei = table_HM.get(z)
    if(ei!=None):
        print(ei+1)
    if(ei!=None):
        print(CW[ei])
        if(CW[ei]==[1]):
            CW[ei]=[0]
        else:
            CW[ei]=[1]
    return CW

def code_extraction(RCW):
    return (binary_matrix_multiply(RCW))

def binary_matrix_multiply(matrix):
    H= [[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]]
    result = []
    for i in range(len(H)):
        row=[]
        for j in range(len(matrix[0])):
            # Compute the dot product of the i-th row of mat1 and j-th column of mat2
            dot_product = sum(H[i][k] & matrix[k][j] for k in range(len(H[0])))
            row.append(dot_product % 2)
        result.append(row)
        single_list = [item for sublist in result for item in sublist]
        result_string = ''.join(map(str, single_list))
    return result_string

def xor_binary(bin_str1, bin_str2):
    # Ensure both binary strings have the same length
    max_len = max(len(bin_str1), len(bin_str2))
    bin_str1 = bin_str1.zfill(max_len)
    bin_str2 = bin_str2.zfill(max_len)

    # Perform XOR operation bit by bit
    result = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(bin_str1, bin_str2))
    return result

def ambtc_compress_block(block_data):

    mean_intensity = sum(block_data) / len(block_data)

    compressed_data = [0] * len(block_data)
    decompressed_data = [0] * len(block_data)
    mean1=0
    count1=0
    count0=0
    mean0=0

    for i in range(len(block_data)):
        if block_data[i] >= mean_intensity:
            mean1 += block_data[i]
            compressed_data[i] = 1
            count1 +=1
        else:
            mean0 += block_data[i]
            compressed_data[i] = 0
            count0 +=1

    mean1=mean1/count1
    if(count0==0):
        mean0=mean1
    else:
        mean0=mean0/count0

    if((mean1-int(mean1))>=0.5):
        mean1=math.ceil(mean1)
    else:
        mean1=math.floor(mean1)
    if((mean0-int(mean0))>=0.5):
        mean0=math.ceil(mean0)
    else:
        mean0=math.floor(mean0)
    
    print(f"mean1={mean1}")
    print(f"mean0={mean0}")
    binary_mean1 = format(mean1, '08b')
    binary_mean0 = format(mean0, '08b')
    binary_secret = xor_binary(binary_mean1, binary_mean0)
    print(binary_mean1)
    print(binary_mean0)
    print(binary_secret)
    
    print(compressed_data)

    for j in range(0,2):
        hamming=[]
        for i in range(0,7):
            if(j==1):
                hamming.append(compressed_data[i+7])
            else:
                hamming.append(compressed_data[i])
        code_word = [[item] for item in hamming]
        print (code_word)
        if(j==1):
            secret_message = binary_secret[3:6]
        else:
            secret_message = binary_secret[0:3]
        print(secret_message)
        code_word_1=code_embedding(code_word, secret_message)
        single_list = [item for sublist in code_word_1 for item in sublist]
        print(single_list)
        secret_message_bit =code_extraction(code_word_1)
        print(secret_message_bit)
        for i in range(0,7):
            if(j==1):
                compressed_data[i+7]=single_list[i]
            else:
                compressed_data[i]=single_list[i]

    
    for i in range(len(block_data)):
        if compressed_data[i] == 1:
            decompressed_data[i] = mean1
        else:
            decompressed_data[i] = mean0

    print(compressed_data)
    
    return decompressed_data

def compress_image(original_image, block_size):
    width, height = original_image.size

    compressed_image = Image.new("L", (width, height))

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):

            block_data = process_block(original_image, x, y, block_size)

            decompressed_data = ambtc_compress_block(block_data)
            print(decompressed_data)

            for block_y in range(block_size):
                for block_x in range(block_size):
                    compressed_image.putpixel((x + block_x, y + block_y), (decompressed_data[block_y * block_size + block_x]))

    return compressed_image

def process_block(image, start_x, start_y, block_size):

    block_data = [image.getpixel((start_x + block_x, start_y + block_y)) for block_y in range(block_size) for block_x in range(block_size)]

    print(block_data)   

    return block_data

def main():

    original_image = Image.open("zelda.jpg").convert("L")

    block_size = 4

    compressed_image = compress_image(original_image, block_size)

    compressed_image.save("compressed_image_Hamming.jpg")

    print("Image compression using AMBTC Hamming code complete!")

if __name__ == "__main__":
    main()


