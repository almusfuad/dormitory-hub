from rest_framework import permissions
from booking.models import Booking


class IsReviewOwner(permissions.BasePermission):
      def has_object_permission(self, request, view, obj):
            return obj.user == request.user


class IsStayed(permissions.BasePermission):
      def has_permission(self, request, view):
            
            booking = Booking.objects.get(student=request.user.basicinformation)
            

            # try:
            #       return booking.status == 'checkedout' # If the user has checked out he have stayed
            # except Booking.DoesNotExist:
            #       return False
            # return False