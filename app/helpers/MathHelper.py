def subscript(text):
    subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return text.translate(subscript_map)

def superscript(text):
    superscript_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return text.translate(superscript_map)

def formatSign(teks):
    mapping = {
        "<=": "≤",
        ">=": "≥",
        "!=": "≠",
        #"!=": "<>",
        "==": "＝",   # opsional
        bytes([243]).decode('cp1252'): "≤",  # ANSI 243 (≤)
        bytes([242]).decode('cp1252'): "≥",  # ANSI 242 (≥)
        bytes([185]).decode('cp1252'): "±",  # ANSI 185 (±)
        bytes([241]).decode('cp1252'): "≠",  # ANSI 241 (≠)
    }
    for lama, baru in mapping.items():
        teks = teks.replace(lama, baru)
    return teks

def formatMath(text):
    subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    superscript_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    result = ""
    i = 0
    foundX = False
    while i < len(text):
        # Jika menemukan tanda ^
        if text[i] == "^":
            i += 1
            num = ""
            # Ambil semua digit setelah tanda ^
            while i < len(text) and text[i].isdigit():
                num += text[i]
                i += 1
            # Ubah semua digit itu ke superscript
            result += num.translate(superscript_map)
        else:
            # Jika karakter angka dan tidak setelah ^
            if text[i].isdigit():
                if not foundX:
                    result += text[i]
                    i += 1
                else:
                    num = ""
                    while i < len(text) and text[i].isdigit():
                        num += text[i]
                        i += 1
                    result += num.translate(subscript_map)
                    foundX = False
            else:
                if (text[i].lower() == "x"):
                    foundX = True
                result += text[i]
                i += 1
    return result

def coefficient(eq):
    arr_eq = eq.split()
    coef = []
    #inisiasi array dengan angka 0
    lenVar = 0
    for arr in arr_eq:
        i =0
        foundX = False
        while i < len(arr) and not foundX:
            if arr[i].lower() == 'x':
                lenVar += 1
                foundX = True
            i += 1
    i=0
    while i < lenVar:
        coef.append(0)
        i += 1
    findMin = False
    for arr in arr_eq:
        i=0
        foundX = False
        str = ""
        idx = ""
        while i < len(arr) and not foundX:
            if arr[i].lower() == 'x':
                foundX = True
                i += 1
                while i < len(arr):
                    idx += arr[i]
                    i += 1
            else:
                if arr[i].isdigit():
                    str += arr[i]
                else:
                    if arr[i] == "-":
                        findMin = True
                i += 1
        if str != "":
            num = int(str)
            if findMin:
                num = num*-1
                findMin = False
            coef[int(idx)-1] = num
        else:
            if foundX:
                if findMin:
                    #coef.append(-1)
                    coef[int(idx)-1] = -1
                    findMin = False
                else:
                    #coef.append(1)
                    coef[int(idx)-1] = 1
    return coef

def mathVariable(eq):
    arr_eq = eq.split()
    variable = []
    for arr in arr_eq:
        i=0
        foundX = False
        str = ""
        while i < len(arr):
            if arr[i].lower() == 'x':
                foundX = True
                str += arr[i]
            else:
                if foundX:
                    str += arr[i]
            i += 1
        if str != '':
            str = subscript(str)
            variable.append(str)
    return variable

def findNotEqualOp(lne):
    ne = ['<','>','<=','>=']
    cne = ''
    found = False
    i = 0
    temp = ""
    while i < len(lne) and not found:
        if lne[i] in ne:
            temp = lne[i]
            i+= 1
            if lne[i] == "=":
                temp += lne[i]
            found = True
            cne = temp
        i += 1
    return cne

def canonic(eq,mathVariable,index=1,destination=True):
    if destination is True:
        arr_eq = eq.split("=")
        coef = coefficient(arr_eq[1])
        #bentuk variabel kanonik
        can = eq[0]
        i = 0
        for c in coef:
            if int(c) > 0:
                if abs(int(c)) > 1:
                    can += " - "+str(c)+mathVariable[i]
                else:
                    can += " - "+mathVariable[i]
            else:
                can += " + "+str(c)+mathVariable[i]
            i += 1
        can += " = 0"
    else:
        ne = findNotEqualOp(eq)
        arr_eq = eq.split(ne)
        ne = formatSign(ne)
        rhs = arr_eq[1].strip()
        coef = coefficient(arr_eq[0])
        #bentuk variabel kanonik
        can = ""
        i = 0
        for c in coef:
            if c < 0:
                if abs(c) > 1:
                    if can == "":
                        can += " -"+str(abs(c))+mathVariable[i]
                    else:
                        can += " - "+str(abs(c))+mathVariable[i]
                else:
                    if can == "":
                        can += " -"+mathVariable[i]
                    else:
                        can += " - "+mathVariable[i]
            else:
                if c > 1:
                    if can == "":
                        can += str(c)+mathVariable[i]
                    else:
                        can += " + "+str(c)+mathVariable[i]
                else:
                    if can == "":
                        can += mathVariable[i]
                    else:
                        can += " + "+mathVariable[i]
            i += 1
        if (ne == "≤" or ne == "<"):
            can += " + "+subscript("s"+str(index))
        else:
            can += " - "+subscript("e"+str(index))
        if int(rhs) > 0:
            can += " - "+str(abs(int(rhs)))
        else:
            can += " + "+rhs
        can += " = 0"
    return can