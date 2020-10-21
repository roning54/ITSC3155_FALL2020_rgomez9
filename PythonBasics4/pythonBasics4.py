# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code.

# # Part A.
def array_2_dict(emails, contacts):
    # YOUR CODE HERE
    if emails:
        names = sorted(list(contacts))
        emails = sorted(emails)
        res = dict(zip(names, emails))
        return res
    return contacts
        
# # Part B.
def array2d_2_dict(contact_info, contacts):
    # YOUR CODE HERE
    if contact_info:
        d = {}
        i = 0
        contact = contact_info
        for keys in contacts:
            contact = contact_info[i]
            d[keys] = dict(email = contact[0], phone = contact[1])
            i += 1
        contacts = d
    return contacts

import numpy as np
# # Part C.
def dict_2_array(contacts):
    # YOUR CODE HERE
    dict = contacts
    result = dict.items() 
    data = list(result) 
    numpyArray = np.array(data) 
     
    return numpyArray

