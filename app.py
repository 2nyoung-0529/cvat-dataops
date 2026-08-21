from cvat_client import get_tasks, get_jobs, get_annotations


def main():
    tasks = get_tasks()

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

            annotation_count = (
                len(shapes)
                + len(tracks)
                + len(tags)
            )

            annotated_frames = {
                shape["frame"]
                for shape in shapes
            }

            annotated_image_count = len(annotated_frames)

            total_images = job.get("frame_count", 0)
            unannotated_image_count = total_images - annotated_image_count

            if total_images > 0:
                progress = (
                    annotated_image_count / total_images
                ) * 100
            else:
                progress = 0.0

            print(
                f"  Job ID: {job_id} | "
                f"Stage: {job['stage']} | "
                f"State: {job['state']} | "
                f"Assignee: {job['assignee']}"
            )

            print(f"    Total images: {total_images}")
            print(f"    Annotated images: {annotated_image_count}")
            print(f"    Unannotated images: {unannotated_image_count}")
            print(f"    Annotation count: {annotation_count}")
            print(f"    Progress: {progress:.1f}%")


if __name__ == "__main__":
    main()