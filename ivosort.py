def tier_cascade_sort(data, map_grootte=6, laag_pct=0.3, mid_pct=0.4, hoog_pct=0.3):
    from math import floor
    from random import shuffle
    
    def split_map(lst):
        lst.sort()
        n = len(lst)
        l = floor(n * laag_pct)
        m = floor(n * mid_pct)
        h = n - l - m
        return lst[:l], lst[l:l+m], lst[l+m:]
    
    kleine_mappen, midden_mappen, grote_mappen = [], [], []
    buffer = []

    for getal in data:
        buffer.append(getal)
        if len(buffer) >= map_grootte:
            klein, midden, groot = split_map(buffer)
            kleine_mappen.append(klein)
            midden_mappen.append(midden)
            grote_mappen.append(groot)
            buffer = []

    # Verwerk laatste buffer als hij nog iets heeft
    if buffer:
        klein, midden, groot = split_map(buffer)
        kleine_mappen.append(klein)
        midden_mappen.append(midden)
        grote_mappen.append(groot)

    # Samenvoegen
    alles = []
    for m in kleine_mappen + midden_mappen + grote_mappen:
        alles.extend(m)

    # Final check (als niet perfect gesorteerd: gladstrijken)
    def is_sorted(lst):
        return all(lst[i] <= lst[i+1] for i in range(len(lst) - 1))

    if not is_sorted(alles):
        # Laatste pass: insertion sort (licht en efficiënt op bijna-gesorteerde data)
        for i in range(1, len(alles)):
            key = alles[i]
            j = i - 1
            while j >= 0 and alles[j] > key:
                alles[j + 1] = alles[j]
                j -= 1
            alles[j + 1] = key

    return alles

lijst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6 ,7, 8, 9 ,12, 34, 45, 675, 78, 234, 768, 23, 678, 12, 234, 67, 90 ,56, 5, 56, 2345, 867, 34, 756, 3214, 56748, 23415, 5674, 3425, 5674, 3245, 4356, 32456, 756, 354, 6453, 4356, 6, 6345, 67, 64573, 46357, 5234 ,67589 ,56789, 5746]
print("Oorspronkelijk:", lijst)
gesorteerd = tier_cascade_sort(lijst)
print("Gesorteerd:   ", gesorteerd)
