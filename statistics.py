import csv
# use math.sqrt() for standard deviation
import math


def clean_data(data):
    """
    Cleans the dataset as strings and transforms them into integer or floats
    """
    # clean new line char and substitute comma with decimal point
    processed_data = [line.replace('\n', '').replace(',', '.')
                      for line in data]
    # transform string values into integer or float
    for value, index in enumerate(processed_data):
        if float(value).is_integer():
            processed_data[index] = int(value)
        else:
            processed_data[index] = float(value)
    return processed_data


def read_from_txt(filename):
    """
    Reads dataset from a txt file and generates a list of data
    """
    # read data from txt file
    with open(filename, 'r') as file:
        data_as_str = file.readlines()
    # clean the strings of data
    data = clean_data(data_as_str)
    return data


def read_from_csv(filename):
    with open(filename, 'r'):
        reader = csv.reader(filename)
        data_as_str = list(reader)
        return clean_data(data_as_str)


def from_txt_to_csv(txt_filename, output_filename='output_dataset.csv'):
    with open(txt_filename, 'r') as f:
        data_as_str = f.readlines()
        clean_dataset = clean_data(data_as_str)
    with open(output_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(clean_dataset)
    # func does not return anything but a csv file


def manual_entry_data():
    """
    Asks repeatedly for values until no value + enter key is entered.
    Returns the list with entered data.
    """
    while True:
        print('\nOpciones:')
        print('Datos aislados --> 1')
        print('Datos repetidos con frecuencia absoluta --> 2')

        data_type = input('Tipo de datos: ')
        
        if data_type in ('1', '2'):
            break
        else:
            print('\nOpción incorrecta')
    
    print('Introduzca los datos. Pulsa "enter" sin introducir dato'
          'para finalizar entrada de datos.')

    # datos aislados
    if data_type == '1':
        datos = []
        while True:
            num = input('Dato: ')
            if num:
                if num.isalpha():
                    print('¡Solo valores numéricos!\n')
                    continue
                else:
                    datos.append(num)

            elif num == '':
                return datos

    # datos con frecuencia absoluta
    elif data_type == '2':
        print('Introduce el valor de x y su frecuencia absoluta,'
              'separados por un espacio.')

        while True:
            pair = input('Dato: ')
            if pair:
                pair = pair.split()
                xi, freq = pair

            elif pair.isalpha():
                print('¡Solo valores numéricos!\n')
            
            elif pair == '':
                break
        # create tuples (xi, absolute frequency)
        xi = clean_data(xi)
        freq = clean_data(freq)
        datos = []
        for i in range(len(xi)):
            datos.append((xi[i], freq[i]))
        datos = sorted(datos, key = lambda j: j[0])

        return datos


def categorize_continuous_var(data):
    """
    Process data of continuous variable.
     Returns two lists:
        1. [strings with intervals]
        2. [(class mark, absolute frequency)]
    """
    # calculate how many classes and their amplitud using formula
    n = len(data)
    number_of_classes = round(1 + 3.322 * math.log10(n))
    class_width = (max(data) - min(data)) // number_of_classes

    # user defined num of classes and width
    print(f'Suggested number of intervals is {number_of_classes} '
          f'and interval width is {class_width}.')
    print('If this is ok, just press enter.'
          'Otherwise, enter your own values, separated by a comma.')
    answer = input('Number of intervals and their amplitude: ')
    if answer:
        number_of_classes, class_width = answer.split(',')

    # generate list of classes, class mark and their absolute frequency
    data.sort()

    # create a list of strings with class interval
    classes_limits_str = []
    classes_limits_numbers = []
    lower_limit = min(data)
    for i in range(1, number_of_classes + 1):
        classes_limits_numbers.append((lower_limit, lower_limit + class_width))
        classes_limits_str.append(
            f'[{lower_limit}, {lower_limit + class_width})')
        # increment the lower limit by adding the class amplitud
        lower_limit += class_width

    # categorize values of x in the corresponding class
    data_precategorized = data.copy()
    data_categorized = []
    for interval in classes_limits_numbers:
        data_categorized.append([])
        lower = interval[0]
        upper = interval[1]
        # finish if there are no more values to categorize
        if data_precategorized:
            for xi, index in enumerate(data_precategorized):
                if lower <= xi < upper:
                    data_categorized[-1].append(xi)
                    # remove item from precategorized dataset
                    # next iteration of search for values within interval
                    # will last less because values are crossed out
                    data_precategorized.pop(index)

    # generate list of mark classes and their absolute frequencies
    xi = []
    abs_freq = []
    for i in range(len(data_categorized)):
        # class mark. Average of lower and upper limit of interval
        xi.append(classes_limits_numbers[0] + class_width / 2)
        # absolute frequency of class
        abs_freq.append(len(data_categorized))
    # create a list with tuples (class mark, abs freq)
    dataset = []
    for i in range(len(xi)):
        dataset.append((xi[i], abs_freq[i]))
    # sort pairs of (value,abs freq). Use value as sorting criterium
    dataset = sorted(dataset, key=lambda j: j[0])

    return classes_limits_str, dataset


def freq_table(data):
    """
    Returns a freq_table, following this structure:
    ['absolute', 'accumulated absolute', 'relative', 'accumulated relative']
    """
    # check the right type of data have been supplied
    if isinstance(data, dict):
        freq_table = []
        # absolute frequencies
        abs_freq = data.values()
        # acumulated absolute frequencies
        n = len(data.values())
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
            return data[(len(data)-1) // 2]
        # if sample size is even, take next two points to position (n-2) / 2
        elif len(data) % 2 == 0:
            num1 = data[(len(data)-2) // 2]
            num2 = data[(len(data)-2) // 2+1]
            return (num1+num2)/2
    # dataset with frequencies
    elif isinstance(data, dict):
        # get the relative frequencies of dataset
        accumulated_relative_freq = freq_table(data)[3]
        xi = list(data.keys())
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
    if not isinstance(data, dict):
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
