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
    
    
    for i in range(len(block_data)):
        if compressed_data[i] == 1:
            decompressed_data[i] = int(mean1)
        else:
            decompressed_data[i] = int(mean0)

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

    original_image = Image.open("girl.jpg").convert("L")

    block_size = 4

    compressed_image = compress_image(original_image, block_size)

    compressed_image.save("compressed_image_AMBTC.jpg")

    print("Image compression using AMBTC complete!")

if __name__ == "__main__":
    main()
