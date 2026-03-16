import numpy as np
import pandas as pd

from app.helpers.MathHelper import subscript
import asyncio

async def Simplex(c, A,b,maximize=True):
    """
    c : koefisien fungsi tujuan (mis. [3, 2])
    A : matriks kendala (mis. [[1,1],[1,2]])
    b : sisi kanan kendala (mis. [4,6])
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    if not maximize:
        A = -A
        b = -b
    c = np.array(c, dtype=float)

    m, n = A.shape
    print(f"m={m}")
    print(f"n={n}")

    # Tambah variabel slack
    I = np.eye(m)
    tableau = np.hstack([A, I, b.reshape(-1,1)])

    # Jika minimisasi → ubah tanda fungsi tujuan
    if maximize:
        z_row = np.hstack([-c, np.zeros(m+1)])
    else:
        z_row = np.hstack([c, np.zeros(m+1)])
    # Tambahkan baris Z
    tableau = np.vstack([tableau, z_row])

    # Basis awal: variabel slack
    basis = [subscript('s' + str(i)) for i in range(m)]
    variables = [subscript('x' + str(i+1)) for i in range(n)] + basis

    #print(f"\nMembentuk Tableau")
    tableustr = "Membentuk Tableau"
    for word in tableustr.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    yield "==========================================================\n"
    df = pd.DataFrame(tableau, columns=variables + ['rhs'])
    df.index = basis + ['Z']
    tableu = str(df.round(3))
    yield tableu+"\n"
    #yield f" \n"
    print(str(df.round(3)))

    iteration = 1
    while True:
        #print(f"\n===== Iterasi {iteration} =====")
        iterasi = f"===== Iterasi {iteration} ====="
        for word in iterasi.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        df = pd.DataFrame(tableau, columns=variables + ['rhs'])
        df.index = basis + ['Z']
        dfstr = str(df.round(3))
        print(str(df.round(3)))
        yield dfstr+"\n"

        # Cek optimalitas (semua koefisien Z >= 0 untuk maksimisasi atau Z <= 0  untuk minimisasi)
        z_row = tableau[-1, :-1]
        #cek optimalisasi
        if maximize:
            optimal = all(z_row >= 0)
        else:
            optimal = all(z_row <= 0)
        if optimal:
            optimal = "✅ Solusi optimum/minium ditemukan."
            for word in optimal.split():
                for char in word:
                    yield f"{char}"
                    await asyncio.sleep(0.05)
                yield " "
            yield f" \n"
            #print("\n✅ Solusi optimum/minium ditemukan.")
            break

        # Tentukan kolom basis (kolom dengan nilai negatif terkecil di baris Z jika maksimum dan nilai terbesar di baris Z jika minimum)
        #pivot_col = np.argmin(z_row)
        pivot_col = np.argmin(z_row) if maximize else np.argmax(z_row)
        entering_var = variables[pivot_col]
        kolom_basis = "➡️ Kolom Basis: "+entering_var
        for word in kolom_basis.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        print("\n➡️ Kolom Basis: ",entering_var)

        # Tentukan baris basis (rasio terkecil positif)
        ratios = []
        for i in range(m):
            if tableau[i, pivot_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)
        pivot_row = np.argmin(ratios)

        leaving_var = basis[pivot_row]
        baris_basis = f"➡️ Baris basis: {leaving_var}"
        for word in baris_basis.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        print(f"➡️ Baris basis: {leaving_var}")

        # Pivot
        pivot_val = tableau[pivot_row, pivot_col]
        pivot = f"➡️ Nilai pivot: {pivot_val:.3f}"
        for word in pivot.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        print(f"➡️ Nilai pivot: {pivot_val:.3f}")
        tableau[pivot_row, :] = tableau[pivot_row, :] / pivot_val

        for i in range(m+1):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

        # Update basis
        basis[pivot_row] = entering_var
        iteration += 1

    # Cetak hasil akhir
    if maximize:
        soloptimum = "=== Solusi Optimum ==="
        for word in soloptimum.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        #print("\n=== Solusi Optimum ===")
    else:
        solminimum = "=== Solusi Minimum ==="
        for word in solminimum.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        #print("\n=== Solusi Minimum ===")
    df = pd.DataFrame(tableau, columns=variables + ['rhs'])
    df.index = basis + ['Z']
    dfstr = str(df.round(3))
    yield dfstr+"\n"
    print(df.round(3))

    Z_opt = tableau[-1, -1]
    if not maximize:
        Z_opt = -Z_opt  # balik tanda untuk minimisasi

    # Nilai solusi optimal
    sol = {v: 0 for v in variables}
    for i, b_name in enumerate(basis):
        sol[b_name] = tableau[i, -1]

    if maximize:
        maxs = "Nilai variabel untuk mendapatkan hasil maksimum adalah:"
        for word in maxs.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        #print("\nNilai variabel untuk mendapatkan hasil maksimum adalah:")
    else:
        mins = "Nilai variabel untuk mendapatkan hasil minimum adalah:"
        for word in mins.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        #print("\nNilai variabel untuk mendapatkan hasil minimum adalah:")
    for i in range(n):
        var = f"{variables[i]} = {sol[variables[i]]:.3f}"
        for word in var.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        #print(f"{variables[i]} = {sol[variables[i]]:.3f}")
    z = f"{'Z maksimum' if maximize else 'Z minimum'} = {Z_opt:.3f}"
    for word in z.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    yield "[DONE]"
    #print(f"\n{'Z maksimum' if maximize else 'Z minimum'} = {Z_opt:.3f}")