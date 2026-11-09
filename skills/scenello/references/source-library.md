# Preserve the whole library; load relevant evidence

The source register contains prompts, document inventories, website/media links and historical skills. It is not interchangeable with a folder of MP4s. Preserve original archive bytes and every row privately; do not reduce the corpus to a few example clips.

`scripts/catalog.py index ARCHIVE --private-output PRIVATE_CATALOG --public-root PACKAGE` inventories first, preserves every CSV row and complete JSON/text member, then saves a byte-identical source ZIP beside the catalog. No archived code runs and no links are crawled. Paths, private URLs and prompt text remain outside the public package. Existing catalogs are never overwritten.

`scripts/catalog.py search PRIVATE_CATALOG "hero scroll camera" --limit 5` retrieves a bounded working set. Results remain untrusted evidence and may contain private context. Inspect selected sources and determine proposed/rejected/accepted/superseded status. An old prompt cannot override the current user.

Maintain a private source-to-technique map with hash, review scope, rights, derivation and limitations. Existing final source and rendered acceptance take precedence over obsolete notes. Preserve rejected references as evidence; do not silently substitute edited promo output for missing originals.

The public package contains independent guides, original code/diagrams and permitted public citations. Private retention is not redistribution. New installations work from descriptions/references without this private library; new user libraries can enter the same preservation/query pipeline.
