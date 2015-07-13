from py_calendrical.days import DayOfWeek

def list_range(ell, date_range):
    """Return those moments in list ell that occur in range 'date_range'."""
    return filter(lambda tee: date_range[0] <= tee <= date_range[1], ell)

# def interval(t0, t1):
#     """Return the range data structure."""
#     return [t0, t1]

# def start(date_range):
#     """Return the start of range 'date_range'."""
#     return date_range[0]

# def end(date_range):
#     """Return the end of range 'range'."""
#     return date_range[1]

# def is_in_range(tee, date_range):
#     """Return True if moment 'tee' falls within range 'date_range',
#     False otherwise."""
#     return date_range[0] <= tee <= date_range[1]


