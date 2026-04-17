def count_frequencies(text):
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies

def create_sorted_node_list(frequencies):
    node_list= [{'symbol' : char, 'frequency' : count} for char, count in frequencies.items()]
    node_list.sort(key=lambda node:node['frequency'])
    return node_list

# Temporary Test Code (Delete before submitting)
test_text = "aaabbc"
freqs = count_frequencies(test_text)
nodes = create_sorted_node_list(freqs)
print(nodes)