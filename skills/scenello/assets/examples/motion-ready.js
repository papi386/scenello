// Reserve the enhanced scene's layout before first paint; failure leaves static content.
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && !new URLSearchParams(location.search).has('static')) document.documentElement.classList.add('motion');
