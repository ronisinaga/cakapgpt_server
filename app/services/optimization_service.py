import numpy as np
from app.helpers.MathHelper import formatMath,coefficient,mathVariable,findNotEqualOp,canonic
from app.helpers.StringHelper import removeSpace,replaceUnicodeMinus
from app.libs.linearprogramming.LinearEquation import GaussianElimination, InverseMatrix, Cramers,GaussSeidel
from app.libs.optimization.Simplex import Simplex
from app.services.welcome_service import linear_message,welcome_message
import uuid
import re
from app.helpers.StreamWriterHelper import StreamCharOfTextWriter,StreamCharWriter,StreamDoneWriter
import time
from app.helpers.equationhelper import validate_equation_list,parse_equation
import asyncio
import numpy as np

sessions = {}
sessionKendala = {}
objective = []

def sessionid(raw):
    #mengecek persamaan, sudah benar atau belum
    sessionid = str(uuid.uuid4())
    print("Session fungsi tujuan:"+sessionid)
    sessions[sessionid] = raw
    return sessionid

def session_kendala(raw):
    #mengecek persamaan, sudah benar atau belum
    sessionid= str(uuid.uuid4())
    sessionKendala[sessionid] = raw
    print("Session fungsi kendala:"+sessionid)
    return sessionid

async def objective_function(sessionid:str):
    if sessionid not in sessions:
        text = f"Persamaan tidak ada"
        StreamCharOfTextWriter(text)
    equations = sessions[sessionid]
    analisis = f"Menganalisis fungsi tujuan yang kamu input..."
    for word in analisis.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    await asyncio.sleep(1)
    #analisis persamaan tujuan
    #cek apakah persamaan valid atau tidak
    arr_msg = []
    arr_msg.append("Baik saya sudah mendapatkan hasil analisisnya. fungsi tujuan kamu adalah")
    arr_msg.append(formatMath(equations))
    arr_msg.append("Sekarang masukkan fungsi kendala kamu:")
    for message in arr_msg:
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    yield "[DONE]"
            
async def get_fungsi_kendala(session):
    if session not in sessions:
        text = f"Persamaan tidak ada"
        StreamCharOfTextWriter(text)
    eqs = sessionKendala[session]
    analisis = f"Menganalisis fungsi kendala yang kamu input..."
    for word in analisis.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    await asyncio.sleep(1)
    #analisis persamaan tujuan
    #cek apakah persamaan valid atau tidak
    arr_msg = []
    arr_msg.append("Baik saya sudah mendapatkan hasil analisisnya. fungsi kendala kamu adalah")
    arr_eq = parse_equation(eqs)
    for eq in arr_eq:
        arr_msg.append(formatMath(eq))
    arr_msg.append("Sekarang masukkan apa yang kamu cari:")
    arr_msg.append("1. Maksimum")
    arr_msg.append("2. Minimum")
    arr_msg.append("Terus metode yang ingin kamu gunakan:")
    arr_msg.append("1. Simpleks sederhana")
    arr_msg.append("2. Simpleks 2 langkah")
    arr_msg.append("3. Simpleks revisi")
    arr_msg.append("Kamu bisa menuliskan dengan cara:")
    arr_msg.append("1, 2")
    arr_msg.append("Tuliskan pilihan kamu")
    for message in arr_msg:
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    yield "[DONE]"

async def optimization_solution(sessionOb,sessionK,maxmin, method):
    ft = sessions[sessionOb]
    fk = sessionKendala[sessionK]
    analisis = f"Melakukan perhitungan {maxmin} menggunakan metode {method}..."
    for word in analisis.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    await asyncio.sleep(1)
    result = f"Baik saya sudah mendapatkan hasil perhitungannya..."
    for word in result.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    arr_ft = ft.split("=")
    A = []
    rhs = []
    mathVariabel = mathVariable(arr_ft[1])
    c = coefficient(arr_ft[1])
    i = 0
    arr_fk = parse_equation(fk)
    for kendala in arr_fk:
        if i < len(arr_fk):
            ne = findNotEqualOp(kendala)
            arr_kendala = kendala.split(ne)
            rhs.append(int(arr_kendala[1].strip()))
            a = coefficient(arr_kendala[0])
            A.append(a)
        i +=1
    kanonik = "Membentuk fungsi kanonik dari fungsi diatas"
    for word in kanonik.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    border = "================================================"
    yield f"{border}"
    yield f" \n"
    canonic_ft = canonic(ft,mathVariabel,destination=True)
    for word in canonic_ft.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"
    canonic_kendala = []
    i = 0
    for kendala in arr_fk:
        if i < len(fk):
            can = canonic(kendala,mathVariabel,i,destination=False)
            canonic_kendala.append(can)  
        i += 1
    for can in canonic_kendala:
        for word in can.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    #yield "[DONE]"
    async for message in Simplex(c,A,rhs,maximize=True):
        yield message


    