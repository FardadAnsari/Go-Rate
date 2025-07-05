from datetime import timedelta
from django.utils import timezone
from .models import FoodhubModel, CachedYearlyStats

def compute_yearly_stats():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    interval_days = 365 // 36

    results = []

    for i in range(36):
        midpoint = start_date + timedelta(days=i * interval_days + interval_days // 2)
        found = False
        max_steps = interval_days // 2

        for step in range(max_steps + 1):  # gradually expand search
            for offset in [-step, step]:
                check_date = midpoint + timedelta(days=offset)
                if check_date < start_date or check_date > end_date:
                    continue

                count = FoodhubModel.objects.filter(
                    last_update__date=check_date.date()
                ).count()

                if count > 0:
                    results.append({
                        "point": i + 1,
                        "date": check_date.date(),
                        "count": count
                    })
                    found = True
                    break
            if found:
                break

        if not found:
            results.append({
                "point": i + 1,
                "date": midpoint.date(),
                "count": 0
            })

    # Save to DB
    CachedYearlyStats.objects.all().delete()  # clear old cache
    CachedYearlyStats.objects.create(data=results)
