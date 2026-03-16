import numpy as np
from app.helpers.MathHelper import formatMath,coefficient,mathVariable
from app.helpers.StringHelper import removeSpace,replaceUnicodeMinus
from app.libs.linearprogramming.LinearEquation import GaussianElimination, InverseMatrix, Cramers,GaussSeidel
from app.services.welcome_service import linear_message,welcome_message
import uuid
import re
from app.helpers.StreamWriterHelper import StreamCharOfTextWriter,StreamCharWriter,StreamDoneWriter
import time
from app.helpers.equationhelper import validate_equation_list,parse_equation
import asyncio
import numpy as np

sessions = {}

def sessionid(raw):
    #mengecek persamaan, sudah benar atau belum
    sessionid = str(uuid.uuid4())
    sessions[sessionid] = raw
    print("Session kamu:"+sessionid)
    return sessionid

async def receive_linear_input(sessionid):
    print("session id:"+sessionid)
    if sessionid not in sessions:
        text = f"Persamaan tidak ada"
        #StreamCharOfTextWriter(text)
        for word in text.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    equations = sessions[sessionid]
    arr_eq = parse_equation(equations)
    analisis = f"Menganalisis {len(arr_eq)} persamaan yang kamu input..."
    for word in analisis.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    await asyncio.sleep(1)
    valid, expected_vars, wrong_vars, wrong_equation = validate_equation_list(arr_eq)
    if not valid:
        #message = f"Persamaan tidak valid. Variabel seharusnya: {list(expected_vars)}. Tetapi {wrong_equation} punya variabel {list(wrong_vars)}"
        message = f"Persamaan tidak valid. Variabel seharusnya {list(expected_vars)}. Tetapi persamaan yang tidak valid adalah {wrong_equation} punya variable {list(wrong_vars)}"
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
        messages = linear_message()
        #StreamCharWriter(messages)
        for message in messages:
            for word in message.split():
                for char in word:
                    yield f"{char}"
                    await asyncio.sleep(0.05)
                yield " "
            yield f" \n"
        yield "[DONE]"
    else:
        arr_msg = []
        arr_msg.append("Baik saya sudah mendapatkan hasil analisisnya. Persamaan kamu adalah")
        arr_eq = parse_equation(equations)
        for eq in arr_eq:
            arr_msg.append(formatMath(eq))
        arr_msg.append("Sekarang pilih metode yang kamu gunakan untuk menyelesaikan persamaan kamu:")
        arr_msg.append("1. Gaussian Elimination")
        arr_msg.append("2. Inverse Matrix")
        arr_msg.append("3. Crammers rule")
        arr_msg.append("Tuliskan angka pilihan kamu:")
        for message in arr_msg:
            for word in message.split():
                for char in word:
                    yield f"{char}"
                    await asyncio.sleep(0.05)
                yield " "
            yield f" \n"
        yield "[DONE]"

def receive_linear_input_old(sessionid):
    wrong = False
    if sessionid not in sessions:
        StreamCharOfTextWriter("Persamaan tidak ada")
        messages = linear_message()
        StreamCharWriter(messages)
        wrong = True
    if not wrong:
        equations = sessions[sessionid]
        analisis = f"Menganalisis {len(equations)} persamaan..."
        StreamCharOfTextWriter(analisis)
        time.sleep(0.5)
        valid, expected_vars, wrong_vars, wrong_equation = validate_equation_list(equations)
        #persamaan tidak valid
        if not valid:
            message = f"Persamaan tidak valid. Variabel seharusnya: {list(expected_vars)}. Tetapi {wrong_equation} punya variabel {list(wrong_vars)}"
            StreamCharOfTextWriter(message)
            messages = linear_message()
            StreamCharWriter(messages)
            wrong = True
        else:
            #persamaan valid
            arr_msg = []
            StreamCharOfTextWriter("Persamaan kamu valid")
            arr_msg.append("Persamaan kamu adalah")
            arr_eq = parse_equation(equations)
            for eq in arr_eq:
                arr_msg.append(formatMath(eq))
            StreamCharWriter(arr_msg)

