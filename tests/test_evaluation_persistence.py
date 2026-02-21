from pathlib import Path
from core.evaluation.comparison import RunMetrics
from core.evaluation.persistence import EvaluationStore

def test_save_and_load_run(tmp_path: Path):
    store = EvaluationStore(root_dir=tmp_path)
    run = RunMetrics(
        trace_id="abc123",
        model_name="test_model",
        version="1.0.0",
        metrics={"iou": 0.8, "dice": 0.85},
    )
    file_path = store.save(run)
    assert file_path.exists()
    loaded = store.load_all("test_model", "1.0.0")
    assert len(loaded) == 1
    assert loaded[0].trace_id == "abc123"
    assert loaded[0].metrics["iou"] == 0.8