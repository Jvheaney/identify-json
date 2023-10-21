import json
import sys
import ast

if len(sys.argv) != 2:
    print("You must specify a file to parse.")
    exit()

FILE = sys.argv[1]

def identify(key, struct):
    var_type = type(struct[key])
    if var_type is list:

        if len(struct[key]) == 0:
            return []

        temp = [{}]
        first_element = struct[key][0]
        first_element_type = type(first_element)

        if first_element_type is list:

            temp = []
            temp_pointer = temp
            while True:
                if first_element_type is dict:
                    temp_dict = {}

                    if len(first_element.keys()) == 0:
                        temp_pointer.append({})
                        return temp

                    for list_key in first_element:
                        temp_dict[list_key] = identify(list_key, first_element)
                    temp_pointer.append(temp_dict)
                    return temp
                elif first_element_type is not list:
                    temp_pointer.append(f'{first_element_type}')
                    return temp
                else:
                    if len(first_element) == 0:
                        return []
                    temp_pointer.append([])
                    temp_pointer = temp_pointer[0]
                    first_element = first_element[0]
                    first_element_type = type(first_element)

        elif first_element_type is dict:

            if len(first_element.keys()) == 0:
                temp[0] = {}
                return temp

            for list_key in first_element:
                temp[0][list_key] = identify(list_key, first_element)
            return temp
        else:
            temp[0] = f'{first_element_type}'
            return temp
    elif var_type is dict:
        temp = {}
        if len(struct[key]) == 0:
            temp = {}
            return temp

        for list_key in struct[key]:
            temp[list_key] = identify(list_key, struct[key])
        return temp

    return f'{var_type}'


with open(FILE, 'r') as handle:

    json_struct = ""
    identity = {}
    json_string_unparsed = handle.read()

    try:
        json_struct = json.load(json_string_unparsed)
    except:
        json_struct = ast.literal_eval(json_string_unparsed)

    if len(json_struct) == 0:
        print("The JSON struct has a length of zero.")
        exit()

    for key in json_struct.keys():
        identity[key] = identify(key, json_struct)

    print(json.dumps(identity, sort_keys=False, indent=4))
