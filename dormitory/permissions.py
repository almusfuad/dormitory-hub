from rest_framework import permissions



class CanCreateReviewPermission(permissions.BasePermission):
      def has_permission(self, request, view):
            if request.method == 'POST':
                  # get the dormitory slug from the request data or URL
                  dormitory_slug = request.data.get('dormitory_slug') or request.GET.get('dormitory_slug')
                  
                  # ensure that the dormitory_slug is provided
                  if not dormitory_slug:
                        return False
                  
                  # get the user booking for the same dormitory 
                  user_bookings = request.user.booking_set.filter(dormitory__slug = dormitory_slug)
                  
                  # if the user has any bookings for the same dormitory
                  if user_bookings.exists():
                        # get the first booking
                        first_booking = user_bookings.first()
                        
                        # check if the booking status is checkedin or checkedout
                        if first_booking.status in ['checkedin', 'checkedout']:
                              
                              # check the review that a user has already created a review for this dormitory
                              existing_reviews_count = first_booking.dormitory.review_set.filter(reviewer = request.user).count()
                              return existing_reviews_count == 0
            return False