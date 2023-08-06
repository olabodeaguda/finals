from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response



response_schema_dict = {
    "200": openapi.Response(
        description="Request Body",
        examples={
            "application/json": {              
                "loan_amnt" : 10000,
                "term" : 36,
                "int_rate" : 11.44,
                "installment" :329.48,
                "grade" : "B",
                "sub_grade" : "B4",
                "emp_title" : "Marketing",
                "emp_length" : 10,
                "home_ownership" : "RENT",
                "annual_inc" : 117000,
                "verification_status" : "Not Verified",
                "issue_d" : "Jan-15",
                "purpose": "vacation",
                "title" : "vavation",
                "dti" : 26.24,
                "earliest_cr_line" : "Jan-90",
                "open_acc" : 16,
                "pub_rec":0,
                "revol_bal" : 36369,
                "revol_util" : 41.8,
                "total_acc" : 25,
                "initial_list_status" : "w",
                "application_type" : "INDIVIDUAL",
                "mort_acc" : 0,
                "pub_rec_bankruptcies" : 0,
                "address" : "0174 Michelle Gateway Mendozaberg, OK 22690"
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
        "loan_amnt" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "term" : openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "int_rate" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "installment" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "grade" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "sub_grade" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "emp_title" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "emp_length" : openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "home_ownership" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "annual_inc" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "verification_status" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "issue_d" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "purpose": openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "title" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "dti" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "earliest_cr_line" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "open_acc" : openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "pub_rec":openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "revol_bal" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "revol_util" : openapi.Schema(type=openapi.TYPE_NUMBER, description='?'),
        "total_acc" : openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "initial_list_status" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "application_type" : openapi.Schema(type=openapi.TYPE_STRING, description='?'),
        "mort_acc" : openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "pub_rec_bankruptcies" : openapi.Schema(type=openapi.TYPE_INTEGER, description='?'),
        "address" : openapi.Schema(type=openapi.TYPE_STRING, description='?')
    }
))
@api_view(['POST'])
def preditLoanApplication(request, format=None):
     return Response({"result": "aguda"}, status = status.HTTP_201_CREATED)