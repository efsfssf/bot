a = ['Lists', 'The first list', '4. Empty', '5. Empty', '6. Lemon', '7. 2 Tangerines']
b = ['The second list is', '3. Apple ', '4. Banana ', '5. Pear', '8. Other']
w = []

x = sorted([
    x for x in a+b
    if x[0].isdigit() and x[3:] != 'Empty'
    ], key=lambda x: int(x[0]))
for x in x: w.append(x)

print('СЛИЯНИЕ:', w)