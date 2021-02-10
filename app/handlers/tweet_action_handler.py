import logging
import traceback
import sys
import json

from django.http import JsonResponse
from rest_framework.views import APIView

from app.models import Tweet
from app.models import User
from app.serializers import TweetGetRequestSerializer


class TweetActionHandler(APIView):
    """
    Tweet Action Handler Class
    """

    def __init__(self):
        super(TweetActionHandler, self).__init__()
        self._logger = logging.getLogger('django')
        self._response_data = {
            "status": 0,
            "message": ""
        }

    def _authenticate_username(self, user_name):
        '''Authenticates if user with given username is present in database.'''
        try:
            user = User.objects.get(user_name=user_name)
            return user
        except:
            return False

    def _create_tweet(self, user_name, tweet):
        '''Creates tweet for a given user.'''
        try:
            Tweet.objects.create(user_name=self._authenticate_username(user_name), tweet_text=tweet)
            return True
        except Exception as err:
            self._logger.debug("Exception = {0}".format(err))
            return False

    def _delete_tweet(self, user, tweet_id):
        '''Deletes the tweet object.'''
        try:
            tweet = Tweet.objects.get(user_name=self._authenticate_username(user), id=tweet_id)
            tweet.delete()
            return True
        except Exception as err:
            self._logger.debug("Exception = {0}".format(err))
            return False

    def _get_tweets(self, user_name):
        '''Gets a list of tweets for given username.'''
        try:
            # user_obj = User.objects.get(user_name=user_name)
            data = Tweet.objects.filter(
                user_name=self._authenticate_username(user_name)
            )
            data = data.values()

            return list(data), 200
        except:
            return {
                       'msg': 'Error is retrieving data.'
                   }, 500

    def _validate_user(self, user_name):
        try:
            resp = User.objects.get(user_name=user_name)
            self._logger.debug("response data = {0}".format(resp))
            return True
        except Exception as err:
            self._logger.debug("response data = {0}".format(err))
            return False

    def get(self, request):
        '''Reads tweets.
            Request Parameters -
        	    request - Django request object.
            Response Parameters -
        	    200 - List of tweets of given username.
        	    400 - Invalid request. (missing parameters or username)
        '''
        try:
            serializer = TweetGetRequestSerializer.TweetGetRequestSerializer(data=request.query_params)
            if not serializer.is_valid():
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request. "
                return JsonResponse(self._response_data)

            user_name = serializer.data.get('user_name')

            self._logger.debug("user_name is {}.".format(user_name))
            if not user_name:
                self._response_data["status"] = 401
                self._response_data["message"] = "Invalid request as user name not provided."
                return JsonResponse(self._response_data)

            usr_exists = self._validate_user(user_name)
            if not usr_exists:
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid user can't get tweets."
                return JsonResponse(self._response_data)

            resp, code = self._get_tweets(user_name)
            self._logger.debug("response data = {0}".format(resp))

            if resp:
                return JsonResponse({'data': resp}, status=code)
            else:
                return JsonResponse({
                    'data': 'Problem retrieving tweets.'
                })
        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            return JsonResponse({
                'data': 'User does not exist exception'
            })

    def post(self, request):
        '''Creates a tweet.
        		Request Parameters -
        			request - Django request object.
        		Response Parameters -
        			201 - Tweet created successfully.
        			400 - Invalid request. (missing parameters or user_name)
        			409 - Tweet creation failed.
        			500 - Internal Server Error
        '''
        try:
            serializer = TweetGetRequestSerializer.TweetGetRequestSerializer(data=request.data)
            if not serializer.is_valid():
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request. "
                return JsonResponse(self._response_data)

            user_name = serializer.data.get('user_name')
            tweet = serializer.data.get('tweet')
            self._logger.debug("user_name is {0} and tweet is {1}.".format(user_name, tweet))
            if not (user_name or tweet):
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request as user name or tweet not provided."
                return JsonResponse(self._response_data)

            usr_exists = self._validate_user(user_name)
            if not usr_exists:
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid user can't tweet."
                return JsonResponse(self._response_data)

            response = self._create_tweet(user_name, tweet)

            if response:
                self._response_data["status"] = 201
                self._response_data["message"] = "Tweet created successfully."
                return JsonResponse(self._response_data)
            else:
                self._response_data["status"] = 409
                self._response_data["message"] = "Couldn't tweet the text."
                return JsonResponse(self._response_data)

        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            self._response_data["status"] = 500
            self._response_data["message"] = "Internal Server Error during following user call"
            return JsonResponse(self._response_data)

    def delete(self, request):
        '''Deletes a tweet.
            Request Parameters -
        	    request - Django request object.
            Response Parameters -
        	    200 - Tweet deleted successfully.
        	    400 - Invalid request. (missing parameters or username)
        	    404 - tweet with given id not found.
        '''
        try:
            serializer = TweetGetRequestSerializer.TweetGetRequestSerializer(data=request.data)
            if not serializer.is_valid():
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request for delete tweet call. "
                return JsonResponse(self._response_data)

            user_name = serializer.data.get("user_name")
            tweet_id = serializer.data.get("id")
            if not (user_name or tweet_id):
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid request as user not provided."
                return JsonResponse(self._response_data)

            usr_exists = self._validate_user(user_name)

            if not usr_exists:
                self._response_data["status"] = 400
                self._response_data["message"] = "Invalid username"
                return JsonResponse(self._response_data)

            response = self._delete_tweet(user_name, tweet_id)

            if response:
                self._response_data["status"] = 201
                self._response_data["message"] = "Tweet deleted successfully."
                return JsonResponse(self._response_data)
            else:
                self._response_data["status"] = 409
                self._response_data["message"] = "Tweet can't be deleted."
                return JsonResponse(self._response_data)

        except Exception as err:
            self._logger.error("\n{0} \n {1} \n".format(type(err), traceback.format_exc()))
            self._response_data["status"] = 500
            self._response_data["message"] = "Internal Server Error during deleting tweet API."
            return JsonResponse(self._response_data)
