import re

def parse_equation(raw:str):
    eq = re.split(r'[\n,]+', raw)
    return [p.strip() for p in eq if p.strip()]

def extract_variables(eq: str):
    return set(re.findall(r"[a-zA-Z][0-9]*", eq))

def validate_equation_list(equations: list[str]):
    base_vars = extract_variables(equations[0])
    for eq in equations[1:]:
        if extract_variables(eq) != base_vars:
            return False, base_vars, extract_variables(eq), eq
    return True, base_vars, None, None