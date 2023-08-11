from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
import pickle
import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

response_schema_dict = {
    "200": openapi.Response(
        description="Request Body",
        examples={
            "application/json": {
                "loan_amnt": 10000,
                "term": 36,
                "int_rate": 11.44,
                "installment": 329.48,
                "grade": "B",
                "sub_grade": "B4",
                "emp_title": "Marketing",
                "emp_length": 10,
                "home_ownership": "RENT",
                "annual_inc": 117000,
                "verification_status": "Not Verified",
                "issue_d": "Jan-15",
                "purpose": "vacation",
                "title": "vavation",
                "dti": 26.24,
                "earliest_cr_line": "Jan-90",
                "open_acc": 16,
                "pub_rec": 0,
                "revol_bal": 36369,
                "revol_util": 41.8,
                "total_acc": 25,
                "initial_list_status": "w",
                "application_type": "INDIVIDUAL",
                "mort_acc": 0,
                "pub_rec_bankruptcies": 0,
                "address": "0174 Michelle Gateway Mendozaberg, OK 22690"
            }
        }
    ),
    "400": openapi.Response(
        description="custom 205 description",
        examples={
            "application/json": {
                "205_key1": "205_value_1",
                "205_key2": "205_value_2",
            }
        }
    ),
}


@swagger_auto_schema(responses=response_schema_dict, method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "loan_amnt": openapi.Schema(type=openapi.TYPE_NUMBER, description='Loan Amount'),
        "term": openapi.Schema(type=openapi.TYPE_INTEGER, description='The duration of the loan, measure in months'),
        "int_rate": openapi.Schema(type=openapi.TYPE_NUMBER, description='Loan interest rate in percentage'),
        "installment": openapi.Schema(type=openapi.TYPE_NUMBER, description='Monthly repayment schedule'),
        "grade": openapi.Schema(type=openapi.TYPE_STRING, description='LC assigned loan grade'),
        "sub_grade": openapi.Schema(type=openapi.TYPE_STRING, description='LC assigned loan subgrade'),
        "emp_title": openapi.Schema(type=openapi.TYPE_STRING, description='Borrowers employment title'),
        "emp_length": openapi.Schema(type=openapi.TYPE_INTEGER, description='Borrowers employment years in length'),
        "home_ownership": openapi.Schema(type=openapi.TYPE_STRING, description='Borrower home ownership status are RENT, OWN, MORTGAGE, OTHER'),
        "annual_inc": openapi.Schema(type=openapi.TYPE_NUMBER, description='Borrowers annual income.'),
        "verification_status": openapi.Schema(type=openapi.TYPE_STRING, description='Borrow annual income verified.'),
        "issue_d": openapi.Schema(type=openapi.TYPE_STRING, description='The month which the loan was funded'),
        "purpose": openapi.Schema(type=openapi.TYPE_STRING, description='A category provided by the borrower for the loan request.'),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description='The loan title provided by the borrower'),
        "dti": openapi.Schema(type=openapi.TYPE_NUMBER, description='A ratio calculated using the borrower’s total monthly debt payments on the total debt obligations, excluding mortgage and the requested LC loan, divided by the borrower’s self-reported monthly income.'),
        "earliest_cr_line": openapi.Schema(type=openapi.TYPE_STRING, description='The month the borrower\'s earliest reported credit line was opened'),
        "open_acc": openapi.Schema(type=openapi.TYPE_INTEGER, description='The number of open credit lines in the borrower\'s credit file.'),
        "pub_rec": openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of derogatory public records'),
        "revol_bal": openapi.Schema(type=openapi.TYPE_NUMBER, description='Total credit revolving balance'),
        "revol_util": openapi.Schema(type=openapi.TYPE_NUMBER, description='Revolving line utilization rate, or the amount of credit the borrower is using relative to all available revolving credit.'),
        "total_acc": openapi.Schema(type=openapi.TYPE_INTEGER, description='The total number of credit lines currently in the borrower\'s credit file'),
        "initial_list_status": openapi.Schema(type=openapi.TYPE_STRING, description='The initial listing status of the loan. Possible values are – W, F'),
        "application_type": openapi.Schema(type=openapi.TYPE_STRING, description='Indicates whether the loan is an individual application or a joint application with two co-borrowers'),
        "mort_acc": openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of mortgage accounts.'),
        "pub_rec_bankruptcies": openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of public record bankruptcies')
    }
))
@api_view(['POST'])
def preditLoanApplication(request, format=None):
    payload = json.loads(request.body)

    data = data_transform(payload)


    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'dnn_model.pkl')

    file = open(file_path, 'rb')
    p = pickle.load(file)

    print(data)
    result = p.predict(data)
    return Response({"result": str(result)}, status=status.HTTP_200_OK)


