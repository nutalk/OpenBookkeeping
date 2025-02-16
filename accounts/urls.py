from django.urls import path, include

from . import views, report_views, account_ann_views


report_api_urls = [
    path('post_total_info/', report_views.post_total_info, name='post_total_info'),
    path('post_month_history/', report_views.post_month_history, name='post_month_history'),
    path('post_month_predict/', report_views.post_month_predict, name='post_month_predict'),
    path('cash_change_next_month/', report_views.cash_change_next_month, name='cash_change_next_month')
]

ana_api_urls = [
    path('analyze_debt/', account_ann_views.analyze_debt, name="analyze_debt"),
]

detial_api_urls = [
    path("prop_detail_post/", views.prop_detail_post, name='prop_detail_post'),
    path('prop_detail_table/', views.prop_detail_table, name='prop_detail_table'),
    path('prop_new/', views.prop_new, name='prop_new'),
    path('prop_del/', views.prop_del, name='prop_del'),
    path('prop_edit/', views.prop_edit, name='prop_edit'),
    path('detail_del/', views.detail_del, name='detail_del'),
    path('detail_new/', views.detail_new, name='detail_new'),
    path('detail_edit/', views.detail_edit, name='detail_edit'),
    path('detail_get_post/', views.detail_get_post, name='detail_get_post'),
]

check_api_urls = [
    path('check_submit/', views.check_submit, name='check_submit'),
]

urlpatterns = []

urlpatterns += report_api_urls + ana_api_urls + detial_api_urls + check_api_urls
