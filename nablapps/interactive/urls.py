from django.conf.urls import url
from django.urls import path
from .views import AdventCalendarView, AdventDoorView, QuizListView, QuizView, QuizResultView
from .views.quiz import quiz_reply, QuizScoreboardView, QuizResultDeleteView
from .views.user_test import test_result, TestView
from .views.advent import participate_in_competition, AdventDoorAdminView, reset_door, register_found_santa, SantaCountListView
from .views.code_golf import CodeGolf, code_golf_score, CodeTaskListView
from .views.color_picker import submitColorChoice
from .views.place import NewestPlaceView, PlaceView, get_place_grid, submit_place, get_place_history, get_place_updates, get_place_info

urlpatterns = [
	url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/$',
		AdventDoorView.as_view(),
		name="advent_door"),
	url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/delta$',
		participate_in_competition,
		name="advent_participate"),
	url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/admin$',
		AdventDoorAdminView.as_view(),
		name="advent_admin"),
	url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/admin/reset$',
		reset_door,
		name="advent_admin_reset"),
	url(r'^julekalender/(?P<year>\d+)/$',
		AdventCalendarView.as_view(),
		name="advent_calendar"),
    
    url(r'^julenisser/',
        SantaCountListView.as_view(),
        name="hidden_santa"),
    url(r'^registersanta/(?P<santa_id>\w)/(?P<redirect_url>[\w\-]+)/$',
        register_found_santa,
        name="register_santa"),

	url(r'^quiz/$',
		QuizListView.as_view(),
		name="quiz_list"),
	url(r'^quiz/(?P<pk>[0-9]+)$',
		QuizView.as_view(),
		name="quiz"),
	url(r'^quiz/(?P<pk>[0-9]+)/reply$',
		quiz_reply,
		name="quiz_reply"),
	url(r'^quiz/(?P<pk>[0-9]+)/reply/delete$',
		QuizResultDeleteView.as_view(),
		name="quiz_result_delete"),
	url(r'^quiz/resultat/(?P<pk>[0-9]+)$',
		QuizResultView.as_view(),
		name="quiz_result"),
	url(r'^quiz/highscore/(?P<pk>[0-9]+)$',
		QuizScoreboardView.as_view(),
		name="quiz_score"),

	url(r'^brukertest/(?P<pk>[0-9]+)$',
		TestView.as_view(),
		name="user_test"),
	url(r'^brukertest/(?P<pk>[0-9]+)/resultat$',
		test_result,
		name="test_result"),

    url(r'^kodegolf/$', CodeTaskListView.as_view(), name="code_golf_menu"),
    url(r'^kodegolf/(?P<task_id>[0-9]+)$', CodeGolf.as_view(), name="code_golf"),
    url(r'^kodegolf/score/(?P<task_id>[0-9]+)$', code_golf_score, name="code_golf_score"),

    # Color picker
    url(r'^colorpicker/$', submitColorChoice, name="color_picker"),

    path('place/', NewestPlaceView.as_view(), name="newest_place"),
    path('place/<int:pk>', PlaceView.as_view(), name="place"),
    path('place/<int:pk>/grid', get_place_grid, name="get_place_grid"),
    path('place/<int:pk>/updates', get_place_updates, name="get_place_updates"),
    path('place/<int:pk>/history', get_place_history, name="get_place_history"),
    path('place/<int:pk>/info', get_place_info, name="get_place_info"),
    path('place/<int:pk>/submit', submit_place, name="submit_place"),
]
