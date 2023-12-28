from PIL import Image
import math
import os

def code_embedding(CW,S):
    matrix_multiplication = binary_matrix_multiply(CW)
    z = xor_binary(matrix_multiplication,S)
    table_HM={'001':0, '010':1, '011':2, '100':3, '101':4, '110':5, '111':6}
    ei = table_HM.get(z)
    if(ei!=None):
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
    
    binary_mean1 = format(mean1, '08b')
    binary_mean0 = format(mean0, '08b')
    binary_secret = xor_binary(binary_mean1, binary_mean0)
 
    secret_bits = compressed_data[0:15]

    for j in range(0,2):
        hamming=[]
        for i in range(0,7):
            if(j==1):
                hamming.append(compressed_data[i+7])
            else:
                hamming.append(compressed_data[i])
        code_word = [[item] for item in hamming]
        if(j==1):
            secret_message = binary_secret[3:6]
        else:
            secret_message = binary_secret[0:3]
        code_word_1=code_embedding(code_word, secret_message)
        single_list = [item for sublist in code_word_1 for item in sublist]
        secret_message_bit =code_extraction(code_word_1)
        for i in range(0,7):
            if(j==1):
                compressed_data[i+7]=single_list[i]
            else:
                compressed_data[i]=single_list[i]
    secret_bit_string=''.join(map(str,secret_bits))
    secret_bit=secret_bit_string[0:3]
    j=3
    for i in range(0,4):
        secret_bit= xor_binary(secret_bit,secret_bit_string[j:j+3])
        j=j+3
    secret_bit=int(secret_bit, 2)
    new_mean1,new_mean0=turtle_shell(mean1,mean0,secret_bit)
    for i in range(len(block_data)):
        if compressed_data[i] == 1:
            decompressed_data[i] = int(new_mean1)
        else:
            decompressed_data[i] = int(new_mean0)

    return decompressed_data

def turtle_shell(AvgH,AvgL,SB):
    x=[0,1,2,3,4,5,6,7]
    k=0
    s=0
    turtle_matrix = [[0 for _ in range(256)] for _ in range(256)]
    for i in range(0,256):
        for j in range(0,256):
            if(k<=7):
                turtle_matrix[i][j]=x[k]
            else:
                k=0
                turtle_matrix[i][j]=x[k] 
            k=k+1
        if(i%2==0):
            for z in range(0,2):
                if(s>7):
                    s=0
                    s=s+1
                else:
                    s=s+1
        else:
            for y in range(0,3):
                if(s>7):
                    s=0
                    s=s+1
                else:
                    s=s+1
        k=s                         

    D=256
    new_high=AvgH
    new_low=AvgL
    for i in range(AvgH-2,AvgH+2):
        for j in range(AvgL-2,AvgL+2):
            if(i>=256 or j>=256):
                i=255
                j=255
            if(turtle_matrix[i][j]==SB):
                new_D=euclidean_distance(AvgH,AvgL,i,j)
                if(new_D<D):
                    D=new_D
                    new_high=i
                    new_low=j
    return (new_high,new_low)

def xor_binary(bin_str1, bin_str2):
    # Ensure both binary strings have the same length
    max_len = max(len(bin_str1), len(bin_str2))
    bin_str1 = bin_str1.zfill(max_len)
    bin_str2 = bin_str2.zfill(max_len)

    # Perform XOR operation bit by bit
    result = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(bin_str1, bin_str2))
    return result

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def compress_image(original_image, block_size):
    width, height = original_image.size

    compressed_image = Image.new("L", (width, height))

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):

            block_data = process_block(original_image, x, y, block_size)

            decompressed_data = ambtc_compress_block(block_data)

            for block_y in range(block_size):
                for block_x in range(block_size):
                    compressed_image.putpixel((x + block_x, y + block_y), (decompressed_data[block_y * block_size + block_x]))

    return compressed_image

def process_block(image, start_x, start_y, block_size):

    block_data = [image.getpixel((start_x + block_x, start_y + block_y)) for block_y in range(block_size) for block_x in range(block_size)]

    return block_data

def process_image(input_path, output_path):
    try:
        # Open the image
        with Image.open(input_path) as img:
            compressed_image = compress_image(img, 4)

            # Extract the filename from the input path
            filename = os.path.splitext(os.path.basename(input_path))[0]

            # Save the processed image to the output folder
            compressed_image.save(os.path.join(output_path, f"{filename}.png"))

    except Exception as e:
        print(f"Error processing image {input_path}: {e}")

def process_images_in_folder(input_folder, output_folder):

    # Traverse the input folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            # Process each image in the input folder
            input_path = os.path.join(root, file)
            process_image(input_path, output_folder)

# Example usage



def main():
    input_folder_path = "input_images"
    output_folder_path = "compressed_images"
    process_images_in_folder(input_folder_path, output_folder_path)

    print("Image compression AMBTC using Hamming Code and Turtle Shell complete!")

if __name__ == "__main__":
    main()
