import argparse
import json


def decompress_payload(payload_text):
	"""Decode a JSON payload produced by Compress.compress_to_payload."""
	if not isinstance(payload_text, str):
		raise TypeError("decompress_payload expects a JSON string")

	try:
		payload = json.loads(payload_text)
	except json.JSONDecodeError as exc:
		raise ValueError("Invalid payload: not valid JSON") from exc

	original_length = payload.get("original_length")
	codes = payload.get("codes")
	encoded_bits = payload.get("encoded_bits")

	if not isinstance(original_length, int) or original_length < 0:
		raise ValueError("Invalid payload: original_length must be a non-negative integer")
	if not isinstance(codes, dict):
		raise ValueError("Invalid payload: codes must be a dictionary")
	if not isinstance(encoded_bits, str):
		raise ValueError("Invalid payload: encoded_bits must be a string")

	if original_length == 0:
		if codes or encoded_bits:
			raise ValueError("Invalid payload: empty text must have empty codes and bits")
		return ""

	reverse_codes = {}
	for symbol, code in codes.items():
		if not isinstance(symbol, str) or len(symbol) != 1:
			raise ValueError("Invalid payload: symbols must be single characters")
		if not isinstance(code, str) or not code or any(bit not in "01" for bit in code):
			raise ValueError("Invalid payload: code values must be non-empty bit strings")
		if code in reverse_codes:
			raise ValueError("Invalid payload: duplicate Huffman code detected")
		reverse_codes[code] = symbol

	current = ""
	output_chars = []

	for bit in encoded_bits:
		if bit not in "01":
			raise ValueError("Invalid payload: encoded_bits contains non-bit characters")
		current += bit
		if current in reverse_codes:
			output_chars.append(reverse_codes[current])
			current = ""

	if current:
		raise ValueError("Invalid payload: leftover undecodable bits")

	output = "".join(output_chars)
	if len(output) != original_length:
		raise ValueError("Invalid payload: decompressed length mismatch")

	return output


def decompress_file(input_path, output_path):
	with open(input_path, "r", encoding="utf-8") as infile:
		payload_text = infile.read()

	text = decompress_payload(payload_text)

	with open(output_path, "w", encoding="utf-8") as outfile:
		outfile.write(text)


def _build_cli():
	parser = argparse.ArgumentParser(description="Decompress Huffman payload")
	parser.add_argument("-i", "--input", required=True, help="Input payload file path")
	parser.add_argument("-o", "--output", required=True, help="Output text file path")
	return parser


if __name__ == "__main__":
	args = _build_cli().parse_args()
	decompress_file(args.input, args.output)
	print(f"Decompressed text written to: {args.output}")
