import datetime
import urllib.parse

from adminpanel.models import FAQ, ContactData, StaticData
from core.models import (
    Notification,
    UploadedFile,
    User,
    UserProfile,
    UserSetting,
    ZerodhaData,
)
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from kiteconnect import KiteConnect
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

KITE_CREDS = settings.KITE_CREDS
kite = KiteConnect(api_key=KITE_CREDS["api_key"])


class Redirect(APIView):
    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="zerodha_redirect",
            fields={
                "errors": serializers.CharField(),
                "data": serializers.JSONField(),
                "status": serializers.IntegerField(),
            },
        ),
    )
    def get(self, request: Request, *args, **kwargs):
        uuid = request.query_params.get("uuid", None)

        if not uuid:
            return Response(
                {
                    "errors": "KYC linking Failed!",
                    "data": None,
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        action = request.query_params.get("action", None)
        type = request.query_params.get("type", None)
        zerodha_status = request.query_params.get("status", None)
        request_token = request.query_params.get("request_token", None)

        if zerodha_status == "cancelled":
            return Response(
                {
                    "errors": "Zerodha Auth Failed",
                    "data": None,
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if action and type and zerodha_status and request_token:
            if zerodha_status == "success":
                data = kite.generate_session(
                    request_token, api_secret=KITE_CREDS["secret"]
                )
                try:
                    user: User = User.objects.get(uuid=uuid)
                    # Delete old data
                    ZerodhaData.objects.filter(local_user=user).delete()
                    # Create new data
                    data["local_user_id"] = user.id
                    ZerodhaData.objects.create(**data)

                    return Response(
                        {
                            "errors": "OK",
                            "data": data,
                            "status": status.HTTP_200_OK,
                        },
                        status=status.HTTP_200_OK,
                    )
                except User.DoesNotExist:
                    return Response(
                        {
                            "errors": "Zerodha Auth Failed",
                            "data": None,
                            "status": status.HTTP_401_UNAUTHORIZED,
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

            return Response(
                {
                    "errors": "Zerodha Auth Failed",
                    "data": None,
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {
                "errors": "Improper Request",
                "data": None,
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class KYCView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="zerodha_kyc",
            fields={
                "errors": serializers.CharField(),
                "kyc_url": serializers.URLField(),
                "status": serializers.IntegerField(),
            },
        ),
    )
    def get(self, request: Request, *args, **kwargs):
        uuid = request.user.uuid

        redirect_params = urllib.parse.quote(f"uuid={uuid}")
        redirect_url = f"https://kite.zerodha.com/connect/login?v=3&api_key={KITE_CREDS['api_key']}&redirect_params={redirect_params}"
        
        return Response(
            {
                "errors": "None",
                "kyc_url": redirect_url,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class CheckStatus(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="zerodha_check_status",
            fields={
                "errors": serializers.CharField(),
                "status": serializers.IntegerField(),
            },
        ),
    )
    def get(self, request: Request, *args, **kwargs):
        try:
            zerodha_data: ZerodhaData = ZerodhaData.objects.get(local_user=request.user)
        except ZerodhaData.DoesNotExist:
            return Response(
                {
                    "errors": "KYC NOT DONE",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if not zerodha_data.login_time:
            return Response(
                {
                    "errors": "KYC NOT DONE",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if datetime.datetime.today().day == zerodha_data.login_time.day:
            return Response(
                {
                    "errors": None,
                    "status": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "errors": "KYC Expired",
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
