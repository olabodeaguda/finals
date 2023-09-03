from webbrowser import get
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
    file_path = os.path.join(module_dir, 'dl_model.pkl')

    file = open(file_path, 'rb')
    p = pickle.load(file)

    result = p.predict([data])

    x = int(result[0][0])
    return Response({"result": False if x == 1 else True}, status=status.HTTP_200_OK)


def data_transform(payload):
  
    py = {
            'loan_amnt': payload['loan_amnt'],
            'term': payload['term'],
            'int_rate': payload['int_rate'],
            'installment': payload['installment'],
            'grade': payload['grade'],
            'sub_grade': payload['sub_grade'],
            'emp_title': payload['emp_title'],
            'emp_length': payload['emp_length'],
            'home_ownership': payload['home_ownership'],
            'annual_inc': payload['annual_inc'],
            'verification_status': payload['verification_status'],
            'issue_d': payload['issue_d'],
            'loan_status': ['Charged off'],
            'purpose': payload['purpose'],
            'title': payload['title'],
            'dti': payload['dti'],
            'earliest_cr_line': payload['earliest_cr_line'],
            'open_acc': payload['open_acc'],
            'pub_rec': payload['pub_rec'],
            'revol_bal': payload['revol_bal'],
            'revol_util': payload['revol_util'],
            'total_acc': payload['total_acc'],
            'initial_list_status': payload['initial_list_status'],
            'application_type': payload['application_type'],
            'mort_acc': payload['mort_acc'],
            'pub_rec_bankruptcies': payload['pub_rec_bankruptcies'],
            'address': payload['address']
    }
    
    data = pd.DataFrame(data=py)

    X_train = getFitTrainData(data)

    X_test = X_train.copy().iloc[[-1]].reset_index(drop=True)
    
    print(len(X_train.dtypes))
    scaler = MinMaxScaler()
    scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    t = np.array(X_train).astype(np.float32).tolist()


    return t[-1]

def getFitTrainData(newRow):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'lending_club_loan_two.csv')

    data = pd.read_csv(file_path, error_bad_lines=False)
    data = pd.concat([data, newRow])

    data = process_data(data)

    if(len(data) > 78):
        data = data[:78]

    return data

def terms(value):
    value = str(value).replace('months','')
    value = value.strip()

    return int(value)

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

def fill_mort_acc(total_acc, mort_acc, total_acc_avg):
    
    if np.isnan(mort_acc):
        return total_acc_avg[total_acc].round()
    else:
        return mort_acc

def process_data(data):

    data['pub_rec'] = data.pub_rec.apply(pub_rec)
    data['mort_acc'] = data.mort_acc.apply(mort_acc)
    data['pub_rec_bankruptcies'] = data.pub_rec_bankruptcies.apply(pub_rec_bankruptcies)

    data.drop('emp_title', axis=1, inplace=True)
    data.drop('emp_length', axis=1, inplace=True)
    data.drop('title', axis=1, inplace=True)

    total_acc_avg = data.groupby(by='total_acc').mean().mort_acc
    data['mort_acc'] = data.apply(lambda x: fill_mort_acc(x['total_acc'], x['mort_acc'], total_acc_avg), axis=1)
   
    data.dropna(inplace=True)

    data['term'] = data['term'].map(terms)

    data.drop('grade', axis=1, inplace=True)
    dummies = ['sub_grade', 'verification_status', 'purpose', 'initial_list_status',
           'application_type', 'home_ownership']
    data = pd.get_dummies(data, columns=dummies, drop_first=True)


    data['zip_code'] = data.address.apply(lambda x: x[-5:])
    data = pd.get_dummies(data, columns=['zip_code'], drop_first=True)
    data.drop('address', axis=1, inplace=True)
    data.drop('issue_d', axis=1, inplace=True)

    data['earliest_cr_line'] = pd.to_datetime(data['earliest_cr_line'])
    data['earliest_cr_line'] = data.earliest_cr_line.dt.year

    
    data = data.drop('loan_status', axis=1)

    return data