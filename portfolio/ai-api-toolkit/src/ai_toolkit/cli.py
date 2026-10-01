from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys

from .config import Settings
from .service import generate, save_response


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-toolkit",
        description="Generate text through Gemini or a local mock provider.",
    )
    parser.add_argument("prompt", help="Prompt sent to the provider")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--mock", action="store_true", help="Avoid network calls")
    parser.add_argument("--save", type=Path, help="Save response as JSON")
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Write application logs to this file",
    )
    return parser


def configure_logging(log_file: Path | None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=handlers,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.log_file)

    try:
        settings = Settings.from_environment(
            model=args.model,
            timeout=args.timeout,
        )

        logging.info("Starting provider=%s model=%s", "mock" if args.mock else "gemini", settings.model)
        response = generate(
            args.prompt,
            api_key=settings.api_key,
            model=settings.model,
            timeout=settings.timeout,
            mock=args.mock,
        )

        print(response.text)

        if args.save:
            save_response(response, args.prompt, args.save)
            logging.info("Saved response to %s", args.save)

        return 0

    except (ValueError, OSError, RuntimeError) as exc:
        logging.error("%s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
