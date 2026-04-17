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

def build_huffman_tree(node_list):
    while len(node_list) > 1:
        node1 = node_list.pop(0)
        node2 = node_list.pop(0)
        parent_node = {
            'frequency': node1['frequency'] + node2['frequency'],
            'left': node1,
            'right': node2
        }
        node_list.append(parent_node)
        node_list.sort(key=lambda node: node['frequency'])
    return node_list[0]

