import os
import time

from eval_common import load_evaldata, read_document

from trafilatura import bare_extraction

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    evaldata = load_evaldata(HERE)
    total = 0
    correct = 0
    start = time.time()

    for item in evaldata.values():
        if not item.get("file") or not item.get("author"):
            continue
        author_gold = item["author"]
        if isinstance(author_gold, list):  # match how trafilatura joins multiple authors
            author_gold = "; ".join(author_gold)
        htmlbinary = read_document(HERE, item["file"])
        if htmlbinary is None:
            continue
        total += 1
        try:
            result = bare_extraction(htmlbinary, output_format="python", with_metadata=True)
        except Exception as exc:  # a crash counts as a miss, like run_and_count
            print(f"{item['file']}: {type(exc).__name__}: {exc}")
            continue
        if result is None:
            continue
        if result.author == author_gold:
            correct += 1

    print("exec. time:", f"{time.time() - start:.2f}")
    print("total, correct, percentage:")
    percentage = correct / total * 100 if total else 0.0
    print(total, correct, f"{percentage:.2f}")


if __name__ == "__main__":
    main()
