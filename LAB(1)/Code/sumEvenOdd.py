even_sum = 0                                                                                                                                             
odd_sum = 0                                                                                                                                              
while True:                                                                                                                                              
    n = int(input("Enter number (0 to stop): "))                                                                                                         
    if n == 0:                                                                                                                                           
        break                                                                                                                                            
    if n % 2 == 0:                                                                                                                                       
        even_sum += n                                                                                                                                    
    else:                                                                                                                                                
            odd_sum += n                                                                                                                                     
print("Even sum:", even_sum)                                                                                                                             
print("Odd sum:", odd_sum)