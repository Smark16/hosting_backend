from django.urls import path
from . import views

urlpatterns = [
     path('', views.ObtainPairView.as_view()),
     path('register', views.registrationView.as_view()),
     path("all_users", views.AllUsers.as_view()),
     path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
     path("get_user/<int:pk>", views.getUser.as_view()),
     path("update_user/<int:pk>", views.updateUser.as_view()),

     # basic info urls
     path("all_basics", views.AllBasic.as_view()),
     path('post_basics', views.post_basic.as_view()),
     path("retrieve_basic/<int:user>", views.retrieveBasic),
     path("update_basic/<int:user_id>", views.updateBasic.as_view()),

     # physical address info
     path("all_physical", views.AllPhysicalAdress.as_view()),
     path('post_physical', views.postPhysical.as_view()),
     path("retrieve_physical/<int:user>", views.retrievePhysical),
     path("update_physical/<int:user_id>", views.updatePhysical.as_view()),

     #capacity urls
     path("all_capacity", views.AllCapacity.as_view()),
     path("post_capacity", views.post_Capacity.as_view()),
     path("retrieve_capacity/<int:user>", views.retrieveCapacity),
     path("update_capacity/<int:user_id>", views.updateCapacity.as_view()),

     # education urls
     path("all_education", views.AllEducation.as_view()),
     path("post_edu", views.post_Education.as_view()),
     path("retrieve_education/<int:user>", views.retrieveEducation),
     path("update_education/<int:user_id>", views.updateEducation.as_view()),

     # category urls
     path("all_category", views.CategoryView.as_view()),
     path("post_cats", views.postCategory.as_view()),
     path("retrieve_cat/<int:user>", views.retrieveCategory),
     path("update_cats/<int:user_id>", views.updateCategory.as_view()),

     # trade urls
     path('employee_trade/', views.TradeCreate.as_view(), name='trade-create'),
     path('post_trade', views.postTrade.as_view()),
     path("retrieve_Trade/<int:user>", views.retrieveTrade),
     path("update_trade/<int:user_id>", views.updateTrade.as_view()),

     # hosting experienc
     path("view_all_hosting", views.AllHosted.as_view()),
     path("all_hosting", views.HostingExperienceCreateView.as_view()),
     path("retrieve_hosted/<int:user>", views.retrieveHosted),
     path("update_host/<int:user_id>", views.UpdateHost.as_view()),

     # additionalInfo urls
     path('all_additional', views.AdditionalView.as_view()),
     path('post_additional', views.postMore.as_view()),
     path("retrive_add/<int:user>",views.retrieveAdd),
     path("update_add/<int:user_id>", views.updateAdd.as_view()),

     #user details
     path('retrieve_Info/<int:pk>', views.retrieveUserInfo),

      #file urls
    path("all_files", views.AllFiles.as_view()),
    path("upload_file", views.UploadFile.as_view()),
    path("update_file/<int:user_id>", views.updateFile.as_view()),
    path("retrieve_File/<int:user>", views.retrieve_File),

    #environment URLS
    path("all_Env", views.EnvironmentView.as_view()),
    path("post_env", views.postEnvironment.as_view()),
    path("update_env/<int:user_id>", views.updateEnv.as_view()),
    path("retrieve_env/<int:user>", views.retrieveEnv),

    #more urls
    path('agriculture/', views.AgricultureListView.as_view(), name='agriculture-list'),
    path('agro-processing/', views.AgroProcessingListView.as_view(), name='agro-processing-list'),
    path('creative-performing-art/', views.Creative_and_Performing_ArtListView.as_view(), name='creative-performing-art-list'),
    path('hotel-hospitality/', views.Hotel_and_HospitalityListView.as_view(), name='hotel-hospitality-list'),
    path('beauty-cosmetology/', views.Beauty_and_CosmetologyListView.as_view(), name='beauty-cosmetology-list'),
    path('manufacturing/', views.ManufacturingListView.as_view(), name='manufacturing-list'),
    path('construction/', views.ConstructionListView.as_view(), name='construction-list'),
    path('food-processing/', views.Food_ProcessingListView.as_view(), name='food-processing-list'),
    path('social-services/', views.Social_ServicesListView.as_view(), name='social-services-list'),
    path('professional-technical-services/', views.Professional_TechnicalServicesListView.as_view(), name='professional-technical-services-list'),
    path('engineering/', views.EngineeringListView.as_view(), name='engineering-list'),
    path('tourism-hospitality/', views.Tourism_and_HospitalityListView.as_view(), name='tourism-hospitality-list'),
    path('environment-protection/', views.Environment_ProtectionListView.as_view(), name='environment-protection-list'),
    path('fishing/', views.FishingListView.as_view(), name='fishing-list'),
    path('ict-digital-media/', views.ICT_and_DigitalMediaListView.as_view(), name='ict-digital-media-list'),
    path('trade-retail-wholesale/', views.TradeRetail_and_WholesaleListView.as_view(), name='trade-retail-wholesale-list'),
    path('mechanical/', views.MechanicalListView.as_view(), name='mechanical-list'),
    path('tailoring-textiles/', views.Tailoring_and_TextilesListView.as_view(), name='tailoring-textiles-list'),

# finshed
    path("finished", views.finished.as_view()),

]