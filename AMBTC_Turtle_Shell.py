from PIL import Image
import math

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
    secret_bits = compressed_data[0:15]
    print(secret_bits)
    secret_bit_string=''.join(map(str,secret_bits))
    print(secret_bit_string)
    secret_bit=secret_bit_string[0:3]
    j=3
    for i in range(0,4):
        secret_bit= xor_binary(secret_bit,secret_bit_string[j:j+3])
        print(secret_bit)
        j=j+3
    secret_bit=int(secret_bit, 2)
    print(secret_bit)
    new_mean1,new_mean0=turtle_shell(mean1,mean0,secret_bit)
    for i in range(len(block_data)):
        if compressed_data[i] == 1:
            decompressed_data[i] = int(new_mean1)
        else:
            decompressed_data[i] = int(new_mean0)

    print(compressed_data)
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
            if(turtle_matrix[i][j]==SB):
                new_D=euclidean_distance(AvgH,AvgL,i,j)
                print(new_D)
                if(new_D<D):
                    D=new_D
                    print(i,j)
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

    compressed_image.save("compressed_image_turtle_shell.jpg")

    print("Image compression using AMBTC Turtle Shell complete!")

if __name__ == "__main__":
    main()
