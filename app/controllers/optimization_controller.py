from app.services.optimization_service import sessionid,objective_function,get_fungsi_kendala,session_kendala,optimization_solution

def create_session(req):
    return sessionid(req)

def create_kendala_session(req):
    return session_kendala(req)

def create_objective_function(session:str):
    return objective_function(session)

def fetch_fungsi_kendala(session:str):
    return get_fungsi_kendala(session)

def solution_optimization(sessionOb, sessionK,prompt):
    arr_prompt = prompt.split(",")
    maxmin = ""
    match arr_prompt[0].strip():
        case "1":
            maxmin = "Maximum"
        case "2":
            maxmin = "Minimum"
    method = ""
    match arr_prompt[1].strip():
        case "1":
            method = "Simpleks sederhana"
        case "2":
            method = "Simpleks 2 langkah"
        case "3":
            method = "Simpleks revisi"     

    return optimization_solution(sessionOb,sessionK,maxmin,method)