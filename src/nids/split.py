def day_based_split(frame, train_days=("Monday",), validation_days=("Tuesday",), test_days=("Wednesday","Thursday","Friday")):
    if "__source_day" not in frame:
        raise ValueError("Missing __source_day metadata.")
    a = frame[frame["__source_day"].isin(train_days)].copy()
    b = frame[frame["__source_day"].isin(validation_days)].copy()
    c = frame[frame["__source_day"].isin(test_days)].copy()
    if a.empty or b.empty or c.empty:
        raise ValueError("Missing one or more required weekday partitions; no chronology is fabricated.")
    return a, b, c
