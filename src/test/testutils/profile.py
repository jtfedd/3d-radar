import linecache
import os
import tracemalloc


def start() -> None:
    tracemalloc.start()


def stop() -> None:
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    displayTop(snapshot)


def displayTop(
    snapshot: tracemalloc.Snapshot, keyType: str = "lineno", limit: int = 3
) -> None:
    snapshot = snapshot.filter_traces(
        (
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        )
    )
    topStats = snapshot.statistics(keyType)

    print(f"Top {limit} lines")
    for index, stat in enumerate(topStats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print(f"#{index}: {filename}:{frame.lineno}: {(stat.size / 1024):.1f} KiB")
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print(f"    {line}")

    other = topStats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print(f"{len(other)} other: {(size / 1024):.1f} KiB")

    total = sum(stat.size for stat in topStats)
    print(f"Total allocated size: {(total / 1024):.1f} KiB")
