# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code.

# # Part A.
def array_2_dict(emails, contacts):
    # YOUR CODE HERE
    res = {}
    if emails == " ":
        res = contacts
        return res
    else: 
        res = dict(zip(contacts, emails))
           
    return res
        
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

# # Part C.
def dict_2_array(contacts):
    # YOUR CODE HERE

    return

