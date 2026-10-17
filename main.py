from fastapi import FastAPI

app = FastAPI()
def to_decimal(number_str, base):
    superscript_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    result = 0
    steps = []
    power = len(number_str) - 1
    for digit in number_str:
        num = int(digit, 36)
        super_power = str(power).translate(superscript_map)
        steps.append(f"{num} * {base}{super_power}")
        result = result + num * (base ** power)
        power = power - 1
    steps_text = " + ".join(steps) + f" = {result}"
    return result, steps_text
def from_decimal(decimal_number, target_base):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result_digits = []
    division_steps = []
    current = decimal_number
    while current > 0:
        remainder = current % target_base
        quotient = current // target_base
        division_steps.append(f"{current} / {target_base} = {quotient} (остаток {remainder})")
        result_digits.append(chars[remainder])
        current = quotient
    step2_str = "\n".join(division_steps)
    final_result = "".join(reversed(result_digits))
    return final_result, step2_str
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
def convert_number(number: str, base_from: int, base_to: int):
    decimal_value, step1_text = to_decimal(number, base_from)
    final_result, step2_text = from_decimal(decimal_value, base_to)
    full_steps = f"Шаг 1: Перевод в 10-ю систему\n{step1_text}\n\nШаг 2: Деление на {base_to}\n{step2_text}"
    return {
        "original": number,
        "decimal_value": decimal_value,
        "result": final_result,
        "steps": full_steps
    }
