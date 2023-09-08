def merge_nested_dicts(a, b):
    c = {}
    
    # Merge dictionary 'a' into 'c'
    for key_a, value_a in a.items():
        if key_a in c:
            # Merge subvalue and featurename
            for subkey, subvalue in value_a.items():
                if subkey in c[key_a]:
                    c[key_a][subkey].extend(subvalue)
                else:
                    c[key_a][subkey] = subvalue
        else:
            c[key_a] = value_a
    
    # Merge dictionary 'b' into 'c'
    for key_b, value_b in b.items():
        if key_b in c:
            # Merge subvalue and featurename
            for subkey, subvalue in value_b.items():
                if subkey in c[key_b]:
                    c[key_b][subkey].extend(subvalue)
                else:
                    c[key_b][subkey] = subvalue
        else:
            c[key_b] = value_b
    
    return c

# Example dictionaries a and b
a = {
    'subvalue1': {
        'featurename1': [
            {'feature1': 'featurevalue1'},
            {'feature2': 'featurevalue2'}
        ]
    }
}

b = {
    'subvalue2': {
        'featurename2': [
            {'featurea': 'featurevaluea'},
            {'featureb': 'featurevalueb'}
        ]
    }
}

# Merge dictionaries a and b into c
c = merge_nested_dicts(a, b)
print(c)
