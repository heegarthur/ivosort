def t_c_s(dat, m_g=6, l_pc=0.3, m_pc=0.4, h_pc=0.3):
    from math import floor
    def s_mp(lst):
        lst.sort()
        n = len(lst)
        l = floor(n * l_pc)
        m = floor(n * m_pc)
        h = n - l - m
        return lst[:l], lst[l:l+m], lst[l+m:]
    k_ma, m_ma, g_ma = [], [], []
    b = []
    for gl in dat:
        b.append(gl)
        if len(b) >= m_g:
            kln, mid, grt = s_mp(b)
            k_ma.append(kln)
            m_ma.append(mid)
            g_ma.append(grt)
            b = []
    if b:
        kln, mid, grt = s_mp(b)
        k_ma.append(kln)
        m_ma.append(mid)
        g_ma.append(grt)
    als = []
    for m in k_ma + m_ma + g_ma:
        als.extend(m)
    def i_s(lst):
        return all(lst[i] <= lst[i+1] for i in range(len(lst) - 1))
    if not i_s(als):
        for i in range(1, len(als)):
            key = als[i]
            j = i - 1
            while j >= 0 and als[j] > key:
                als[j + 1] = als[j]
                j -= 1
            als[j + 1] = key
    return als
li = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6 ,7, 8, 9 ,12, 34, 45, 675, 78, 234, 768, 23, 678, 12, 234, 67, 90 ,56, 5, 56, 2345, 867, 34, 756, 3214, 56748, 23415, 5674, 3425, 5674, 3245, 4356, 32456, 756, 354, 6453, 4356, 6, 6345, 67, 64573, 46357, 5234 ,67589 ,56789, 5746]
print(t_c_s(li))
