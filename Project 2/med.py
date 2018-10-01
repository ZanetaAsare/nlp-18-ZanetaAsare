#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def med(source,target):
    
    n = len(source)
    m = len(target)
    edit = 0
    
    s_list = list(source)         #splitting the string into a list of characters
    t_list = list(target)
    
    d = [0] * (n+1)             #creating the rows
    
    for i in range(n+1):  
        d[i] = [0] * (m+1)      #creating the columns
        
    d[0][0] = 0
    
    for i in range(1,n+1):            #calculating the values for the first row, ie. from empty string to n characters
        d[i][0] = d[i-1][0] + 1
        
    
    for j in range(1,m+1):       #calculating values for the first column, ie. from empty string to m characters
        d[0][j] = d[0][j-1] + 1
        
    
    for i in range(1,n+1):
        for j in range(1,m+1):    #an iteration through each position in the matrix
            
            if s_list[i-1] == t_list[j-1]:      #comparing characters to see if they are equal or not to find the cost of substitution
                edit = 0
            else:
                edit = 2      
            
            d[i][j] = min(d[i-1][j]+1,d[i-1][j-1]+edit,d[i][j-1]+1)      #finding the minimum amongst the three computations
            
            
    
    dis = d[n][m]
    
    print("Minimum edit distance between",source,"and",target,"is" ,dis)

    


# In[ ]:




