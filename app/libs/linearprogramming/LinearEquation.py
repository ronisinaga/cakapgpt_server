import numpy as np

def GaussianElimination(A,b):
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1)])
    
    # Eliminasi maju
    for i in range(n):
        # pivot
        pivot = M[i, i]
        M[i] = M[i] / pivot
        for j in range(i+1, n):
            M[j] = M[j] - M[i] * M[j, i]
    
    # Substitusi balik
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = M[i, -1] - np.sum(M[i, i+1:n] * x[i+1:n])
    return x

def InverseMatrix(A,b):
    A_Inv = np.linalg.inv(A)
    X_Inv = np.dot(A_Inv,b)
    return X_Inv

def Cramers(A,b):
    detA = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / detA
    return x

def GaussSeidel(A,b,x0=None,tol=1e-6,max_iter=100):
    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy()
    for iteration in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            sum1 = np.dot(A[i, :i], x_new[:i])
            sum2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - sum1 - sum2) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

def lu_decomposition(A):
    """
    Melakukan faktorisasi LU dari matriks A (tanpa pivoting)
    A: matriks bujur sangkar (numpy array)
    Return: L, U
    """
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    
    for i in range(n):
        # Elemen U
        for k in range(i, n):
            sum_u = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - sum_u
        
        # Elemen L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1  # diagonal L = 1
            else:
                sum_l = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (A[k][i] - sum_l) / U[i][i]
    
    return L, U


def forward_substitution(L, b):
    """Menyelesaikan L*y = b"""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    return y


def backward_substitution(U, y):
    """Menyelesaikan U*x = y"""
    n = len(y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x


def solve_lu(A, b):
    """Menggunakan faktorisasi LU untuk menyelesaikan A*x = b"""
    L, U = lu_decomposition(A)
    y = forward_substitution(L, b)
    x = backward_substitution(U, y)
    return x, L, U