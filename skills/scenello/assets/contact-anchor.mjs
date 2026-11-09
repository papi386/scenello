/** Original normalized-anchor helper. No anatomy, asset rights or visual-quality claims. */
export function anchorTransform({anchor, size, contact, rotation = 0, scale = 1}) {
  if (![...anchor, ...size, ...contact, rotation, scale].every(Number.isFinite) ||
      anchor.length !== 2 || size.length !== 2 || contact.length !== 2 ||
      anchor.some(v => v < 0 || v > 1) || size.some(v => v <= 0) || scale <= 0) {
    throw new RangeError('Finite dimensions, normalized anchor and positive scale required');
  }
  const angle = rotation * Math.PI / 180;
  const a = scale * Math.cos(angle), b = scale * Math.sin(angle);
  const c = -b, d = a, x = anchor[0] * size[0], y = anchor[1] * size[1];
  const tx = contact[0] - a * x - c * y;
  const ty = contact[1] - b * x - d * y;
  return {matrix: [a, b, c, d, tx, ty], css: `matrix(${a},${b},${c},${d},${tx},${ty})`};
}

export function projectAnchor(matrix, anchor, size) {
  const [a, b, c, d, tx, ty] = matrix;
  const x = anchor[0] * size[0], y = anchor[1] * size[1];
  return [a * x + c * y + tx, b * x + d * y + ty];
}
