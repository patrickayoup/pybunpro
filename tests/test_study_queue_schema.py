from pybunpro import StudyQueueSchema


class TestStudyQueueSchema(object):

    def test_dump(self, study_queue, study_queue_dict):
        schema = StudyQueueSchema()
        result, errors = schema.dump(study_queue)

        assert errors == dict()
        assert result == study_queue_dict

    def test_load(self, study_queue, study_queue_dict):
        schema = StudyQueueSchema()
        result, errors = schema.load(study_queue_dict)

        assert errors == dict()
        assert result == study_queue
