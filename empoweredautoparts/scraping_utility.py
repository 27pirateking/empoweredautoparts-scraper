

def preprocess_descrip_array(des_array):
    remove_index=-1
    for index in range(0,len(des_array)):
        if "Rotors are a direct bolt on item".lower() in des_array[index].lower():
            remove_index = index
            continue
        if "Disc wear is reduced by up to 50% with".lower() in des_array[index].lower():
            remove_index = index
            continue
        if "Empowered Auto Parts is an authorised".lower() in des_array[index].lower():
            remove_index = index
    if remove_index > 0:
        des_array = des_array[0:remove_index]
    return des_array

def process_description(des_item, descrip_html):
    descrip_html = preprocess_descrip_array(descrip_html)

    index = 0
    compatible_models=-1
    features=-1
    product_highlights=-1
    you_are_buying=-1
    product_specifications=-1

    for aa in descrip_html:
        index+= 1
        if "COMPATIBLE MODELS".lower() in aa.lower():
            compatible_models = index-1
            continue

        if "FEAURES".lower() in aa.lower():
            features = index-1
            continue

        if "PRODUCT HIGHLIGHTS".lower() in aa.lower():
            product_highlights = index-1
            continue

        if "YOU ARE BUYING".lower() in aa.lower():
            you_are_buying = index-1
            continue

        if "PRODUCT SPECIFICATIONS".lower() in aa.lower():
            product_specifications = index-1
            continue

    descrips = [compatible_models,features,product_highlights,you_are_buying,product_specifications]
    descrips.append(len(descrip_html))
    descrips.sort()
    keys = [i for i in descrips if i >= 0]
    iter_keys = iter(keys)

    des_item['description'] = ''.join(descrip_html[0:next(iter_keys)])
    last_index = compatible_models + 1

    if compatible_models >= 0:
        next_last_index = next(iter_keys)
        des_item['compatible_models'] = ''.join(descrip_html[last_index:next_last_index])
        last_index=next_last_index + 1
    else:
        des_item['compatible_models'] = '.'

    if features >= 0:
        next_last_index = next(iter_keys)
        des_item['features'] = ''.join(descrip_html[last_index:next_last_index])
        last_index=next_last_index + 1
    else:
        des_item['features'] = '.'

    if product_highlights >= 0:
        next_last_index = next(iter_keys)
        des_item['product_highlights'] = ''.join(descrip_html[last_index:next_last_index])
        last_index=next_last_index + 1
    else:
        des_item['product_highlights'] = '.'

    if you_are_buying >= 0:
        next_last_index = next(iter_keys)
        des_item['you_are_buying'] = ''.join(descrip_html[last_index:next_last_index])
        last_index=next_last_index + 1
    else:
        des_item['you_are_buying'] = '.'

    if product_specifications >= 0:
        next_last_index = next(iter_keys)
        des_item['product_specifications'] = ''.join(descrip_html[last_index:next_last_index])
    else:
        des_item['product_specifications'] = '.'

    return des_item
