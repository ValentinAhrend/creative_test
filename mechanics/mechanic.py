def bound(min_value, max_value, value, new_max_value):
    """
    bounds a value into the correct relation between to new boundaries
    :param min_value: the old boundary min value
    :param max_value: the old boundary max value
    :param value: the value that should be renewed
    :param new_max_value: the new boundary max value
    :return: the value in the correct bound (from new_min_value to new_max_value)

    Example:
    bound(0, 20, 15, 0, 1)
    >> 0.75

    """
    if min_value != 0:
        max_value -= min_value
        value -= min_value
    x = value / float(max_value) * float(new_max_value)
    return x
