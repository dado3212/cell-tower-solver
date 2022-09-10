def is_number_composable(number: int, minNumber: int, maxNumber: int) -> bool:
    if number < minNumber:
        return False
    if number >= minNumber and number <= maxNumber:
        return True
    if number > maxNumber:
        for subtract in range(minNumber, maxNumber + 1):
            if is_number_composable(number - subtract, minNumber, maxNumber):
                return True
    return False
