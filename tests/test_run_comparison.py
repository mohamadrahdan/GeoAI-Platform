from core.evaluation.comparison import RunMetrics, compare_runs, best_run

def test_compare_runs_sorts_correctly():
    runs = [
        RunMetrics(trace_id="a", model_name="m", version="1", metrics={"iou": 0.5}),
        RunMetrics(trace_id="b", model_name="m", version="1", metrics={"iou": 0.7}),
        RunMetrics(trace_id="c", model_name="m", version="1", metrics={"iou": 0.6}),
    ]
    sorted_runs = compare_runs(runs, metric_name="iou")
    assert sorted_runs[0].trace_id == "b"
    assert sorted_runs[-1].trace_id == "a"

def test_best_run_returns_correct_one():
    runs = [
        RunMetrics(trace_id="a", model_name="m", version="1", metrics={"dice": 0.3}),
        RunMetrics(trace_id="b", model_name="m", version="1", metrics={"dice": 0.8}),
    ]
    best = best_run(runs, metric_name="dice")
    assert best is not None
    assert best.trace_id == "b"