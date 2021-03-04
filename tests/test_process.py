from src.process import get_stats

def test_get_stats(mocker):
    logger = mocker.Mock("logger")
    msgs = [{"type": "pageview", "value": 1.1, "occurred_at": "2021-03-03 10:33:38"}, 
            {"type": "pageview", "value": 1, "occurred_at": "2021-03-03 10:33:38"}]
    expected = [{"type": "pageview", "count": 2, "sum": 2.1}]
    actual = get_stats(msgs, logger)
    assert actual == expected