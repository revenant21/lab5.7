# организация обработки запросов

from flask import Blueprint, jsonify, request, render_template
from .utils import get_exchange_rate

converter_bp = Blueprint('converter', __name__)

@converter_bp.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    base = 'USD'
    target = 'RUB'
    amount = None

    if request.method == 'POST':
        try:
            base = request.form.get('base').upper()
            target = request.form.get('target').upper()
            amount = float(request.form.get('amount'))

            rate = get_exchange_rate(base, target)
            if rate:
                result = round(amount * rate, 2)
            else:
                error = "Не удалось получить курс валют."
        except (ValueError, TypeError):
            error = "Введите корректное число."

    return render_template('index.html',
                           result=result,
                           error=error,
                           base=base,
                           target=target,
                           amount=amount)