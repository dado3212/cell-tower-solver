def is_number_composable(number: int, minNumber: int, maxNumber: int) -> bool:
    if number < minNumber:
        return False
    if number >= minNumber and number <= maxNumber:
        return True
    if number > maxNumber:
        # Try some hacky things first
        if number > maxNumber * 3:
            if is_number_composable((number % maxNumber) + maxNumber * 2, minNumber, maxNumber):
                return True
        for subtract in range(minNumber, maxNumber + 1):
            if is_number_composable(number - subtract, minNumber, maxNumber):
                return True
    return False
