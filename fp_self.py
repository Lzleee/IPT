class TreeNode:
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None

    def inc(self, count):
        self.count += count

def create_tree(transactions, min_support):
    header_table = {}
    for trans in transactions:
        for item in trans:
            header_table[item] = header_table.get(item, 0) + transactions[trans]
    header_table = {k: v for k, v in header_table.items() if v >= min_support}
    if len(header_table) == 0: return None, None
    
    for k in header_table:
        header_table[k] = [header_table[k], None]
    
    root_node = TreeNode('Null Set', 1, None)
    for trans, count in transactions.items():
        local_items = {k: header_table[k][0] for k in trans if k in header_table}
        if len(local_items) > 0:
            ordered_items = [v[0] for v in sorted(local_items.items(), key=lambda v: v[1], reverse=True)]
            update_tree(ordered_items, root_node, header_table, count)
    return root_node, header_table

def update_tree(items, node, header_table, count):
    if items[0] in node.children:
        node.children[items[0]].inc(count)
    else:
        new_node = TreeNode(items[0], count, node)
        node.children[items[0]] = new_node
        if header_table[items[0]][1] == None:
            header_table[items[0]][1] = new_node
        else:
            update_header(header_table[items[0]][1], new_node)
    if len(items) > 1:
        update_tree(items[1:], node.children[items[0]], header_table, count)

def update_header(node_to_test, target_node):
    while node_to_test.node_link != None:
        node_to_test = node_to_test.node_link
    node_to_test.node_link = target_node

def find_prefix_path(base_pat, node):
    cond_pats = {}
    while node != None:
        prefix_path = []
        ascend_tree(node, prefix_path)
        if len(prefix_path) > 1:
            cond_pats[frozenset(prefix_path[1:])] = node.count
        node = node.node_link
    return cond_pats

def ascend_tree(leaf_node, prefix_path):
    if leaf_node.parent != None:
        prefix_path.append(leaf_node.name)
        ascend_tree(leaf_node.parent, prefix_path)

def mine_tree(node, header_table, min_support, pre_fix, freq_item_list):
    big_l = [v[0] for v in sorted([(k, s[0]) for k, s in header_table.items()], key=lambda p: p[1])]
    for base_pat in big_l:
        new_freq_set = pre_fix.copy()
        new_freq_set.add(base_pat)
        freq_item_list.append((list(new_freq_set), header_table[base_pat][0]))
        cond_patt_bases = find_prefix_path(base_pat, header_table[base_pat][1])
        cond_tree, head = create_tree(cond_patt_bases, min_support)
        if head != None:
            mine_tree(cond_tree, head, min_support, new_freq_set, freq_item_list)

def fpgrowth(transactions, min_support):
    freq_items = []
    root_node, header_table = create_tree(transactions, min_support)
    if root_node != None:
        mine_tree(root_node, header_table, min_support, set(), freq_items)
    return freq_items

# Example use
transactions = {
    ('bread', 'milk'): 1,
    ('bread', 'diaper', 'beer', 'egg'): 1,
    ('milk', 'diaper', 'beer', 'cola'): 1,
    ('bread', 'milk', 'diaper', 'beer'): 1,
    ('bread', 'milk', 'diaper', 'cola'): 1
}

min_support = 2
result = fpgrowth(transactions, min_support)
print(result)
