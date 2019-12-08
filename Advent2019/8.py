def create_layers(input_string, layer_width, layer_height):
    index = 0
    layer_size = layer_width * layer_height
    layers = []
    while index + layer_size <= len(input_string):
        layers.append(input_string[index : index + layer_size])
        index += layer_size
    return layers

def find_fewest_zeroes(layers, layer_width, layer_height):
    fewest_zeroes = layer_width * layer_height
    fewest_zero_index = -1
    for index, layer in enumerate(layers):
        zero_count = layer.count("0")
        if zero_count < fewest_zeroes:
            fewest_zeroes = zero_count
            fewest_zero_index = index
    return fewest_zero_index

def create_image(layers, layer_width, layer_height):
    layer_size = layer_width * layer_height
    final_image = ["2"] * layer_size
    for layer in layers:
        for i, char in enumerate(layer):
            if final_image[i] == "2" and char != "2":
                final_image[i] = char
    return "".join(final_image)

def print_image(image_data, layer_width, layer_height):
    index = 0
    layer_size = layer_width * layer_height
    image_list = []
    # Convert 1s and 0s to asterisks and spaces
    for char in image_data:
        image_list.append("*" if char == "1" else " ")
    image = "".join(image_list) 
    while index + layer_width <= layer_size:
        print(image[index:index + layer_width])
        index += layer_width

if __name__ == "__main__":
    # Tests
    layers = create_layers("123456789012", 3, 2)
    assert layers[0] == "123456" and layers[1] == "789012", "Part one test failed"
    layers = create_layers("0222112222120000", 2, 2)
    assert layers[0] == "0222" and layers[1] == "1122" and layers[2] == "2212" and layers[3] == "0000", \
        "Part two test 1 failed"
    image = create_image(layers, 2, 2)
    assert image == "0110", "Part two test 2 failed"

    with open("8.txt") as infile:
        digits = infile.readline().strip()
    layers = create_layers(digits, 25, 6)

    fewest_zero_index = find_fewest_zeroes(layers, 25, 6)

    zero_count = layers[fewest_zero_index].count("0")
    one_count = layers[fewest_zero_index].count("1")
    two_count = layers[fewest_zero_index].count("2")
    print(f"Part one: fewest zeros: {zero_count}. 1s * 2s = {one_count * two_count}")

    assert zero_count == 7 and one_count * two_count == 2460, "Part one is no longer correct"

    image = create_image(layers, 25, 6)
    print_image(image, 25, 6)
