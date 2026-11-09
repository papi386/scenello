import {test} from 'node:test';
import assert from 'node:assert/strict';
import {anchorTransform, projectAnchor} from '../skills/scenello/assets/contact-anchor.mjs';

test('independently annotated asset anchors meet across widths, scales and rotations', () => {
  for (const width of [320, 360, 390, 768, 1440, 2560]) {
    const target = [width * .5, width * .3];
    for (const [anchor, rotation] of [[[.91, .28], -8], [[.08, .52], 12]]) {
      for (const scale of [.5, 1, 1.6]) {
        const size = [width * .7, width * .4];
        const {matrix} = anchorTransform({anchor, size, contact: target, rotation, scale});
        const actual = projectAnchor(matrix, anchor, size);
        assert.ok(Math.hypot(actual[0] - target[0], actual[1] - target[1]) < 1e-9);
      }
    }
  }
});

test('invalid scene metrics fail explicitly', () => {
  assert.throws(() => anchorTransform({anchor:[2, .5], size:[100, 50], contact:[0, 0]}), RangeError);
  assert.throws(() => anchorTransform({anchor:[.2, .5], size:[0, 50], contact:[0, 0]}), RangeError);
});
