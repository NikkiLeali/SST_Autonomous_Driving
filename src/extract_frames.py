import cv2
from pathlib import Path


def extract_frames(video_path: Path, out_dir: Path, num_frames: int = 10) -> list[Path]:
    cap = cv2.VideoCapture(str(video_path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    assert total > 0, f"No frames found in video: {video_path}"

    num_frames = min(num_frames, total)
    frame_indices = [round(i * (total - 1) / max(num_frames - 1, 1)) for i in range(num_frames)]

    out_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []

    for n, idx in enumerate(frame_indices, start=1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if not ok:
            continue

        frame_path = out_dir / f"frame_{n:02d}.png"
        cv2.imwrite(str(frame_path), frame)
        frame_paths.append(frame_path)

    cap.release()
    return frame_paths


if __name__ == "__main__":
    # TEST VIDEO PATH
    video_path = Path("data/raw/sample_construction_drive.mp4")
    out_dir = Path("data/frames") / video_path.stem

    frames = extract_frames(video_path, out_dir, num_frames=10)
    print(f"Extracted {len(frames)} frames -> {out_dir}")
