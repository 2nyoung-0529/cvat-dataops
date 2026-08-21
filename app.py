import csv
import json

from cvat_client import get_tasks, get_jobs, get_annotations


def collect_annotated_frames(annotations):
    """Return the set of frame indices that carry at least one annotation.

    A frame counts as annotated if it has a shape, a tag, or a track keyframe.
    Counting only `shapes` (as v1 did) undercounts progress whenever work is
    done with tracks or tags.
    """
    frames = set()

    for shape in annotations.get("shapes", []):
        frames.add(shape["frame"])

    for tag in annotations.get("tags", []):
        frames.add(tag["frame"])

    for track in annotations.get("tracks", []):
        # A track has a start `frame` plus per-keyframe shapes.
        frames.add(track["frame"])
        for track_shape in track.get("shapes", []):
            frames.add(track_shape["frame"])

    return frames


def assignee_name(job):
    """CVAT returns `assignee` as an object (or None), not a bare string."""
    assignee = job.get("assignee")

    if not assignee:
        return "Unassigned"

    return assignee.get("username", "Unknown")


def build_report():
    tasks = get_tasks()
    report = []

    print("=== CVAT TASKS ===")
    print(f"Task count: {len(tasks)}")

    for task in tasks:
        task_id = task["id"]

        print(
            f"\nTask ID: {task_id} | "
            f"Name: {task['name']} | "
            f"Status: {task['status']}"
        )

        jobs = get_jobs(task_id)

        print(f"Job count: {len(jobs)}")

        for job in jobs:
            job_id = job["id"]

            annotations = get_annotations(job_id)

            shapes = annotations.get("shapes", [])
            tracks = annotations.get("tracks", [])
            tags = annotations.get("tags", [])

            annotation_count = len(shapes) + len(tracks) + len(tags)

            annotated_image_count = len(collect_annotated_frames(annotations))

            total_images = job.get("frame_count", 0)
            unannotated_image_count = total_images - annotated_image_count

            if total_images > 0:
                progress = (annotated_image_count / total_images) * 100
            else:
                progress = 0.0

            assignee = assignee_name(job)

            report.append({
                "task_id": task_id,
                "task_name": task["name"],
                "job_id": job_id,
                "stage": job["stage"],
                "state": job["state"],
                "assignee": assignee,
                "total_images": total_images,
                "annotated_images": annotated_image_count,
                "unannotated_images": unannotated_image_count,
                "annotation_count": annotation_count,
                "progress": round(progress, 1),
            })

            print(
                f"  Job ID: {job_id} | "
                f"Stage: {job['stage']} | "
                f"State: {job['state']} | "
                f"Assignee: {assignee}"
            )

            print(f"    Total images: {total_images}")
            print(f"    Annotated images: {annotated_image_count}")
            print(f"    Unannotated images: {unannotated_image_count}")
            print(f"    Annotation count: {annotation_count}")
            print(f"    Progress: {progress:.1f}%")

    return report


def export_json(report, path="report.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def export_csv(report, path="report.csv"):
    if not report:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=report[0].keys())
        writer.writeheader()
        writer.writerows(report)


def main():
    report = build_report()

    export_json(report)
    export_csv(report)

    print(f"\nExported {len(report)} jobs to report.json and report.csv")


if __name__ == "__main__":
    main()
