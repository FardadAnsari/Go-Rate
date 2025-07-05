from django.apps import AppConfig
import threading

class FoodhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodhub'

    def ready(self):
        from .models import CachedYearlyStats
        from .search_algorithms import compute_yearly_stats

        if not CachedYearlyStats.objects.exists():
            print("Running cache computation at startup...")
            compute_yearly_stats()

        #threading.Thread(target=run_if_no_cache).start()
