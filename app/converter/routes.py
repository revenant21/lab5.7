# организация обработки запросов

from flask import Blueprint, jsonify, request
from .utils import get_exchange_rate

converter_bp = Blueprint('converter', __name__)


@converter_bp.route('/convert', methods=['GET'])
def convert():
    base = request.args.get('from', 'USD').upper()
    target = request.args.get('to', 'RUB').upper()
    amount = float(request.args.get('amount', 1))

    rate = get_exchange_rate(base, target)

    if rate:
        result = amount * rate
        return jsonify({
            'status': 'success',
            'base': base,
            'target': target,
            'amount': amount,
            'rate': rate,
            'result': round(result, 2)
        })

    return jsonify({'status': 'error', 'message': 'Rate not found'}), 400