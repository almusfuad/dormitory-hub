from rest_framework import permissions
from booking.models import Booking



class CanCreateReviewPermission(permissions.BasePermission):
      def has_permission(self, request, view):
            if request.method == 'GET':
                  # get the dormitory slug from the request data or URL
                  dormitory_id = request.data.get('dormitory_id') or request.GET.get('dormitory_id')
                  
                  print(dormitory_id)
                  
                  # ensure that the dormitory_slug is provided
                  # if not dormitory_id:
                  #       return False
                  
                  # get the user booking for the same dormitory 
                  user = request.user
                  user_bookings = Booking.objects.filter(student__user = user, dormitory_id = dormitory_id)
                  
                  print(user_bookings.exists())
                  
                  # if the user has any bookings for the same dormitory
                  if user_bookings.exists():
                        first_booking = user_bookings.first()
                        
                        # check if the booking status is checkedin or checkedout
                        if first_booking.status in ['checkedin', 'checkedout']:
                              
                              # check the review that a user has already created a review for this dormitory
                              existing_reviews_count = first_booking.dormitory.review_set.filter(reviewer = user).count()
                              return existing_reviews_count == 0
            return False