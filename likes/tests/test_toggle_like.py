from likes.models import toggle_like
from .base import BaseLikeTest


class TestLikeModel(BaseLikeTest):

    def test_toggle(self):
        self.assertNotUserLikes(self.user, self.object)

        toggle_like(
            instance=self.object,
            user=self.user
        )

        self.assertUserLikes(self.user, self.object)

        toggle_like(
            instance=self.object,
            user=self.user
        )
        self.assertNotUserLikes(self.user, self.object)
