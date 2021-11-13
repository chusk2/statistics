import csv
import math

# read data from command line
def get_data():
    
    while True:
        print('\nOpciones:')
        print('Datos aislados con frecuencia absoluta = 1 --> 1')
        print('Datos repetidos con frecuencia absoluta --> 2')
        data_type = input('Tipo de datos: ')
        
        if data_type in ('1','2'):
            break
        else:
            print('\nOpción incorrecta')
    
    print('Introduzca los datos. Pulsa "enter" sin introducir dato para finalizar entrada de datos.')
    # datos aislados
    if data_type == '1':
        datos = []
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
                return datos
    # datos con frecuencia absoluta
    elif data_type == '2':
        print('Introduce el valor de x y su frecuencia absoluta, separados por un espacio.')
        datos = {}
        while True:
            pair = input('Dato: ')
            if pair:
                pair = pair.split()
                xi, freq = pair
                if not xi.isalpha() and not freq.isalpha():
                    # replace comma with decimal point
                    if ',' in xi:
                            xi = xi.replace(',', '.')
                            xi = float(xi) if not float(xi).is_integer() else int(xi)

                    if ',' in freq:
                            freq = freq.replace(',', '.')
                            freq = float(freq) if not float(freq).is_integer() else int(freq)
                # store the pair: value and absolute frequency
                datos[xi] = freq
                        
            elif pair.isalpha():
                print('¡Solo valores numéricos!\n')
            
            elif pair == '':
                return datos

def freq_table(data):
    """ Returns a freq_table, following this structure:
    ['absolute', 'accumulated absolute', 'relative', 'accumulated relative']"""
    # check the right type of data have been supplied
    if isinstance(data, dict):
        freq_table = []
        # absolute frequencies
        abs_freq = data.values()
        # acumulated absolute frequencies
        n = len(data.values)
        accum_abs_freq = []
        accumulated = 0
        for freq in accum_abs_freq:
            accumulated += freq
            accum_abs_freq.append(accumulated)
        # relative frequencies
        rel_freq = [i/n for i in abs_freq]
        # accumulated relative frequencies
        accum_rel_freq = []
        accumulated = 0
        for freq in rel_freq:
            accumulated += freq
            accum_rel_freq.append(accumulated)
        
        freq_table.append(abs_freq)
        freq_table.append(accum_abs_freq)
        freq_table.append(rel_freq)
        freq_table.append(accum_rel_freq)

        return freq_table
    else:
        print('Wrong type of data. Given data have no frequencies.')



#read data from txt file
with open('ejercicio2.txt', 'r') as file:
    data = file.readlines()
#create a function to clean and prepare data
def clean_data(array):
    # clean new line char and substitute comma with decimal point
    data = [i.replace('\n', '').replace(',', '.') for i in array]
    data = [float(i) for i in data]
    data = [int(i) for i in data if i.is_integer()]
    return data


def gen_csv(data, output_fllename = 'raw_data.csv'):
    # write the data to a csv file
    with open(output_fllename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in data:
            # every new row must be a list
            writer.writerow([line])


def mean(data):
    # isolated values
    if not isinstance(data, dict):
        return sum(data)/len(data)
    # dataset with frequencies
    elif isinstance(data, dict):
        # get the absolute frequencies of dataset
        sumatory_xi_fi = 0
        n = 0 
        for xi, fi in data.items():
            sumatory_xi_fi += xi*fi
            n += fi
        return sumatory_xi_fi / n


def median(data):
    # isolated values
    if not isinstance(data, dict):

        # sample size is odd, take point in position n/2 + 1
        if len(data) % 2 != 0:
            return data[(len(data) -1) // 2]
        # if sample size is even, take next two points to position (n-2) / 2
        elif len(data) % 2 == 0:
            num1 = data[ (len(data) -2 ) // 2 ]
            num2 = data[ (len(data) -2 ) // 2  +1]
            return (num1+num2)/2
    # dataset with frequencies
    elif isinstance(data, dict):
        # get the relative frequencies of dataset
        accumulated_relative_freq = freq_table(data)[3]
        xi = data.keys()
        for value, index in enumerate(accumulated_relative_freq):
            # find first value of x that reaches or exceeds 50% of data
            if value >= 0.5:
                return xi[index]


def std_deviation(data):
    x_mean = mean(data)
    # isolated values
    if not isinstance(data, dict):
        x_square = [i**2 for i in data]
        n = len(data)
        return math.sqrt(sum(x_square)/n - x_mean**2)
    # dataset with frequencies
    elif isinstance(data, dict):
        sumatory_xi2_fi = 0
        n = 0 
        for xi, fi in data.items():
            sumatory_xi2_fi += xi**2*fi
            n += fi
        return math.sqrt(sumatory_xi2_fi / n - x_mean**2)


def mode(data):
    if isinstance(data, dict):
        max_abs_freq = max(data.values())
        for xi, abs_freq in data.items():
            if abs_freq == max_abs_freq:
                return xi

def var_range(data):
    if not isinstance(data):
        return max(data) - min(data)
    elif isinstance(data, dict):
        xi = data.keys()
        return max(xi) - min(xi)

def report(data):
    print('Parámetros estadísticos de la variable x:\n')
    print(f'Media: {mean(data):.3f}')
    print(f'Mediana: {median(data):.3.f}')
    # dataset with freq
    if isinstance(data, dict):
        print(f'Moda: {mode(data)}')
    print(f'Desviación típica: {std_deviation(data):.3.f}')
    print(f'Varianza: {std_deviation(data)**2:.3.f}')
    print(f'Rango: {var_range(data)}')
    