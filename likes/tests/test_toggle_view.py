import json
from likes.models import toggle_like
from .base import BaseLikeTest, BaseViewTest, User


class LoggedInTest(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.login()


class TestProcessLikePress(LoggedInTest):
    """Tests a logged in user trying to post a like press"""

    def test_post_like(self):
        self.client.post(self.url, self.post_data)
        self.assertUserLikes(self.user, self.object)

    def test_return_bad_request_on_missing_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400, "Should return HTTP 400 Bad Request on missing data")

    def test_return_bad_request_on_unknown_content_type(self):
        response = self.client.post(self.url, {'contenttypeId': 1000, 'objectId': 1})
        self.assertEqual(response.status_code, 400)

    def test_return_bad_request_on_unknown_object(self):
        data = self.post_data.copy()
        data['objectId'] = 1000
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_post_unlike(self):
        toggle_like(
            instance=self.object,
            user=self.user
        )
        self.client.post(self.url, self.post_data)
        self.assertNotUserLikes(self.user, self.object)

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "Only POST requests should be allowed, not GET.")


class TestJsonResponse(LoggedInTest):
    """Test the response from posting a press"""
    def setUp(self):
        super().setUp()

        self.initial_likes = 10
        self.users = [User.objects.create(username="user{}".format(i)) for i in range(self.initial_likes)]
        for user in self.users:
            toggle_like(self.object, user)

    def test_returns_json(self):
        response = self.client.post(self.url, self.post_data)
        result_dict = json.loads(response.content.decode())
        self.assertIsInstance(result_dict, dict)

    def test_returns_liked_when_liked(self):
        response = self.client.post(self.url, self.post_data)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(result_dict['liked'], True)

    def test_returns_not_liked_when_unliked(self):
        toggle_like(self.object, self.user)
        response = self.client.post(self.url, self.post_data)
        result_dict = json.loads(response.content.decode())
        self.assertEqual(result_dict['liked'], False)

    def test_returns_correct_count(self):
        response = self.client.post(self.url, self.post_data)
        result_dict = json.loads(response.content.decode())
        likes = self.initial_likes + 1
        self.assertEqual(result_dict['count'], likes)


class TestNotLoggedInUser(BaseViewTest):
    def test_post_like_redirects_on_not_logged_in_user(self):
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, 302, "Not logged in users should be redirected")
