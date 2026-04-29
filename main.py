import logging
from log import info

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    logging.info("agentcore-iam-script")
    info({"project_name": "agentcore-iam-script"})


if __name__ == "__main__":
    main()