async def solution(session,method):
    currMethod = ""
    match method:
        case "1":
            currMethod="gaussian elimination"
        case "2":
            currMethod="inverse matrix"
        case "3":
            currMethod="crammers rule"
    equations = sessions[session]
    eqs = parse_equation(equations)
    solutions = linear_solution(eqs,currMethod)
    arr_msg = []
    arr_msg.append(f"Solusi dari persamaan kamu menggunakan method {currMethod} adalah")
    arr_msg.append(solutions["solution"])
    for message in arr_msg:
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    text = "Dalam menemukan solusi diatas, matrix yang digunakan adalah"
    for word in text.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield "\n"

    matrixA = np.array(solutions["matrix"],dtype=float)
    vectorB = np.array(solutions["vector"],dtype=float)
    yield "A ="
    yield "\n"
    if matrixA.ndim == 1:
        matrixA = matrixA.reshape(1, -1)
    width = max(len(f"{x:.3f}") for row in matrixA for x in row)
    for row in matrixA:
        row_str = " ".join(f"{x:>{width}.3f}" for x in row)
        yield f"| {row_str} |"
        yield "\n"

    arr_msg = []
    if vectorB.ndim == 1:
        vectorB = vectorB.reshape(1, -1)
    width = max(len(f"{x:.3f}") for row in vectorB for x in row)
    arr_msg.append("Vektor yang digunakan adalah")
    txt = "b = "
    for row in vectorB:
        txt += "[ " + "  ".join(f"{x:>{width}.3f}" for x in row) + " ]"
    arr_msg.append(txt)
    for message in arr_msg:
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield "\n"
    txt = "Saya sudah berhasil menyelesaikan persamaan linear kamu. Kamu bisa mencoba fitur lainnya."
    for word in txt.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield "\n"
    yield "====================================================================================="
    yield "\n"
    #show menu
    welcome = welcome_message()
    #StreamCharWriter(welcome)
    for message in welcome:
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield "\n"
    yield "[DONE]"

def linear_solution(eqs,method):
    A = []
    b = []
    i = 0
    variable = []
    equations = []
    res = ""
    for eq in eqs:
        equations.append(formatMath(eq))
        #print(formatMath(eq))
        eq_ = removeSpace(eq)
        lhs,rhs = eq_.split("=")
        b.append(int(replaceUnicodeMinus(rhs)))
        coef = coefficient(lhs)
        if i == 0:
            variable = mathVariable(lhs)
        A.append(coef)
        i += 1
    matA = []
    vecB = []
    matA = np.array(A,dtype=float)
    vecB = np.array(b,dtype=float)
    match method.lower():
        case "gaussian elimination":
            solutions = GaussianElimination(matA,vecB)
            # Jika hasil masih numpy → konversi
            if isinstance(solutions, np.ndarray):
                solutions = solutions.tolist()
            for i, sol in enumerate(solutions):
                res += f"{variable[i]} = {round(sol,3)} "
        case "inverse matrix":
            solutions = InverseMatrix(matA,vecB)
            # Jika hasil masih numpy → konversi
            if isinstance(solutions, np.ndarray):
                solutions = solutions.tolist()
            for i, sol in enumerate(solutions):
                res += f"{variable[i]} = {round(sol,3)} "
        case "crammers rule":
            solutions = Cramers(matA,vecB)
            # Jika hasil masih numpy → konversi
            if isinstance(solutions, np.ndarray):
                solutions = solutions.tolist()
            for i, sol in enumerate(solutions):
                res += f"{variable[i]} = {round(sol,3)} "

    return {
        "equations":equations,
        "matrix": matA.tolist(),
        "vector": vecB.tolist(),
        "solution":res.strip()
    }