from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
# from django.contrib.sitemaps.views import sitemap
from . import views

# app_name = 'CoreApp'

# sitemaps_dict = {'Static_sitemap': sitemaps.StaticSitemap,
#                 'Product_sitemap': sitemaps.ProductSitemap,
#                 'Campaign_sitemap': sitemaps.CampaignSitemap,
#                 'Post_sitemap': sitemaps.PostSitemap,
#                 'FAQ_sitemap': sitemaps.FAQCategoriesSitemap,
#                 'Store_sitemap': sitemaps.StoreSitemap,
#                 'Product_sitemap': sitemaps.ProductSitemap
#                 }

urlpatterns = [
    # Maintenance
    # path('maintenance/', views.MaintenanceView.as_view(), name='maintenance_page'),'

    # This is for sitemap.xml
    # path('SiteMapMode.xml', sitemap, {'sitemaps': sitemaps_dict},
    #  name='django.contrib.sitemaps.views.sitemap'),
]


# handler404 = 'apps.baseApp.views.error_404'
# handler500 = 'apps.baseApp.views.error_500'
