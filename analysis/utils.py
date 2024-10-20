# remove duplicates from array
# Flatten array

def remove_elements(original_array, elements_to_remove):
    return [element for element in original_array if element not in elements_to_remove]
