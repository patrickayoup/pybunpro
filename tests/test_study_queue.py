from pybunpro import StudyQueue


class TestStudyQueue(object):

    def test_constructor(self, reviews_available, next_review_date,
                         reviews_available_next_hour,
                         reviews_available_next_day):
        study_queue = StudyQueue(reviews_available, next_review_date,
                                 reviews_available_next_hour,
                                 reviews_available_next_day)

        assert study_queue.reviews_available == reviews_available
        assert study_queue.next_review_date == next_review_date
        assert study_queue.reviews_available_next_hour == \
            reviews_available_next_hour
        assert study_queue.reviews_available_next_day == \
            reviews_available_next_day
