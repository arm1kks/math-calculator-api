from fastapi import FastAPI

app = FastAPI()
def to_decimal(number_str, base):
    result = 0
    steps = []
    power = len(number_str) - 1
    for digit in number_str:
        num = int(digit, 36)
        steps.append(f"{num} * {base}^{power}")
        result = result + num * (base ** power)
        power = power - 1
    steps_text = " + ".join(steps)
    return result, steps_text
def from_decimal(decimal_number, target_base):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result_digits = []
    current = decimal_number
    while current > 0:
        remainder = current % target_base
        result_digits.append(chars[remainder])
        current = current // target_base
    final_result = "".join(result_digits[::-1])
    return final_result


@app.get("/convert")
def convert_system(number: str, base_from: int, base_to: int):
    dec_number, steps_text = to_decimal(number, base_from)
    final_answer = from_decimal(dec_number, base_to)
    return {
        "original": number,
        "steps": steps_text,
        "decimal_value": dec_number,
        "result": final_answer
    }