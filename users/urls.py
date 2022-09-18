from django.urls import path

from .views import CreateUserView, CreatePortfolioView, UpdateDestroyPortfolioView, UpdateDestroyProfileView, \
    CreatePortfolioImageView, UpdateDestroyPortfolioImageView, CreateImageCommentView, ImageListView, LogoutView

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="sign_up"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("profile/<int:pk>/", UpdateDestroyProfileView.as_view(), name="update_delete_profile"),

    path("portfolio/", CreatePortfolioView.as_view(), name="create_portfolio"),
    path("portfolio/<int:pk>/", UpdateDestroyPortfolioView.as_view(), name="update_delete_portfolio"),
    path("portfolio_image/", CreatePortfolioImageView.as_view(), name="create_portfolio_image"),
    path("portfolio_image/<int:pk>/", UpdateDestroyPortfolioImageView.as_view(), name="update_delete_portfolio_image"),

    path("image_comment/", CreateImageCommentView.as_view(), name="create_image_comment"),
    path("image_search/", ImageListView.as_view(), name="image_search"),
]
