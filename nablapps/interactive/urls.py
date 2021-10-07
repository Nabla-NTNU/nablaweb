from django.urls import path

from .views import (
    AdventCalendarView,
    AdventDoorView,
    QuizListView,
    QuizResultView,
    QuizView,
)
from .views.advent import (
    AdventDoorAdminView,
    SantaCountListView,
    participate_in_competition,
    register_found_santa,
    reset_door,
)
from .views.code_golf import CodeGolf, CodeTaskListView, code_golf_score
from .views.color_picker import submitColorChoice
from .views.place import (
    NewestPlaceView,
    PlaceView,
    get_place_grid,
    get_place_history,
    get_place_info,
    get_place_updates,
    submit_place,
)
from .views.quiz import QuizResultDeleteView, QuizScoreboardView, quiz_reply
from .views.user_test import TestView, test_result

urlpatterns = [
    path(
        "julekalender/<int:year>/",
        AdventCalendarView.as_view(),
        name="advent_calendar",
    ),
    path(
        "julekalender/<int:year>/<int:number>/",
        AdventDoorView.as_view(),
        name="advent_door",
    ),
    path(
        "julekalender/<int:year>/<int:number>/delta/",
        participate_in_competition,
        name="advent_participate",
    ),
    path(
        "julekalender/<int:year>/<int:number>/admin/",
        AdventDoorAdminView.as_view(),
        name="advent_admin",
    ),
    path(
        "julekalender/<int:year>/<int:number>/admin/reset/",
        reset_door,
        name="advent_admin_reset",
    ),
    path("julenisser/", SantaCountListView.as_view(), name="hidden_santa"),
    path(
        "registersanta/<int:santa_id>/<str:redirect_url>/",
        register_found_santa,
        name="register_santa",
    ),
    path("quiz/", QuizListView.as_view(), name="quiz_list"),
    path("quiz/<int:pk>/", QuizView.as_view(), name="quiz"),
    path("quiz/<int:pk>/reply/", quiz_reply, name="quiz_reply"),
    path(
        "quiz/<int:pk>/reply/delete/",
        QuizResultDeleteView.as_view(),
        name="quiz_result_delete",
    ),
    path("quiz/resultat/<int:pk>/", QuizResultView.as_view(), name="quiz_result"),
    path(
        "quiz/highscore/<int:pk>/",
        QuizScoreboardView.as_view(),
        name="quiz_score",
    ),
    path("brukertest/<int:pk>/", TestView.as_view(), name="user_test"),
    path("brukertest/<int:pk>/resultat/", test_result, name="test_result"),
    path("kodegolf/", CodeTaskListView.as_view(), name="code_golf_menu"),
    path("kodegolf/<int:task_id>/", CodeGolf.as_view(), name="code_golf"),
    path("kodegolf/score/<int:task_id>/", code_golf_score, name="code_golf_score"),
    # Color picker
    path("colorpicker/", submitColorChoice, name="color_picker"),
    path("place/", NewestPlaceView.as_view(), name="newest_place"),
    path("place/<int:pk>/", PlaceView.as_view(), name="place"),
    path("place/<int:pk>/grid/", get_place_grid, name="get_place_grid"),
    path("place/<int:pk>/updates/", get_place_updates, name="get_place_updates"),
    path("place/<int:pk>/history/", get_place_history, name="get_place_history"),
    path("place/<int:pk>/info/", get_place_info, name="get_place_info"),
    path("place/<int:pk>/submit/", submit_place, name="submit_place"),
]
