import re

lower_bound = 172930
upper_bound = 683082


# for x0 in range(int(lower_bound[0]),int(upperbound[0])+1):
#     #print(x0)
#     for x1 in range(int(lower_bound[1]), int(upperbound[1]) + 1):
#         #print(x1)
#         for x2 in range(int(lower_bound[2]), int(upperbound[2]) + 1):
#             for x3 in range(int(lower_bound[3]), int(upperbound[3]) + 1):
#                 for x4 in range(int(lower_bound[4]), int(upperbound[4]) + 1):
#                     for x5 in range(int(lower_bound[5]), int(upperbound[5]) + 1):
#
#                         print(counter)
#                         lis = [x0, x1, x2, x3, x4,x5]
#                         if all(lis[i] <= lis[i+1] for i in range(1,5)):
#
#                             counter=counter+1
#                             print(counter)

#print(re.findall(r'(.)\1{1,1}',"999599"))
#print(re.match(r"(.)\1{1,1}(.)\1{1,1}(.)\1{1,1}", "999999dasd").groups())
range_of_numbers = range(lower_bound, upper_bound+1)
#print (min(range_of_numbers))

#range_of_numbers = [111122,123444,112233]

counter = 0
for number in range_of_numbers:
    str1 = str(number)
    check1 = re.findall(r'(.)\1{1}',str1)
    #print(number, check1)
    if check1:
        #print(number, check1)
        for i in check1:
            #print (f'checking for groups of {i} in {number}')
            check2 = re.findall(rf'({i})\1{{2}}',str1)
            #print(not check2)
            if not check2 and all(str1[i] <= str1[i+1] for i in range(0,len(str1)-1)):
                #print(number)
                counter = counter + 1
                break
    #check = re.findall(r'(.)\1{1}',str1) and re.search(r)
    #if check1: #and not re.search(r'(.)\1{2}',str1) and not re.search(r'(.)\1{4}',str1):
        #check2 = check[0][0]
        #print(check)
        #print(rf'({check2})\1{{1}}')

        # if not re.search(rf'({check2})\1{{2}}', str1):
        #     #print(check[0])
        #     if :

        #         print(number)

print(counter)
exit(0)




#    for x2 in range(7, 9)
#        for x3 in range ()
#    print(x1)