from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import pagination
from .models import JustEat
from .serializers import JustEatSerializer
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


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


class JustEatView(APIView):
    def get(self, request):
        start_date_str = request.query_params.get('from', None)
        end_date_str = request.query_params.get('to', None)
        preorder = request.query_params.get('preorder', None)
        openCollection = request.query_params.get('openCollection', None)
        openDelivery = request.query_params.get('opendelivery', None)
        is_Collection = request.query_params.get('collection', None)
        is_Delivery = request.query_params.get('delivery', None)
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

        queryset = JustEat.objects.all()

        if cuisines:
            queryset = queryset.filter(cuisines=cuisines)

        if rating:
            queryset = queryset.filter(rating=rating)

        def filter_boolean(qs, val, field_name):
            val = val.lower()
            if val in ['true', '1', 'yes']:
                return qs.filter(**{field_name: True})
            elif val in ['false', '0', 'no']:
                return qs.filter(**{field_name: False})
            else:
                raise ValueError(f"Invalid value for {field_name}")

        try:
            if preorder:
                queryset = filter_boolean(queryset, preorder, 'isOpenNowForPreorder')
            if openCollection:
                queryset = filter_boolean(queryset, openCollection, 'isOpenNowForCollection')
            if openDelivery:
                queryset = filter_boolean(queryset, openDelivery, 'isOpenNowForDelivery')
            if is_Collection:
                queryset = filter_boolean(queryset, is_Collection, 'isCollection')
            if is_Delivery:
                queryset = filter_boolean(queryset, is_Delivery, 'isDelivery')
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        if start_date:
            queryset = queryset.filter(last_update__gte=start_date)
        if end_date:
            queryset = queryset.filter(last_update__lte=end_date)

        all_qs = JustEat.objects.all()
        total_records = all_qs.count()
        filtered_total_records = queryset.count()

        status_counts = {
            "preorder": {
                "open": all_qs.filter(isOpenNowForPreorder=True).count(),
                "closed": all_qs.filter(isOpenNowForPreorder=False).count(),
            },
            "collection": {
                "open": all_qs.filter(isOpenNowForCollection=True).count(),
                "closed": all_qs.filter(isOpenNowForCollection=False).count(),
            },
            "delivery": {
                "open": all_qs.filter(isOpenNowForDelivery=True).count(),
                "closed": all_qs.filter(isOpenNowForDelivery=False).count(),
            },
            "is_collection": {
                "open": all_qs.filter(isCollection=True).count(),
                "closed": all_qs.filter(isCollection=False).count(),
            },
            "is_delivery": {
                "open": all_qs.filter(isDelivery=True).count(),
                "closed": all_qs.filter(isDelivery=False).count(),
            },
        }

        filtered_status_counts = {}

        def add_filtered_counts(param, field_name, label):
            val = request.query_params.get(param, None)
            if val:
                val = val.lower()
                if val in ['true', '1', 'yes']:
                    open_count = queryset.count()
                    closed_count = 0
                else:
                    open_count = 0
                    closed_count = queryset.count()
                filtered_status_counts[label] = {"open": open_count, "closed": closed_count}

        add_filtered_counts('preorder', 'isOpenNowForPreorder', 'preorder')
        add_filtered_counts('openCollection', 'isOpenNowForCollection', 'collection')
        add_filtered_counts('opendelivery', 'isOpenNowForDelivery', 'delivery')
        add_filtered_counts('iscollection', 'isCollection', 'is_collection')
        add_filtered_counts('isdelivery', 'isDelivery', 'is_delivery')

        extra_data = {
            "status_counts": status_counts,
            "total_records": total_records,
        }

        if filtered_status_counts:
            extra_data["filtered_status_counts"] = filtered_status_counts
            extra_data["filtered_total_records"] = filtered_total_records

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = JustEatSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data, extra_data=extra_data)
