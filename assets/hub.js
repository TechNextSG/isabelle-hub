(() => {
  const q = document.getElementById('q');
  const tabs = [...document.querySelectorAll('.ix-tab')];
  const groups = [...document.querySelectorAll('.ix-group')];
  const empty = document.getElementById('empty');
  let tab = 'all';

  const norm = s => (s || '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '');

  function apply() {
    const t = norm(q.value.trim());
    let shown = 0;
    groups.forEach(g => {
      let n = 0;
      const inTab = tab === 'all' || g.dataset.g === tab;
      g.querySelectorAll('.ix-card').forEach(c => {
        let hit = !t || norm(c.dataset.words).includes(t);
        // a search that matches a page inside a website keeps that card and opens its list on the match
        const pages = c.querySelector('.ix-pages');
        if (pages) {
          let ph = 0;
          pages.querySelectorAll('li').forEach(li => {
            const m = !t || hit || norm(li.textContent).includes(t);
            li.hidden = !m; if (m) ph++;
          });
          if (t && !hit && ph) { hit = true; pages.open = true; }
          pages.querySelector('.ix-pc').textContent = t && ph !== pages.querySelectorAll('li').length ? `${ph} matching` : `${pages.querySelectorAll('li').length} pages`;
        }
        const on = inTab && hit;
        c.hidden = !on; if (on) n++;
      });
      g.hidden = !n; shown += n;
    });
    empty.hidden = shown > 0;
  }

  q.addEventListener('input', apply);
  tabs.forEach(b => b.addEventListener('click', () => {
    tab = b.dataset.tab;
    tabs.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    apply();
  }));
  document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); }
    if (e.key === 'Escape' && document.activeElement === q) { q.value = ''; apply(); }
  });

  // copy link
  document.querySelectorAll('.ix-copy').forEach(b => b.addEventListener('click', async () => {
    const url = b.dataset.url, label = b.querySelector('.ix-cl');
    try { await navigator.clipboard.writeText(url); }
    catch { const i = document.createElement('input'); i.value = url; document.body.append(i); i.select(); document.execCommand('copy'); i.remove(); }
    label.textContent = 'Copied'; b.classList.add('is-done');
    setTimeout(() => { label.textContent = 'Copy link'; b.classList.remove('is-done'); }, 1600);
  }));
})();
