def radix_lsd(numbers):
    max_num = max(numbers)

    exponent = 1
    while max_num / exponent >= 1:
        numbers = counting_sort(numbers, exponent)
        exponent *= 10

    return numbers


def counting_sort(numbers, digit_exp):
    """

    :param numbers: The list of numbers
    :param digit_exp: This should be 10^digit_number
    :return:
    """

    n = len(numbers)
    output = [0] * n
    count = [0] * 10

    # now we will store the number of of each index in array
    for i in range(0, n):
        count[int(numbers[i] / digit_exp) % 10] += 1

    # this indicates where that digit should be stored in the array
    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = int(numbers[i] / digit_exp) % 10
        output[count[index] - 1] = numbers[i]
        count[index] -= 1
        i -= 1

    return output
