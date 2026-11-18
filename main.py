
from workflow.graph import run_workflow


def main():

    print("=" * 50)
    print("   SELF-EVALUATING AI LESSON GENERATOR")
    print("=" * 50)

    topic = input("\nEnter a learning topic: ").strip()

    if not topic:
        print("Please enter a valid topic.")
        return

    print("\nStarting AI agent workflow...")

    result = run_workflow(topic)

    print("\n" + "=" * 50)
    print("             FINAL REPORT")
    print("=" * 50)

    print(f"\nTopic: {result['topic']}")
    print(f"Status: {result['status']}")
    print(f"Regenerations: {result['retry_count']}")

    print("\n--- REJECTION LOG ---")

    if result["rejection_log"]:
        for log in result["rejection_log"]:
            print(f"\nAttempt: {log['attempt']}")

            for failure in log["failed_checks"]:
                print(f"- {failure}")
    else:
        print("No rejections.")

    if result["status"] == "PASS":

        print("\n--- FINAL APPROVED LESSON ---")
        print(result["lesson"])

    else:
        print("\nLesson was rejected.")
        print("Maximum retry limit reached.")

    print("\n--- FINAL EVALUATION ---")

    for name, check in result["evaluation"].items():
        print(f"{name}: {check['status']}")
        print(f"Reason: {check['reason']}")


if __name__ == "__main__":
    main()
