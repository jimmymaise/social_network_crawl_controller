from DBService.Service.ReportService import ReportService
from DBService.Service.PostService import PostService
from DBService.Service.KOLService import KOLService
from DBService.Service.UserService import UserService
from DBService.Service.PageService import PageService
from DBService.Service.NormalUserService import NormalUserService
from DBService.Service.FollowerService import FollowerService
from DBService.Service.PostReactionService import PostReactionService

# Create services
report_service = ReportService()
post_service = PostService()
kol_service = KOLService()
user_service = UserService()
page_service = PageService()
normaluser_service = NormalUserService()
follower_service = FollowerService()
postreaction_service = PostReactionService()
