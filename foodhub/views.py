
from rest_framework import pagination
from .serializers import FoodHubSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from collections import defaultdict
from .models import FoodhubModel


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data, extra_data=None):
        response_data = {
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'pages': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
        }
        if extra_data:
            response_data.update(extra_data)
        response_data['results'] = data

        return Response(response_data)


class FoodHubView(APIView):
    def get(self, request):
        start_date_str = request.query_params.get('from', None)
        end_date_str = request.query_params.get('to', None)
        delivery = request.query_params.get('delivery', None)
        collection = request.query_params.get('collection', None)
        restaurant = request.query_params.get('restaurant', None)
        county = request.query_params.get('county', None)
        cuisines = request.query_params.get('cuisines', None)
        rating = request.query_params.get('rating', None)



        start_date = None
        end_date = None
        try:
            if start_date_str:
                start_date = make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
            if end_date_str:
                end_date = make_aware(datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(microseconds=1))
            if start_date and end_date and start_date > end_date:
                return Response({"error": "start_date must be before end_date."}, status=400)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        queryset = FoodhubModel.objects.all()


        if county:
            queryset = queryset.filter(county=county)

        if cuisines:
            queryset = queryset.filter(cuisines=cuisines)

        if rating:
            queryset = queryset.filter(rating=rating)


        if start_date:
            queryset = queryset.filter(last_update__gte=start_date)
        if end_date:
            queryset = queryset.filter(last_update__lte=end_date)

        def filter_boolean(qs, val, field_name):
            val = val.lower()
            if val in ['true', '1', 'yes']:
                return qs.filter(**{field_name: True})
            elif val in ['false', '0', 'no']:
                return qs.filter(**{field_name: False})
            else:
                raise ValueError(f"Invalid value for {field_name}")

        try:
            if delivery:
                queryset = filter_boolean(queryset, delivery, 'store_status_delivery')
            if collection:
                queryset = filter_boolean(queryset, collection, 'store_status_collection')
            if restaurant:
                queryset = filter_boolean(queryset, restaurant, 'store_status_restaurant')
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        all_qs = FoodhubModel.objects.all()
        total_records = all_qs.count()
        filtered_total_records = queryset.count()

        status_counts = {
            "delivery": {
                "open": all_qs.filter(store_status_delivery=True).count(),
                "closed": all_qs.filter(store_status_delivery=False).count(),
            },
            "collection": {
                "open": all_qs.filter(store_status_collection=True).count(),
                "closed": all_qs.filter(store_status_collection=False).count(),
            },
            "restaurant": {
                "open": all_qs.filter(store_status_restaurant=True).count(),
                "closed": all_qs.filter(store_status_restaurant=False).count(),
            }
        }

        filtered_status_counts = {}

        if delivery:
            val = delivery.lower()
            if val in ['true', '1', 'yes']:
                delivery_open = queryset.count()
                delivery_closed = 0
            else:
                delivery_open = 0
                delivery_closed = queryset.count()
            filtered_status_counts["delivery"] = {"open": delivery_open, "closed": delivery_closed}

        if collection:
            val = collection.lower()
            if val in ['true', '1', 'yes']:
                collection_open = queryset.count()
                collection_closed = 0
            else:
                collection_open = 0
                collection_closed = queryset.count()
            filtered_status_counts["collection"] = {"open": collection_open, "closed": collection_closed}

        if restaurant:
            val = restaurant.lower()
            if val in ['true', '1', 'yes']:
                restaurant_open = queryset.count()
                restaurant_closed = 0
            else:
                restaurant_open = 0
                restaurant_closed = queryset.count()
            filtered_status_counts["restaurant"] = {"open": restaurant_open, "closed": restaurant_closed}

        extra_data = {
            "status_counts": status_counts,
            "total_records": total_records,
        }

        if filtered_status_counts:
            extra_data["filtered_status_counts"] = filtered_status_counts
            extra_data["filtered_total_records"] = filtered_total_records

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = FoodHubSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data, extra_data=extra_data)





class YearlyBreakdownView(APIView):
    def get(self, request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)

        interval_days = 365 // 36  # ≈10 days
        results = []

        for i in range(36):
            period_start = start_date + timedelta(days=i * interval_days)
            period_end = period_start + timedelta(days=interval_days)

            count = FoodhubModel.objects.filter(
                last_update__gte=period_start,
                last_update__lt=period_end
            ).count()

            results.append({
                "period_start": period_start.date(),
                "period_end": period_end.date(),
                "count": count
            })

        return Response(results)






# views.py

class Foodhub10DayStatsView(APIView):
    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        postcode = request.query_params.get('postcode')

        # if not year or not postcode:
        #     return Response({"error": "Please provide 'year' and 'postcode'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
            start_date = make_aware(datetime(year, 1, 1))
            end_date = make_aware(datetime(year + 1, 1, 1))
        except:
            return Response({"error": "Invalid year format."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Query once for all records in year/postcode
        records = FoodhubModel.objects.filter(
            postcode__startswith=postcode,
            last_update__gte=start_date,
            last_update__lt=end_date
        ).only('last_update')

        # Step 2: Count per day
        counts_per_day = defaultdict(int)
        for obj in records:
            day = obj.last_update.date()
            counts_per_day[day] += 1

        # Step 3: Build result with all 365 days
        result = []
        for i in range((end_date - start_date).days):
            day = (start_date + timedelta(days=i)).date()
            result.append({
                'date': day,
                'count': counts_per_day.get(day, 0)
            })

        return Response(result, status=status.HTTP_200_OK)