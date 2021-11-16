from pydantic import BaseModel


def prettify(response):
    if isinstance(response, list):
        return __prettify_list(response)
    return __prettify_object(response)


def __prettify_list(response) -> str:
    output = ""
    if isinstance(response, list):
        size = len(response)
        if size:
            response = response[0]
        else:
            return "[ ]"

        output += f"[ {size} * {__prettify_list(response)}"

    else:
        response = __prettify_object(response)
        output += response + " ] "

    return output


def __prettify_object(response) -> str:
    if isinstance(response, BaseModel):
        return response.json()
    return str(response)
