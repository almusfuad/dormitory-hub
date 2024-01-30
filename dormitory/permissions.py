from rest_framework import permissions
# from booking.models import Booking


class IsReviewOwner(permissions.BasePermission):
      def has_object_permission(self, request, view, obj):
            return obj.user == request.user


# class IsStayed(permissions.BasePermission):
#       message = "You must have a booking to create or update a review for this dormitory."
#       def has_permission(self, request, view):
#             if request.method == 'POST':
#                   user = request.user
#                   dormitory_id = view.kwargs.get('id')
#                   print(f"dormitory id: {dormitory_id}")
#                   if not dormitory_id:
#                         return False
                  
#                   # check for the booking records of the user and dormitory
#                   booking_exists = Booking.objects.filter(student__user = user, dormitory__id = dormitory_id).exists()
                  
#                   return booking_exists
#             return True
            