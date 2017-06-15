from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail, BadHeaderError
from rest_framework.response import Response

from apps.core.models import User
from apps.core.permissions import ReadOnlyOrWriteAccess, StudentNotAllowed
from apps.core.serializers import MailSerializer
from apps.school.models import Student, Teacher
from . import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = User
	queryset = User.objects.all().select_related('person_student', 'person_teacher')
	serializer_class = serializers.UserApiSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [ReadOnlyOrWriteAccess]
	model = Student
	queryset = Student.objects.all().select_related('user')
	serializer_class = serializers.StudentSerializerWithCounselor


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [ReadOnlyOrWriteAccess]
	model = Teacher
	queryset = Teacher.objects.all().select_related('user')
	serializer_class = serializers.TeacherSerializer


class EmailView(views.APIView):
	permission_classes = [StudentNotAllowed]

	def post(self, request):
		serializer = MailSerializer(data=request.data)
		if serializer.is_valid():
			subject = serializer.data['subject']
			message = serializer.data['message']
			to_email = serializer.data['to_email'],
			from_email = request.user.email

			try:
				send_mail(subject, message, from_email, to_email)
				return Response({'results': serializer.data}, status=status.HTTP_200_OK)
			except BadHeaderError:
				return Response({'results': 'Invalid header.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
