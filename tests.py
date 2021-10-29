import unittest
from copy import deepcopy

from main import credit_decision

BASE_OK_SCENARIO = {'age': 20, 'sex': 'M', 'income_source': 'наёмный работник', 'last_year_income': 2,
                    'credit_rating': 0, 'requested_sum': 0.1, 'repayment_period': 1, 'aim': 'ипотека'}


class CreditDecisionTestCases(unittest.TestCase):

    def setUp(self):
        self.test_data = deepcopy(BASE_OK_SCENARIO)

    def test_pos_approved(self):
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_age_over_pension_age(self):
        self.test_data['age'] = 61
        self.assertEqual(credit_decision(**self.test_data), (False, None))

        self.test_data['age'] = 56
        self.test_data['sex'] = 'F'
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_age_will_be_over_pension_age(self):
        self.test_data['age'] = 60
        self.assertEqual(credit_decision(**self.test_data), (False, None))

        self.test_data['age'] = 55
        self.test_data['sex'] = 'F'
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_age_ok_max(self):
        self.test_data['age'] = 59
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

        self.test_data['age'] = 54
        self.test_data['sex'] = 'F'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_not_allowed_if_requested_sum_by_years_more_than_third_of_yearly_income(self):
        self.test_data['last_year_income'] = 2
        self.test_data['requested_sum'] = 3
        self.test_data['repayment_period'] = 4
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_not_allowed_by_credit_rating(self):
        self.test_data['credit_rating'] = -2
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_not_allowed_income_source_no_source(self):
        self.test_data['income_source'] = 'безработный'
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_not_allowed_annual_payment_greater_than_half_of_income(self):
        self.test_data['last_year_income'] = 1
        self.test_data['requested_sum'] = 5
        self.test_data['repayment_period'] = 19
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_not_allowed_sum_lesser_than_requested_passive_income(self):
        self.test_data['income_source'] = 'пассивный доход'
        self.test_data['requested_sum'] = 2
        self.test_data['repayment_period'] = 20
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_allowed_sum_max_requested_passive_income(self):
        self.test_data['income_source'] = 'пассивный доход'
        self.test_data['requested_sum'] = 1
        self.test_data['repayment_period'] = 20
        self.assertEqual(credit_decision(**self.test_data), (True, 0.135))

    def test_not_allowed_sum_lesser_than_requested_hired(self):
        self.test_data['income_source'] = 'наёмный работник'
        self.test_data['requested_sum'] = 6
        self.test_data['repayment_period'] = 20
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_allowed_sum_max_requested_hired(self):
        self.test_data['income_source'] = 'наёмный работник'
        self.test_data['requested_sum'] = 5
        self.test_data['repayment_period'] = 10
        self.assertEqual(credit_decision(**self.test_data), (True, 0.8525515))

    def test_allowed_sum_max_requested_own_business_and_credit_rating_1_or_more(self):
        self.test_data['income_source'] = 'собственный бизнес'
        self.test_data['requested_sum'] = 10
        self.test_data['repayment_period'] = 16
        self.test_data['last_year_income'] = 4
        self.test_data['credit_rating'] = 1
        self.assertEqual(credit_decision(**self.test_data), (True, 1.325))

    def test_not_allowed_sum_lesser_than_requested_credit_rating_m1(self):
        self.test_data['credit_rating'] = -1
        self.test_data['requested_sum'] = 2
        self.test_data['repayment_period'] = 5
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_allowed_sum_max_requested_credit_rating_m1(self):
        self.test_data['credit_rating'] = -1
        self.test_data['requested_sum'] = 1
        self.test_data['repayment_period'] = 5
        self.assertEqual(credit_decision(**self.test_data), (True, 0.2925))

    def test_not_allowed_sum_lesser_than_requested_credit_rating_0(self):
        self.test_data['credit_rating'] = 0
        self.test_data['requested_sum'] = 6
        self.test_data['repayment_period'] = 10
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_allowed_sum_max_requested_credit_rating_0(self):
        self.test_data['credit_rating'] = 0
        self.test_data['requested_sum'] = 5
        self.test_data['repayment_period'] = 10
        self.assertEqual(credit_decision(**self.test_data), (True, 0.8525515))


