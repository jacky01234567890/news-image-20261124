// One image of Tuesday 24 November 2026 (Node 22, standard library only).
// The front page is drawn by tools/make_image.py and committed here as
// entry.png; this program just copies it to the grader's output path.
// The gate wants a whole PNG or JPEG of at most 1 MiB and 1024 by 1024,
// and the judge sees exactly the bytes copied.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'),
);
