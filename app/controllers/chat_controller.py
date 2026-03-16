from typing import List
from app.schemas.text_schema import TextResponse
from app.services.welcome_service import welcome_message,wrong_choice_message,linear_message,optimization_message
from app.schemas.choice_schema import ChoiceResponse

def welcome() -> TextResponse:
    return TextResponse(
        processed=welcome_message()
    )

def choice(choice:str) -> ChoiceResponse:
    message = []
    stat = False
    try:
        number = int(choice)
        match number:
            case 1:
                message = linear_message()
                stat = True
            case 2:
                message = optimization_message()
                stat = True
            case 3:
                message = linear_message()
                stat = True
            case 4:
                message = optimization_message()
                stat = True
            case 5:
                message = optimization_message()
                stat = True
    except:
        stat = False
        message = wrong_choice_message()
    return ChoiceResponse (
        status=stat,
        message=message
    )