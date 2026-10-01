from pathlib import Path

from filepilot.organizer import category_for, plan_organization


def test_category_for_known_extension():
    assert category_for(Path("photo.JPG")) == "images"
    assert category_for(Path("track.mp3")) == "audio"
    assert category_for(Path("unknown.xyz")) == "other"


def test_plan_organization(tmp_path: Path):
    (tmp_path / "photo.jpg").write_bytes(b"image")
    (tmp_path / "song.mp3").write_bytes(b"audio")
    operations = plan_organization(tmp_path)
    destinations = {op.destination.relative_to(tmp_path).as_posix() for op in operations}
    assert destinations == {"images/photo.jpg", "audio/song.mp3"}