class CreditSumTestCases(unittest.TestCase):

    def setUp(self):
        self.test_data = deepcopy(BASE_OK_SCENARIO)

    def test_credit_rating_m1(self):
        self.test_data['credit_rating'] = -1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.11025))

    def test_credit_rating_0(self):
        self.test_data['credit_rating'] = 0
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_credit_rating_1(self):
        self.test_data['credit_rating'] = 1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.1085))

    def test_credit_rating_2(self):
        self.test_data['credit_rating'] = 2
        self.assertEqual(credit_decision(**self.test_data), (True, 0.108))

    def test_income_source_passive(self):
        self.test_data['income_source'] = 'пассивный доход'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.1095))

    def test_income_source_hired(self):
        self.test_data['income_source'] = 'наёмный работник'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_income_source_own_business(self):
        self.test_data['income_source'] = 'собственный бизнес'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10925))

    def test_aim_business_development(self):
        self.test_data['aim'] = 'развитие бизнеса'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.11025))

    def test_aim_car(self):
        self.test_data['aim'] = 'автокредит'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.11075))

    def test_aim_consumer_loan(self):
        self.test_data['aim'] = 'потребительский'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.11225))

    def test_amount_modifier_p1(self):
        self.test_data['requested_sum'] = 0.1
        self.test_data['repayment_period'] = 20
        self.test_data['income_source'] = 'собственный бизнес'
        self.test_data['last_year_income'] = 4
        self.test_data['credit_rating'] = 1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.014))

    def test_amount_modifier_0(self):
        self.test_data['requested_sum'] = 1
        self.test_data['repayment_period'] = 20
        self.test_data['income_source'] = 'собственный бизнес'
        self.test_data['last_year_income'] = 4
        self.test_data['credit_rating'] = 1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.13))

    def test_amount_modifier_m1(self):
        self.test_data['requested_sum'] = 10
        self.test_data['repayment_period'] = 20
        self.test_data['income_source'] = 'собственный бизнес'
        self.test_data['last_year_income'] = 4
        self.test_data['credit_rating'] = 1
        self.assertEqual(credit_decision(**self.test_data), (True, 1.2))


class InputDataTestCases(unittest.TestCase):

    def setUp(self):
        self.test_data = deepcopy(BASE_OK_SCENARIO)

    def test_age_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['age'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['age'] = 0
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['age'] = 11.11
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['age'] = '18'
            credit_decision(**self.test_data)

        self.test_data['age'] = 18
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_sex_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['sex'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['sex'] = 0
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['sex'] = 'X'
            credit_decision(**self.test_data)

        self.test_data['sex'] = 'F'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

        self.test_data['sex'] = 'M'
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_income_source_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['income_source'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['income_source'] = 1
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['income_source'] = 'другое'
            credit_decision(**self.test_data)

    def test_last_year_income_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['last_year_income'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['last_year_income'] = '10'
            credit_decision(**self.test_data)

        self.test_data['last_year_income'] = 1.1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

        self.test_data['last_year_income'] = 12
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

    def test_credit_rating_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['credit_rating'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['credit_rating'] = -3
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['credit_rating'] = 3
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['credit_rating'] = 1.5
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['credit_rating'] = '2'
            credit_decision(**self.test_data)

    def test_requested_sum_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['requested_sum'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['requested_sum'] = -1
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['requested_sum'] = 0
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['requested_sum'] = 11
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['requested_sum'] = '5'
            credit_decision(**self.test_data)

        self.test_data['requested_sum'] = 0.1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

        self.test_data['requested_sum'] = 10
        self.assertEqual(credit_decision(**self.test_data), (False, None))

    def test_repayment_period_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['repayment_period'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['repayment_period'] = -1
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['repayment_period'] = 0.1
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['repayment_period'] = 21
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['repayment_period'] = '10'
            credit_decision(**self.test_data)

        self.test_data['repayment_period'] = 1
        self.assertEqual(credit_decision(**self.test_data), (True, 0.10875))

        self.test_data['repayment_period'] = 20
        self.assertEqual(credit_decision(**self.test_data), (True, 0.01375))

    def test_aim_inputs(self):
        with self.assertRaises(AssertionError):
            self.test_data['aim'] = None
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['aim'] = 1
            credit_decision(**self.test_data)

        with self.assertRaises(AssertionError):
            self.test_data['aim'] = 'просто так'
            credit_decision(**self.test_data)


if __name__ == '__main__':
    unittest.main()