def data_transform(payload):

    py = {
        'loan_amnt': [payload['loan_amnt']],
        'term': [payload['term']],
        'int_rate': [payload['int_rate']],
        'installment': [payload['installment']],
        'annual_inc': [payload['annual_inc']],
        'dti': [payload['dti']],
        'earliest_cr_line': [payload['earliest_cr_line']],
        'open_acc': [payload['open_acc']],
        'pub_rec': [payload['pub_rec']],
        'revol_bal': [payload['revol_bal']],
        'revol_util': [payload['revol_util']],
        'total_acc': [payload['total_acc']],
        'mort_acc': [payload['mort_acc']],
        'pub_rec_bankruptcies': [payload['pub_rec_bankruptcies']],
        'sub_grade_A2': [1 if payload['sub_grade'].lower() == 'a2' else 0],
        'sub_grade_A3': [1 if payload['sub_grade'].lower() == 'a3' else 0],
        'sub_grade_A4': [1 if payload['sub_grade'].lower() == 'a4' else 0],
        'sub_grade_A5': [1 if payload['sub_grade'].lower() == 'a5' else 0],
        'sub_grade_B1': [1 if payload['sub_grade'].lower() == 'b1' else 0],
        'sub_grade_B2': [1 if payload['sub_grade'].lower() == 'b2' else 0],
        'sub_grade_B3': [1 if payload['sub_grade'].lower() == 'b3' else 0],
        'sub_grade_B4': [1 if payload['sub_grade'].lower() == 'b4' else 0],
        'sub_grade_B5': [1 if payload['sub_grade'].lower() == 'b5' else 0],
        'sub_grade_C1': [1 if payload['sub_grade'].lower() == 'c1' else 0],
        'sub_grade_C2': [1 if payload['sub_grade'].lower() == 'c2' else 0],
        'sub_grade_C3': [1 if payload['sub_grade'].lower() == 'c3' else 0],
        'sub_grade_C4': [1 if payload['sub_grade'].lower() == 'c4' else 0],
        'sub_grade_C5': [1 if payload['sub_grade'].lower() == 'c5' else 0],
        'sub_grade_D1': [1 if payload['sub_grade'].lower() == 'd1' else 0],
        'sub_grade_D2': [1 if payload['sub_grade'].lower() == 'd2' else 0],
        'sub_grade_D3': [1 if payload['sub_grade'].lower() == 'd3' else 0],
        'sub_grade_D4': [1 if payload['sub_grade'].lower() == 'd4' else 0],
        'sub_grade_D5': [1 if payload['sub_grade'].lower() == 'd5' else 0],
        'sub_grade_E1': [1 if payload['sub_grade'].lower() == 'e1' else 0],
        'sub_grade_E2': [1 if payload['sub_grade'].lower() == 'e2' else 0],
        'sub_grade_E3': [1 if payload['sub_grade'].lower() == 'e3' else 0],
        'sub_grade_E4': [1 if payload['sub_grade'].lower() == 'e4' else 0],
        'sub_grade_E5': [1 if payload['sub_grade'].lower() == 'e5' else 0],
        'sub_grade_F1': [1 if payload['sub_grade'].lower() == 'f1' else 0],
        'sub_grade_F2': [1 if payload['sub_grade'].lower() == 'f2' else 0],
        'sub_grade_F3': [1 if payload['sub_grade'].lower() == 'f3' else 0],
        'sub_grade_F4': [1 if payload['sub_grade'].lower() == 'f4' else 0],
        'sub_grade_F5': [1 if payload['sub_grade'].lower() == 'f5' else 0],
        'sub_grade_G1': [1 if payload['sub_grade'].lower() == 'g1' else 0],
        'sub_grade_G2': [1 if payload['sub_grade'].lower() == 'g2' else 0],
        'sub_grade_G3': [1 if payload['sub_grade'].lower() == 'g3' else 0],
        'sub_grade_G4': [1 if payload['sub_grade'].lower() == 'g4' else 0],
        'sub_grade_G5': [1 if payload['sub_grade'].lower() == 'g5' else 0],
        'verification_status_Verified': [1 if payload['verification_status'].lower() == 'Verified' else 0],
        'verification_status_Source Verified': [1 if payload['verification_status'].lower() != 'Verified' else 0],
        'purpose_credit_card': [1 if payload['purpose'].lower() == 'credit card' else 0],
        'purpose_debt_consolidation': [1 if payload['purpose'].lower() == 'consolidation' else 0],
        'purpose_educational': [1 if payload['purpose'].lower() == 'educational' else 0],
        'purpose_home_improvement': [1 if payload['purpose'].lower() == 'improvement' else 0],
        'purpose_house': [1 if payload['purpose'].lower() == 'house' else 0],
        'purpose_major_purchase': [1 if payload['purpose'].lower() == 'purchase' else 0],
        'purpose_medical': [1 if payload['purpose'].lower() == 'medical' else 0],
        'purpose_moving': [1 if payload['purpose'].lower() == 'moving' else 0],
        'purpose_other': [1 if payload['purpose'].lower() == 'other' else 0],
        'purpose_renewable_energy': [1 if payload['purpose'].lower() == 'renewable_energy' else 0],
        'purpose_small_business': [1 if payload['purpose'].lower() == 'small_business' else 0],
        'purpose_vacation': [1 if payload['purpose'].lower() == 'vacation' else 0],
        'purpose_wedding': [1 if payload['purpose'].lower() == 'wedding' else 0],
        'initial_list_status': [0 if payload['initial_list_status'] == 'f' else 0],
        'application_type_JOINT': [ 1 if payload['application_type'].lower() == 'join' else 0],
        'application_type_MORTGAGE': [1 if payload['application_type'].lower() == 'mortgage' else 0],
        'home_ownership_MORTGAGE': [ 1 if payload['home_ownership'].lower() == 'mortage' else 0],
        'home_ownership_NONE': [ 1 if payload['home_ownership'].lower() == 'none' else 0],
        'home_ownership_OTHER': [ 1 if payload['home_ownership'].lower() == 'other' else 0],
        'home_ownership_OWN': [ 1 if payload['home_ownership'].lower() == 'own' else 0],
        'home_ownership_RENT': [ 1 if payload['home_ownership'].lower() == 'rent' else 0],
        'zip_code_05113': [0],
        'zip_code_11650': [0],
        'zip_code_22690': [0],
        'zip_code_29597': [0],
        'zip_code_30723': [0],
        'zip_code_48052': [0],
        'zip_code_70466': [0],
        'zip_code_86630': [0],
        'zip_code_93700': [0]
    }

    data = pd.DataFrame(data=py)

    data['pub_rec'] = data['pub_rec'].apply(pub_rec)
    data['mort_acc'] = data['mort_acc'].apply(mort_acc)
    data['pub_rec_bankruptcies'] = data['pub_rec_bankruptcies'].apply(pub_rec_bankruptcies)

    for column in data.columns:
        if data[column].isna().sum() != 0:
            missing = data[column].isna().sum()
            portion = (missing / data.shape[0]) * 100
        
    term_values = {'36 months': 36, '60 months': 60}
    data['term'] = data['term'].map(term_values)

    data['earliest_cr_line'] = pd.to_datetime(data['earliest_cr_line'])
    data['earliest_cr_line'] = data['earliest_cr_line'].dt.year

    x = data.iloc[0].to_list()
    print(x)

    scaler = MinMaxScaler()
    resp = scaler.fit_transform(data)

    print(resp)

    return resp


def pub_rec(number):
    if number == 0.0:
        return 0
    else:
        return 1


def mort_acc(number):
    if number == 0.0:
        return 0
    elif number >= 1.0:
        return 1
    else:
        return number


def pub_rec_bankruptcies(number):
    if number == 0.0:
        return 0
    elif number >= 1.0:
        return 1
    else:
        return number
