from math import log10
from decimal import *
from typing import Tuple, Optional

BASIC_INTEREST_RATE = Decimal('0.1')
VERBOSE = True


def credit_decision(age: int, sex: str, income_source: str, last_year_income: float,
                    credit_rating: int, requested_sum, repayment_period, aim: str) -> Tuple[bool, Optional[float]]:
    def _check_inputs():
        """Проверки входных данных.
        Через assert для наглядности, но можно разделить на TypeError и прочие"""
        assert None not in [age, sex, income_source, last_year_income,
                            credit_rating, requested_sum, repayment_period, aim]

        assert type(age) == int
        assert age >= 18

        assert sex in ['F', 'M']

        assert income_source in ['пассивный доход', 'наёмный работник', 'собственный бизнес', 'безработный']

        assert type(last_year_income) in (float, int)

        assert credit_rating in [-2, -1, 0, 1, 2]

        assert type(requested_sum) in (float, int)
        assert Decimal('0.1') <= requested_sum <= 10

        assert type(repayment_period) in (float, int)
        assert 1 <= repayment_period <= 20

        assert aim in ['ипотека', 'развитие бизнеса', 'автокредит', 'потребительский']

    def _get_pension_age():
        """Возвращает пенсионный возраст для клиента.
        Для определения точного пенсионного возраста на момент выплаты кредита нужно знать хотя бы полугодие рождения
        https://pfr.gov.ru/grazhdanam/zakon/"""

        pension_ages = {'F': 55, 'M': 60}
        return pension_ages[sex]

    def _get_interest_rate_modifier():
        """Возвращает модификатор базовой процентной ставки"""

        interest_rate_modifier = Decimal('0')

        if aim == 'ипотека':
            interest_rate_modifier -= Decimal('0.02')
        elif aim == 'развитие бизнеса':
            interest_rate_modifier -= Decimal('0.005')
        elif aim == 'потребительский':
            interest_rate_modifier += Decimal('0.015')

        if credit_rating == -1:
            interest_rate_modifier += Decimal('0.015')
        elif credit_rating == 0:
            interest_rate_modifier -= Decimal('0')  # для прозрачности
        elif credit_rating == 1:
            interest_rate_modifier -= Decimal('0.0025')
        elif credit_rating == 2:
            interest_rate_modifier -= Decimal('0.0075')

        sum_interest_modifier = Decimal(str(-log10(requested_sum))) * Decimal('0.01')
        interest_rate_modifier += sum_interest_modifier

        if income_source == 'пассивный доход':
            interest_rate_modifier += Decimal('0.005')
        elif income_source == 'наёмный работник':
            interest_rate_modifier -= Decimal('0.0025')
        elif income_source == 'собственный бизнес':
            interest_rate_modifier += Decimal('0.0025')

        return interest_rate_modifier

    def _get_credit_sum():
        """Возвращает разрешенную сумму кредита"""

        available_credit_sum = requested_sum

        if income_source == 'пассивный доход':
            available_credit_sum = available_credit_sum if available_credit_sum <= 1 else 1
        elif income_source == 'наёмный работник':
            available_credit_sum = available_credit_sum if available_credit_sum <= 5 else 5
        elif income_source == 'собственный бизнес':
            available_credit_sum = available_credit_sum if available_credit_sum <= 10 else 10

        if credit_rating == -1:
            available_credit_sum = available_credit_sum if available_credit_sum <= 1 else 1
        elif credit_rating == 0:
            available_credit_sum = available_credit_sum if available_credit_sum <= 5 else 5
        elif credit_rating >= 1:
            available_credit_sum = available_credit_sum if available_credit_sum <= 10 else 10

        available_credit_sum = Decimal(str(available_credit_sum))

        return available_credit_sum

    def get_annual_payment(allowed_credit_sum, interest_rate, modifier):
        """Возвращает годовой платёж по кредиту"""

        return allowed_credit_sum * (1 + repayment_period * (interest_rate + modifier)) / repayment_period

    def get_verdict(allowed_credit_sum):
        """Возвращает решение о выдаче кредита"""

        credit_denial_reasons = {
            'Запрошенная сумма больше возможной к выдаче':
                requested_sum > allowed_credit_sum,
            'Возраст на момент окончания кредита превышает пенсионный':
                age + repayment_period > _get_pension_age(),
            'Коэффициент запрошенной суммы на срок погашения больше трети дохода за последний год':
                requested_sum / repayment_period > last_year_income / 3,
            'Недостаточный кредитный рейтинг':
                credit_rating == -2,
            'Нет источника постоянного дохода':
                income_source == 'безработный',
            'Ежегодный платёж больше половины годового дохода':
                result_annual_payment > last_year_income / 2
        }

        if VERBOSE:
            current_denial_reasons = [reason for reason in credit_denial_reasons.keys()
                                      if credit_denial_reasons[reason]]
            return (False, current_denial_reasons) if current_denial_reasons else True

        return False if [reason for reason in credit_denial_reasons.keys()
                         if credit_denial_reasons[reason]] else True

    _check_inputs()
    requested_sum, repayment_period = Decimal(str(requested_sum)), Decimal(str(repayment_period))
    credit_sum = _get_credit_sum()
    current_interest_rate_modifier = _get_interest_rate_modifier()
    result_annual_payment = get_annual_payment(credit_sum, BASIC_INTEREST_RATE, current_interest_rate_modifier)
    result_annual_payment = float(result_annual_payment.quantize(Decimal(
        '1.00000000')))
    result_verdict = get_verdict(credit_sum)

    if VERBOSE:

        if result_verdict is not True:
            result_verdict, reasons = result_verdict
            result = f'Кредит не выдаётся: {reasons}'

        else:
            result = f'Кредит: выдаётся, годовой платёж: {result_annual_payment * 1000000} р.'

        requester_data = f'''
Возраст: {age},
Пол: {sex},
Источник дохода: {income_source},
Доход за прошлый год (млн. р.): {last_year_income},
Кредитный рейтинг: {credit_rating},
Запрошенная сумма (млн. р.): {requested_sum},
Срок погашения: {repayment_period} {'г.' if repayment_period < 5 else 'лет'},
Цель: {aim}'''

        print(requester_data, result, sep='\n')

    return result_verdict, result_annual_payment if result_verdict else None


if __name__ == '__main__':
    print(credit_decision(age=20, sex='M', income_source='наёмный работник', last_year_income=2.2,
                          credit_rating=0, requested_sum=0.1, repayment_period=1, aim='ипотека'))
