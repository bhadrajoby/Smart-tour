"""
URL configuration for Smart_Tour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('admin_index/',views.admin_index),
    path('change_password_get/',views.change_password_get),
    path('send_notification_get/',views.send_notification_get),
    path('send_notification_post/',views.send_notification_post),
    path('verify_agency_get/',views.verify_agency_get),
    path('view_complaint_get/',views.view_complaint_get),
    path('view_emergency_alert_get/',views.view_emergency_alert_get),
    path('view_feedback_get/',views.view_feedback_get),
    path('view_places_get/',views. view_places_get),
    path('login_page/',views.login_page_get),
    path('login_post/',views.login_post),
    path('admin_changepassword_post/',views.admin_changepassword_post),
    path('view_notification_get/',views.view_notification_get),
    path('admin_delete_notification/<id>',views.admin_delete_notification),
    path('verified_agency/',views.verified_agency),
    path('logout_get/',views.logout_get),
    path('accept_agency/<id>',views.accept_agency),
    path('reject_agency/<id>',views.reject_agency),

# ----------------agency

    path('register/',views.register),
    path('register_post/',views.register_post),
    path('view_profile/',views.view_profile),
    path('add_places/',views.add_places),
    path('add_places_post/',views.add_places_post),
    path('assign_guide/',views.assign_guide),
    path('AGENCY_change_password/',views.AGENCY_change_password),
    path('agency_changepassword_post/',views.agency_changepassword_post),
    path('edit_places/',views.edit_places),
    path('send_reply/<id>',views.send_reply),
    path('send_reply_post/',views.send_reply_post),
    path('view_complaint/',views.view_complaint),
    path('view_emergency_alert/',views.view_emergency_alert),
    path('agency_view_instruction/',views.agency_view_instruction),
    path('agency_view_places/',views.agency_view_places),
    path('view_request_and_verify/',views.view_request_and_verify),
    path('agency_home/',views.agency_home),
    path('verify_guide/',views.verify_guide),
    path('agency_accept_guide/<id>',views.agency_accept_guide),
    path('agency_reject_guide/<id>',views.agency_reject_guide),
    path('verified_guide/',views.verified_guide),
    path('delete_place/<id>',views.delete_place),
    path('edit_place/<id>',views.edit_place),
    path('edit_places_post/',views.edit_places_post),
    path('agency_view_booking/',views.agency_view_booking),
    path('admin_view_feed/',views.admin_view_feed),
    path('assign_guide/<id>',views.assign_guide),
    path('assign_guide_post/<id>',views.assign_guide_post),
    path('agency_edit_profile/', views.agency_edit_profile),
    path('agency_edit_profile_post/', views.agency_edit_profile_post),
    path('view_assign_guide/', views.view_assign_guide),
    path('admin_reply/<id>', views.admin_reply),
    path('admin_reply_post/<id>', views.admin_reply_post),

    # -----------------------guide

    path('android_login/',views.android_login),
    path('guide_register_post/',views.guide_register_post),
    path('guide_change/',views.guide_change),
    path('guide_view_profile/',views.guide_view_profile),
    path('view_agency_places/',views.view_guide_places),
    path('view_assign/',views.view_assign),
    path('add_instruction/',views.add_instruction),
    path('guide_view_instruction/',views.guide_view_instruction),
    path('guide_instructionviewforedit/',views.guide_instructionviewforedit),
    path('edit_instruction/',views.edit_instruction),
    path('guide_profileviewforedit/',views.guide_profileviewforedit),
    path('guide_edit_profile/',views.guide_edit_profile),
    path('guide_delete_instruction/',views.guide_delete_instruction),

    # -----------------------user

    path('user_register_post/',views.user_register_post),
    path('user_search_places/',views.user_search_places),
    path('user_search_agency/',views.user_search_agency),
    path('send_complaint/',views.send_complaint),
    path('user_view_complaint/',views.user_view_complaint),
    path('view_user_places/',views.view_user_places),
    path('send_feedback_user/',views.send_feedback_user),
    path('user_view_agency/',views.user_view_agency),
    path('send_agencyfeedback_user',views.send_agencyfeedback_user),
    path('add_moments/',views.add_moments),
    path('view_memories_user/',views.view_memories_user),
    path('user_to_expert_chatview/',views.user_to_expert_chatview),
    path('user_to_expert_chatview/',views.user_to_expert_chatview),
    path('user_to_expert_sendchat/',views.user_to_expert_sendchat),
    path('user_view_profile/',views.user_view_profile),
    path('user_profileviewforedit/',views.user_profileviewforedit),
    path('user_edit_profile/',views.user_edit_profile),
    path('user_add_places/',views.user_add_places),
    path('view_non_popular/',views.view_non_popular),
    path('user_add_booking/',views.user_add_booking),
    path('user_view_package/',views.user_view_package),
    path('user_view_notification/',views.user_view_notification),


    path('agency_chat_to_user/<id>',views.agency_chat_to_user),
    path('delete_package/<id>',views.delete_package),
    path('view_package/',views.view_package),
    path('add_package/',views.add_package),
    path('confrim_requests/',views.confrim_requests),
    path('completed_requests/',views.completed_requests),
    path('agency_chat_with_user/<id>',views.agency_chat_with_user),
    path('chat_view/',views.chat_view),
    path('chat_send/<msg>',views.chat_send),


    path('view_user_beach_places/',views.view_user_beach_places),
    path('view_user_city_places/',views.view_user_city_places),
    path('view_user_desert_places/',views.view_user_desert_places),
    path('view_user_hills_places/',views.view_user_hills_places),
    path('recommend_places/',views.recommend_places),
    path('recommend_users/',views.recommend_users),
    path('updatelocation/',views.updatelocation),
    path('user_predict_weather/',views.user_predict_weather),
    path('user_view_booking/',views.user_view_booking),
    path('user_sent_emergency_sos/',views.user_sent_emergency_sos),

    path('search_package_by_price/',views.search_package_by_price),
    path('user_view_assigned_guide/',views.user_view_assigned_guide),
    path('guide_updatelocation/',views.guide_updatelocation),
    path('view_other_memories_user/',views.view_other_memories_user),
    path('user_view_guide_guidence/',views.user_view_guide_guidence),













]