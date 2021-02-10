from rest_framework import response
from rest_framework import status
import logging
import traceback

from django.http import JsonResponse
from rest_framework.views import APIView

from app.models import Follow
from app.models import User
from app.serializers import UserGetResponseSerializer

class FollowActionHandler(APIView):

    """
    Following Action Handler Class
    """

    def __init__(self):
        super(FollowActionHandler, self).__init__()
        self._logger = logging.getLogger()
        self._response_data = {
            "status": 0,
            "message": ""
        }

    def _follow(self, user, following_user):
        '''Creates a new Follow object.'''
        try:
            Follow.objects.get(follower=user, following=following_user)
            return False
        except Exception as err:
            self._logger.debug("Exception = {0}".format(err))
            pass
        try:
            follower_user_obj = User.objects.get(user_name=user)
            following_user_obj = User.objects.get(user_name=following_user)
            Follow.objects.create(follower=follower_user_obj, following=following_user_obj)

            return True
        except Exception as err:
            self._logger.debug("Exception = {0}".format(err))
            pass

    def _unfollow(self, user, following_user):
        '''Deletes the follow relatioship object.'''
        try:
            fol = Follow.objects.get(follower=user, following=following_user)
            fol.delete()
            return True
        except Exception as err:
            self._logger.debug("Exception = {0}".format(err))
            return False

    def _validate_user(self, user_name):
        try:
            resp = User.objects.get(user_name=user_name)
            self._logger.debug("response data = {0}".format(resp))
            return True
        except Exception as err:
            self._logger.debug("response data = {0}".format(err))
            return False

    def get(self, request):
        try:
            user_name = request.data.get("user_name")
            user_obj = User.objects.get(user_name=user_name)
            resp = Follow.objects.get(following=user_obj)
            self._logger.debug("response data = {0}".format(resp))

            if resp :
                return response.Response(UserGetResponseSerializer(resp).data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'data': 'Follower does not exist'
                })
        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            return JsonResponse({
                'data': 'User does not exist exception'
            })

    def post(self, request):
        try:
            user_name = request.data.get("user_name")
            follow_user = request.data.get("follow_user")
            if not (user_name and follow_user):
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request"
                return JsonResponse(self._response_data)

            if user_name == follow_user:
                self._response_data["status"] = 400
                self._response_data["message"] = "Can't follow self"
                return JsonResponse(self._response_data)

            usr_exists = self._validate_user(user_name)
            following_usr_exists = self._validate_user(follow_user)

            if not (usr_exists and following_usr_exists):
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid username or follow_user."
                return JsonResponse(self._response_data)

            response = self._follow(user_name, follow_user)

            if response:
                self._response_data["status"] = 201
                self._response_data["message"] = "Followed user successfully."
                return JsonResponse(self._response_data)
            else:
                self._response_data["status"] = 409
                self._response_data["message"] = "The requested user is already followed."
                return JsonResponse(self._response_data)

        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            self._response_data["status"] = 500
            self._response_data["message"] = "Internal Server Error during following user call"
            return JsonResponse(self._response_data)

    def delete(self, request):
        try:
            user_name = request.data.get("user_name")
            follow_user = request.data.get("follow_user")
            if not (user_name and follow_user):
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request"
                return JsonResponse(self._response_data)

            if user_name == follow_user:
                self._response_data["status"] = 400
                self._response_data["message"] = "Can't follow self"
                return JsonResponse(self._response_data)

            usr_exists = self._validate_user(user_name)
            following_usr_exists = self._validate_user(follow_user)

            if not (usr_exists and following_usr_exists):
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid username or follow_user."
                return JsonResponse(self._response_data)

            response = self._unfollow(user_name, follow_user)

            if response:
                self._response_data["status"] = 201
                self._response_data["message"] = "Unfollowed user successfully."
                return JsonResponse(self._response_data)
            else:
                self._response_data["status"] = 409
                self._response_data["message"] = "The requested user is already unfollowed."
                return JsonResponse(self._response_data)

        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            self._response_data["status"] = 500
            self._response_data["message"] = "Internal Server Error during unfollowing user call"
            return JsonResponse(self._response_data)
