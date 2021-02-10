from django.http import JsonResponse
from rest_framework import response
from rest_framework import status
from rest_framework.views import APIView
import hashlib
import json
import logging
import traceback

from app.models.user import User
from app.serializers.UserGetRequestSerializer import UserGetRequestSerializer
from app.serializers.UserGetResponseSerializer import UserGetResponseSerializer
from app.serializers.UserPostRequestSerializer import UserPostRequestSerializer


class UserManagementHandler(APIView):
    """
    User Management Handler Class
    """

    def __init__(self):
        super(UserManagementHandler, self).__init__()
        self._logger = logging.getLogger()

    # def _process_validation_error_response(self, validation_error):

    def _create_user(self, user_name, password, email, first_name, last_name):
        password = hashlib.sha256(password.encode())
        try:
            User.objects.create(
                user_name=user_name,
                password=password.hexdigest(),
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            return True
        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            return False

    def _get_user(self):
        try:
            data = User.objects.all()
            data = data.values('user_name', 'email', 'first_name', 'last_name')
            return list(data)
        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            return str(err)


    def get(self, request):
        """
        # Get the details about the user if user exists in the system.
        parameters:
            - name: user_name
              type: string
              paramType: query
              required: True
              description: User Name (e.g. ntiwari)

        responseMessage:
            - code:200
              message: Successful

        request_serializer: app.serializers.UserGetRequestSerializer.UserGetRequestSerializer
        response_serializer: app.serializers.UserGetRequestSerializer.UserGetRequestSerializer
        """
        serializer = UserGetRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return JsonResponse({
                'data': {
                    'msg': 'Invalid request'
                }
            }, status=400)
        try:
            user_name = serializer.data.get("user_name")
            resp = User.objects.get(user_name=user_name)
            self._logger.debug("response data = {0}".format(resp))

            if resp :
                return response.Response(UserGetResponseSerializer(resp).data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'data': 'User does not exist' + UserGetResponseSerializer(resp).data
                })
        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            return JsonResponse({
                'data': 'User does not exist exception'
            })

    def post(self, request):
        serializer = UserPostRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({
                'data': {
                    'msg': 'Invalid request body'
                }
            }, status=400)

        user_name = serializer.data.get('user_name') # request_data.get('user_name')
        pasword = serializer.data.get('password')
        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        email = serializer.data.get('email')
        if not (user_name and pasword and first_name and email):
            return JsonResponse({
                'data': {
                    'msg': 'Invalid request body'
                }
            }, status=400)

        response = self._create_user(user_name=user_name,
                                     password=pasword,
                                     email=email,
                                     first_name=first_name,
                                     last_name=last_name)
        if response:
            return JsonResponse({
                'data': {
                    'msg': 'User created'
                }
            }, status=201)
        else:
            return JsonResponse({
                'data': {
                    'msg': 'User alerady exists.'
                }
            }, status=409)
