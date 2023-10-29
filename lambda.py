lambda_for_odd = lambda: [num for num in range(21) if num % 2 == 0]
lambda_for_pow = lambda x: [num ** 2 for num in x]

result = lambda_for_pow(lambda_for_odd())
print(result)

# print((lambda x: [num ** 2 for num in x])((lambda: [num for num in range(21) if num % 2 == 0])())) - чисто если хочется голову поломать)