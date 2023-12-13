from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from .models import Status, Profile
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class MySecureView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a secure endpoint!'})



@api_view(['POST', 'GET'])
def change_user_status(request):
    user = request.user
    new_status = request.data.get('status', '').lower()

    try:
        user_profile = Profile.objects.get(user=user)
        user_status = Status.objects.get(id=user_profile.user_status.id)
        current_status = user_status.status.lower()
        print(current_status)

        if current_status == 'checkedin':
            if new_status == 'checkedout':
            # if new_status in ['breakedin', 'checkedout']:
                user_status.status = new_status
                user_status.checkedout_time = timezone.now()
                user_status.duty_time = user_status.checkedout_time - user_status.checkedin_time
                user_status.save()
                return Response({'detail': 'User status and checkedout time updated successfully.', 'duty_time': user_status.duty_time}, status=status.HTTP_200_OK)

                # return Response({'detail': 'User status updated successfully.'}, status=status.HTTP_200_OK
            
            elif new_status=='breakedin':
                user_status.status = new_status
                user_status.breakedin_time = timezone.now()
                user_status.save()
                return Response({'detail': 'User status and breakedin time updated successfully.', 'breakedin_in': user_status.breakedin_time}, status=status.HTTP_200_OK)

                
            
            elif new_status == 'checkedin' or new_status == 'breakedout':
                return Response({'detail': 'Invalid operation for user checked in.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid user status.'}, status=status.HTTP_400_BAD_REQUEST)

        elif current_status == 'checkedout':
            if new_status == 'checkedin':
                # Valid operation for a user checked out
                user_status.status = new_status
                user_status.checkedout_time=None
                user_status.breakedin_time=None
                user_status.breakedout_time=None
                user_status.duty_time=None
                user_status.break_time=None


                user_status.checkedin_time = timezone.now()
                user_status.save()
                return Response({'detail': 'User status and time for checkingin updated successfully.'}, status=status.HTTP_200_OK)
            elif new_status in ['breakedin', 'checkedout', 'breakedout']:
                return Response({'detail': 'Invalid operation for user checked out.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid user status.'}, status=status.HTTP_400_BAD_REQUEST)

        elif current_status == 'breakedin':
            if new_status=='breakedout':
                user_status.status = 'checkedin'
                user_status.breakedout_time = timezone.now()
                # print(user_status.breakedin_time)
                user_status.break_time = user_status.breakedout_time - user_status.breakedin_time+user_status.break_time
                # user_status.break_time += user_status.breakedout_time - user_status.breakedin_time
                user_status.save()
                # return Response({'detail': 'User status and breakedout time updated successfully.'}, status=status.HTTP_200_OK)
                return Response({'detail': 'User status and breakedout time updated successfully.', 'Break_time': user_status.break_time}, status=status.HTTP_200_OK)



                
            elif new_status=='checkedout':
                user_status.status = new_status
                user_status.breakedout_time=timezone.now()
                user_status.break_time = user_status.breakedout_time - user_status.breakedin_time
                user_status.checkedout_time=timezone.now()
                user_status.duty_time = user_status.breakedin_time - user_status.checkedin_time

                user_status.save()
                return Response({'detail': 'User status updated successfully.'}, status=status.HTTP_200_OK)
            elif new_status == 'checkedin':
                return Response({'detail': 'Invalid operation for user on break.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid user status.'}, status=status.HTTP_400_BAD_REQUEST)

        elif current_status == 'breakedout':
            if new_status in ['checkedout', 'breakedin']:
                # Valid operations for a user off break
                user_status.status = new_status
                user_status.save()
                return Response({'detail': 'User status updated successfully.'}, status=status.HTTP_200_OK)
            elif new_status == 'breakedout' or new_status == 'checkedin':
                return Response({'detail': 'Invalid operation for user off break.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid user status.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Handle any other scenarios or provide an appropriate response
            return Response({'detail': 'Invalid user status.'}, status=status.HTTP_400_BAD_REQUEST)

    except Status.DoesNotExist:
        user_status = Status.objects.create(status=new_status)
        user_profile = Profile.objects.create(user=user, user_status=user_status)
        print('New Status created successfully!')
        # user_status = Status(user=user, status=new_status)
        # user_status.save()
        # return Response({ 'User status created successfully.'}, status=status.HTTP_201_CREATED)
