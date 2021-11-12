datos = []

print('Introduzca los datos...')

while True:
    num = input('Dato: ')
    if num:
        if not num.isalpha():
            # replace comma with decimal point
            if ',' in num:
                num = num.replace(',', '.')
            datos.append(float(num))
    
    elif num.isalpha():
        print('¡Solo valores numéricos!\n')
    
    elif num == '':
        break
print('Los valores introducidos son:\n')
print(datos)
mean = sum(datos)/len(datos)

        