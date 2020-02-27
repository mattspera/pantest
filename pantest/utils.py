# Utility Functions

def compare_dict(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    changed = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    #same = set(o for o in intersect_keys if d1[o] == d2[o])

    diff = {
        'added' : added, # this k, v pair denotes keys found in d2 but not in d1
        'removed' : removed, # this k, v pair denotes keys found in d1 but not in d2
        'changed [baseline, tvt]' : changed # this k, v pair denotes keys found in both d1 and d2 with a modified value
    }

    return diff

def compare_list(l1, l2):
    added = sorted(list(set(l2) - set(l1)))
    removed = sorted(list(set(l1) - set(l2)))

    diff = {
        'added' : added, # denotes items found in l2 but not in l1
        'removed' : removed, # denotes items found in l1 but not in l2
    }

    return diff

def find_seq_number(log_type, s):
    line_list = s.splitlines()

    target_log_list = []

    for line in line_list:
        if log_type in line:
            target_log_list.append(line)

    seq_number_list = []

    for item in target_log_list:
        item_line_list = item.split(' ')
        for item in item_line_list:
            if item.isdigit() and not item == '0':
                seq_number_list.append(item)

    last_fwd_seq = seq_number_list[0]

    return last_fwd_seq