from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from company.models import Company
from .models import User
from accounts import serializers


# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyEmailView(generics.GenericAPIView):  # for authenticated users
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.verify_email()

        return Response({'message': 'Please check your email for verification code'}, status=status.HTTP_200_OK)


class VerificationCodeView(generics.GenericAPIView):
    serializer_class = serializers.VerificationCodeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.verification_code == request.verification_code:
            user.email_verified = True
            user.verification_code = ''
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Incorrect code'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        if email in User.objects.values_list('email', flat=True):
            user = User.objects.get(email=email)
            user.verify_email()
            # print(1, email, user)
            return Response({'message': 'Check your email for password reset'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': f'There is no users with this {email} email'},
                            status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request):
        # print(request.data)
        email = request.data.get('email')
        ver_code = request.data.get('verification_code')
        p1 = request.data.get('password1')
        p2 = request.data.get('password2')
        if email in User.objects.values_list('email', flat=True):
            user = User.objects.get(email=email)
            if user.verification_code == ver_code:
                if p1 == p2:
                    user.set_password(p1)
                    user.save()
                    return Response({'message': 'Your password succesfully changed'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Password1 does not equal password2'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': f'This {email} dose not exist'}, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(generics.GenericAPIView):
    serializer_class = serializers.UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserDataSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateUserSerializer

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        for attr in data:
            if attr == 'email' and data['email'] != user.email:
                user.email_verified = False

            user.__setattr__(attr, data[attr])

        user.save()

        data['message'] = 'Succesfully updated'
        return Response(data, status=status.HTTP_200_OK)


class AddEmployeeView(generics.GenericAPIView):
    serializer_class = serializers.AddEmployeeSerializer

    def post(self, request):
        user = request.user
        if user.type != 'admin':
            return Response({'message': 'You are not allowed to add employee'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AllEmployeeDataView(generics.GenericAPIView):
    serializer_class = serializers.AllEmployeeDataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.type != 'admin' and user != Company.owner:
            return Response({'message': 'You are not allowed to get employee data'}, status=status.HTTP_400_BAD_REQUEST)
        company_id = kwargs.get('pk', '')
        company = Company.objects.get(id=company_id)
        queryset = company.employees.all()
        serializer = serializers.AllEmployeeDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteEmployeeView(generics.GenericAPIView):
    serializer_class = serializers.DeleteEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        if user.type != 'admin' and user != Company.owner:
            return Response({'message': 'You are not allowed to delete employee'}, status=status.HTTP_400_BAD_REQUEST)
        ids = request.data.get('employee_ids')
        idss = []
        for i in range(len(ids)):
            employee_id = ids[i]
            employee = User.objects.get(id=employee_id)
            company_id = request.data.get('company_id')
            company = Company.objects.get(id=company_id)

            if employee in company.employees.all():
                idss.append(employee.id)
                employee.delete()
                employee.save()

        s = ', '.join(idss)
        return Response({'message': f'{s}th id Employee is succesfully deleted'}, status=status.HTTP_200_OK)
