def cuando_detiene(a, b, h):
    f_a, f_s = [0] * 8
    filas = []

    # Fila inicial
    f_a[0] = 0
    f_a[1] = a
    f_a[2] = f_a[1] * b
    f_a[3] = (f_a[1] + (h / 2) * f_a[2]) * b
    f_a[4] = (f_a[1] + (h / 2) * f_a[3]) * b
    f_a[5] = (f_a[1] + h * f_a[4]) * b
    f_a[6] = f_a[0] + h
    f_a[7] = f_a[1] + (h / 6) * (f_a[2] + 2 * f_a[3] + 2 * f_a[4] + f_a[5])

    filas.append(f_a)

    while f_a[7] >= 3 * a:
        f_s[0] = f_a[6]
        f_s[1] = f_a[7]
        f_s[2] = f_s[1] * b
        f_s[3] = (f_s[1] + (h / 2) * f_s[2]) * b
        f_s[4] = (f_s[1] + (h / 2) * f_s[3]) * b
        f_s[5] = (f_s[1] + h * f_s[4]) * b
        f_s[6] = f_s[0] + h
        f_s[7] = f_s[1] + (h / 6) * (f_s[2] + 2 * f_s[3] + 2 * f_s[4] + f_s[5])

        filas.append(f_s)
        f_a = f_s

    return filas, f_a[7]