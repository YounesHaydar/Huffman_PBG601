import argparse
import json


def count_frequencies(text):
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies


def create_sorted_node_list(frequencies):
    node_list = [{"symbol": char, "frequency": count} for char, count in frequencies.items()]
    node_list.sort(key=lambda node: (node["frequency"], node.get("symbol", "")))
    return node_list


def build_huffman_tree(node_list):
    if not node_list:
        return None

    while len(node_list) > 1:
        node1 = node_list.pop(0)
        node2 = node_list.pop(0)
        parent_node = {
            "frequency": node1["frequency"] + node2["frequency"],
            "left": node1,
            "right": node2,
        }
        node_list.append(parent_node)
        node_list.sort(key=lambda node: node["frequency"])
    return node_list[0]


def generate_huffman_codes(node, code, codes):
    if node is None:
        return

    if "symbol" in node:
        # Single-symbol input still needs a usable code.
        codes[node["symbol"]] = code or "0"
    else:
        if "left" in node:
            generate_huffman_codes(node["left"], code + "0", codes)
        if "right" in node:
            generate_huffman_codes(node["right"], code + "1", codes)


def encode_text(text, codes):
    return "".join(codes[char] for char in text)


def compress_to_payload(text):
    """Compress text and return a JSON payload string."""
    if not isinstance(text, str):
        raise TypeError("compress_to_payload expects a string")

    if text == "":
        payload = {"original_length": 0, "codes": {}, "encoded_bits": ""}
        return json.dumps(payload, ensure_ascii=False)

    frequencies = count_frequencies(text)
    node_list = create_sorted_node_list(frequencies)
    tree = build_huffman_tree(node_list)

    codes = {}
    generate_huffman_codes(tree, "", codes)

    encoded_bits = encode_text(text, codes)
    payload = {
        "original_length": len(text),
        "codes": codes,
        "encoded_bits": encoded_bits,
    }
    return json.dumps(payload, ensure_ascii=False)


def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        text = infile.read()

    payload = compress_to_payload(text)

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(payload)


def _build_cli():
    parser = argparse.ArgumentParser(description="Compress text with Huffman coding")
    parser.add_argument("-i", "--input", required=True, help="Input text file path")
    parser.add_argument("-o", "--output", required=True, help="Output payload file path")
    return parser


if __name__ == "__main__":
    args = _build_cli().parse_args()
    compress_file(args.input, args.output)
    print(f"Compressed payload written to: {args.output}")



