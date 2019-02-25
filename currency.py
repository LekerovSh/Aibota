import requests
from babel.numbers import format_currency

def currencyapp(c_from, c_to, value):
    ans = ""
    value = value
    from_to = c_from + "_" + c_to
    res = requests.get("https://free.currencyconverterapi.com/api/v6/convert",
                       params={'q': from_to, 'compact': 'ultra'})
    data = res.json()
    result = data[from_to]
    result = result * value
    result = round(result, 3)
    print(result)
    curr_value = format_currency(value, c_from, locale='ru_RU', decimal_quantization = False)
    curr_result = format_currency(result, c_to, locale='ru_RU', decimal_quantization = False)
    ans = curr_value + " = " + curr_result
    return ans


#print(currencyapp("USD", "KZT", 10))  # 10 доллар в тенге

