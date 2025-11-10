import json
import argparse
from extractors.linkedin_parser import LinkedInExtractor
from outputs.json_exporter import JSONExporter

def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Post Engagement Scraper (No cookies, public data only)"
    )
    parser.add_argument("--url", required=True, help="LinkedIn post URL")
    parser.add_argument("--type", choices=["likers", "commenters"], required=True)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--output", default="data/output.json")

    args = parser.parse_args()

    extractor = LinkedInExtractor(args.url, args.type)
    results = extractor.fetch_all(iterations=args.iterations, start_index=args.start)

    JSONExporter.export(results, args.output)
    print(f"[+] Exported {len(results)} records to {args.output}")

if __name__ == "__main__":
    main()