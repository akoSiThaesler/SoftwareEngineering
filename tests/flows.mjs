// Browser checks for the prototype: drives every flow, asserts the results and saves screenshots.
// Usage: serve docs/app on a local port, then: BASE_URL=http://localhost:8000/ node tests/flows.mjs <screenshot folder>
// Needs: npm install playwright
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const BASE = (process.env.BASE_URL || 'http://localhost:8000/') + (process.argv[3] || '');
const OUT = process.argv[2];
mkdirSync(OUT, { recursive: true });
const log = [];
const ok = (name, cond, detail) => { log.push((cond ? 'PASS ' : 'FAIL ') + name + (detail ? ' :: ' + detail : '')); };

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, locale: 'de-CH' });
// Full-page captures: the action bar is sticky in the app; lay it out in flow so the picture shows the whole screen in order.
await ctx.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = '.actions,.tabs,.appbar{position:static !important} *{animation:none !important}'; document.head.appendChild(s); }); });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
process.on('uncaughtException', (e) => { console.log(log.join('\n')); console.log('ABORTED: ' + String(e).split('\n')[0]); console.log('page errors: ' + errors.join(' ; ')); process.exit(1); });
const shot = (n) => page.screenshot({ path: OUT + '/' + n + '.png', fullPage: true });
const h1 = () => page.locator('h1').innerText();
const waitH1 = (t) => page.waitForFunction((x) => document.querySelector('h1') && document.querySelector('h1').textContent === x, t, { timeout: 8000 });
const act = (a, extra = '') => page.locator('[data-act="' + a + '"]' + extra).first().click();
const txt = (sel) => page.locator(sel).allInnerTexts();

await page.goto(BASE);
await page.evaluate(() => localStorage.clear());
await page.goto(BASE);
await shot('01-start');
ok('start: suggestion shown', (await txt('#reco')).join(' ').includes('Grösse XL'));

await act('size', '[data-i="0"][data-id="L"]');
await shot('02-box-gewaehlt');
await act('check');
await waitH1('Passt nicht');
const sub3 = (await txt('.hero p')).join(' ');
ok('one L box: not enough + cartons', sub3.includes('4.0 m³') && sub3.includes('etwa 50 Umzugskartons'), sub3);
const acts3 = await txt('[data-act="fix"]');
ok('fixes on the page: smallest first, with reserve second', /Grösse S dazunehmen/.test(acts3[0]) && /keine Reserve/.test(acts3[0]) && /Grösse XL/.test(acts3[1]) && /4\.0 m³ Reserve/.test(acts3[1]), acts3.join(' | '));
ok('result bar has one button', (await txt('.actions button')).length === 1, (await txt('.actions button')).join(' | '));
await shot('03-passt-nicht');

await act('fix', '[data-j="0"]');
await waitH1('Passt, aber knapp');
ok('knapp: note visible', (await txt('.note')).join(' ').includes('Knappes Ergebnis'));
await shot('04-passt-knapp');

await act('toReserve');
await waitH1('Reservierung abschliessen');
await act('reserve');
ok('form: three errors on empty submit', (await txt('.err')).filter(Boolean).length === 3);
await page.fill('[data-f="date"]', '2027-01-15');
await page.fill('[data-f="name"]', 'Julia Beispiel');
await page.fill('[data-f="mail"]', 'julia@beispiel.ch');
await shot('05-reservieren');
await act('reserve');
await waitH1('Reserviert');
ok('booking: number shown', /LR-\d{6}/.test((await txt('main')).join(' ')));
await shot('06-reserviert');

await page.goto(BASE);
const start2 = (await txt('main')).join(' ');
ok('reload: reservation + inputs still there', start2.includes('Deine Reservierung') && start2.includes('letzte Eingabe'));
await shot('07-start-mit-reservierung');

await act('openBooking');
await waitH1('Reserviert');
await act('editForm');
await waitH1('Reservierung ändern');
await page.fill('[data-f="date"]', '2027-02-01');
await act('reserve');
await waitH1('Reserviert');
const m8 = (await txt('main')).join(' ');
ok('edit date: saved + flash', m8.includes('Reservierung geändert') && m8.includes('01.02.2027'));

await act('editBoxes');
await waitH1('Passt dein Hausrat in die Box?');
ok('edit boxes: banner', (await txt('main')).join(' ').includes('Du änderst die Boxen'));
await act('remove', '[data-i="1"]');
await act('size', '[data-i="0"][data-id="XL"]');
await act('check');
await waitH1('Passt');
ok('edit boxes: primary label', (await txt('.actions button'))[0].includes('Änderung übernehmen'));
await act('toReserve');
await waitH1('Reserviert');
const b = await page.evaluate(() => JSON.parse(localStorage.getItem('lagerraum-box-check-reservierung-v1')));
ok('edit boxes: booking updated, same number', b.boxes.length === 1 && b.boxes[0].mode === 'XL' && b.form.date === '2027-02-01', JSON.stringify(b.boxes));

await act('cancelAsk');
await shot('08-stornieren-nachfrage');
await act('cancelNo');
ok('cancel: "Nein" keeps it', await page.evaluate(() => !!localStorage.getItem('lagerraum-box-check-reservierung-v1')));
await act('cancelAsk');
await act('cancelYes');
await waitH1('Passt dein Hausrat in die Box?');
ok('cancel: removed + undo offered', (await txt('main')).join(' ').includes('storniert') && (await page.locator('[data-act="undoCancel"]').count()) === 1 && await page.evaluate(() => !localStorage.getItem('lagerraum-box-check-reservierung-v1')));
await shot('09-storniert');
await act('undoCancel');
await waitH1('Reserviert');
ok('undo: restored', (await txt('main')).join(' ').includes('wiederhergestellt') && await page.evaluate(() => !!localStorage.getItem('lagerraum-box-check-reservierung-v1')));
await act('cancelAsk'); await act('cancelYes');
await waitH1('Passt dein Hausrat in die Box?');

// invalid input
await page.evaluate(() => localStorage.clear());
await page.goto(BASE);
await act('own', '[data-i="0"]');
await page.fill('[data-i="0"][data-k="l"]', '3.0');
await page.fill('[data-i="0"][data-k="b"]', '-2');
await page.fill('[data-i="0"][data-k="h"]', '2.4');
await act('check');
ok('invalid: message names the field', (await txt('#err0')).join('') === 'Breite: Muss grösser als 0 sein', (await txt('#err0')).join(''));
await shot('10-ungueltige-eingabe');

// implausible sizes
await page.fill('[data-i="0"][data-k="l"]', '42');
await page.fill('[data-i="0"][data-k="b"]', '22');
await page.fill('[data-i="0"][data-k="h"]', '22.5');
ok('implausible: hint while typing', (await txt('#warn0')).join('').includes('sehr gross'), (await txt('#warn0')).join(''));
await act('check');
await waitH1('Passt');
const odd = (await txt('.note')).join(' ');
ok('implausible: result note + primary is "Masse prüfen"', odd.includes('Ungewöhnliche Masse') && (await txt('.actions button'))[0].includes('Masse prüfen'), (await txt('.actions button')).join(' | '));
await shot('11-unplausible-masse');

// more space than needed
await act('back');
await act('size', '[data-i="0"][data-id="XL"]');
await act('add');
await act('size', '[data-i="1"][data-id="XL"]');
await act('check');
await waitH1('Passt');
ok('oversize: note + smaller option', (await txt('.note')).join(' ').includes('Deutlich mehr Platz') && (await txt('.note')).join(' ').includes('Kleinere Auswahl prüfen'));
await act('recoFix');
await page.waitForFunction(() => document.querySelectorAll('tr').length === 3, null, { timeout: 8000 });
ok('oversize: one tap switches to suggestion', (await txt('tr')).join(' ').includes('Box 1 (XL)') && (await txt('tr.diff')).join('').includes('4.0'));

// API error via the simulation panel
await page.evaluate(() => localStorage.clear());
await page.goto(BASE + '?test');
await page.click('#simtab');
await page.waitForTimeout(400);
await page.locator('#simApi').check();
await shot('12a-simulation-handy');
await page.click('#simtab');
await page.waitForTimeout(400);
await act('size', '[data-i="0"][data-id="L"]');
await act('check');
await page.waitForSelector('.alert');
ok('api error: message, inputs kept', (await txt('.alert')).join('').includes('Keine Verbindung') && await page.evaluate(() => S.boxes[0].mode === 'L'));
await shot('12-api-fehler');

// shared links: just below, rounding trap
await page.evaluate(() => localStorage.clear());
await page.goto(BASE + '?n=14.0&b=2.0x2.0x2.5_1.8x1.0x2.0');
await waitH1('Passt nicht, knapp');
ok('shared link: 13.6 just below', (await txt('tr.sum')).join('').includes('13.6') && (await txt('.hero p')).join('').includes('0.4 m³, etwa 5 Umzugskartons'), (await txt('.hero p')).join(''));
await shot('13-passt-knapp-nicht');
await page.goto(BASE + '?n=14.0&b=2.0x2.0x2.5_1.99x1.0x2.0');
await waitH1('Passt nicht, knapp');
ok('rounding trap: shows 13.98, not 14.0', (await txt('tr.sum')).join('').includes('13.98') && (await txt('.hero p')).join('').includes('weniger als 1 Umzugskarton'), (await txt('tr.sum')).join(''));
await page.goto(BASE + '?n=14.0&b=2.0x2.0x2.5_2.0x1.0x2.0');
await waitH1('Passt, aber knapp');
ok('exact limit: fits, knapp', (await txt('tr.diff')).join('').includes('0.0'));
await page.goto(BASE + '?n=14.0&b=3.0x2.5x2.4_1.5x1.5x2.0');
await waitH1('Passt');
ok('normal case 22.5', (await txt('tr.sum')).join('').includes('22.5'));

// demo account: optional sign-in, editable profile, prefilled reservation form
await page.evaluate(() => localStorage.clear());
await page.goto(BASE);
ok('need hint in cartons', (await txt('#needHint')).join('') .includes('0.08 m³'), (await txt('#needHint')).join(''));
ok('header: signed out', (await txt('#acct')).join('') === 'Anmelden');
await page.click('#acct');
await waitH1('Anmelden');
await shot('15-konto-anmelden');
await act('login');
await waitH1('Mein Konto');
ok('login: header shows name', (await txt('#acct')).join('').includes('Julia'));
await page.fill('[data-p="mail"]', 'kaputt');
await act('saveProfile');
ok('profile: invalid mail rejected', (await txt('#perr-mail')).join('').includes('gültige'));
await page.fill('[data-p="mail"]', 'j.brandt@beispiel.ch');
await page.fill('[data-p="phone"]', '+49 7621 555 99 99');
await act('saveProfile');
ok('profile: saved + feedback', (await txt('.saved')).join('').includes('gespeichert') && await page.evaluate(() => JSON.parse(localStorage.getItem('lagerraum-box-check-konto-v1')).phone === '+49 7621 555 99 99'));
await shot('16-konto');
await act('closeAccount');
await waitH1('Passt dein Hausrat in die Box?');
await act('size', '[data-i="0"][data-id="XL"]');
await act('check');
await waitH1('Passt');
await act('toReserve');
await waitH1('Reservierung abschliessen');
ok('reserve form prefilled from account', await page.inputValue('[data-f="name"]') === 'Julia Brandt' && await page.inputValue('[data-f="mail"]') === 'j.brandt@beispiel.ch');
await page.fill('[data-f="date"]', '2027-01-15');
await act('reserve');
await waitH1('Reserviert');
const dl = page.waitForEvent('download');
await act('ics');
const file = await dl;
ok('calendar file offered', /^lagerraum-LR-\d{6}\.ics$/.test(file.suggestedFilename()), file.suggestedFilename());
await page.click('#acct');
await waitH1('Mein Konto');
ok('account lists the reservation', (await txt('main')).join(' ').includes('ab 15.01.2027'));
await act('logout');
ok('logout: header back to "Anmelden", booking kept', (await txt('#acct')).join('') === 'Anmelden' && await page.evaluate(() => !!localStorage.getItem('lagerraum-box-check-reservierung-v1')));

// regressions from the three reviews
await page.evaluate(() => localStorage.clear());
await page.goto(BASE);
ok('check disabled until a size is picked', await page.locator('[data-act="check"]').isDisabled() && (await txt('[data-act="check"]')).join('').includes('Zuerst eine Grösse'));
await act('size', '[data-i="0"][data-id="XL"]');
ok('running sum from catalogue', (await txt('#pickSum')).join('').includes('18.0 m³'));
await act('check');
await waitH1('Passt');
await act('back');
await act('size', '[data-i="0"][data-id="S"]');
await page.goBack();
await page.waitForTimeout(200);
ok('browser back after changing boxes: no stale result', await h1() === 'Passt dein Hausrat in die Box?', await h1());
await act('add');
await page.goForward();
await page.waitForTimeout(200);
ok('forward with different box count: no crash', errors.length === 0 && await h1() === 'Passt dein Hausrat in die Box?', errors.join(';'));
await act('remove', '[data-i="1"]');
await act('size', '[data-i="0"][data-id="L"]');
await act('check');
await waitH1('Passt nicht');
await page.evaluate(() => { SIM.apiErr = true; });
await act('fix', '[data-j="0"]');
await page.waitForSelector('.actions .alert');
ok('failed fix: stays on result, selection untouched', await h1() === 'Passt nicht' && await page.evaluate(() => S.boxes.length === 1 && S.boxes[0].mode === 'L') && (await txt('.actions .alert')).join('').includes('unverändert'));
await page.evaluate(() => { SIM.apiErr = false; });
await act('fix', '[data-j="1"]');
await waitH1('Passt');
await act('toReserve');
await page.fill('[data-f="date"]', '2030-01-10');
await page.fill('[data-f="until"]', '2029-01-01');
await page.fill('[data-f="name"]', 'Anna Test');
await page.fill('[data-f="mail"]', 'anna@beispiel.ch');
await act('reserve');
ok('end before start is blocked, summary names it', await h1() === 'Reservierung abschliessen' && (await txt('.actions .alert')).join('').includes('Einlagern bis'), (await txt('.actions .alert')).join(''));
await page.fill('[data-f="until"]', '2030-02-24');
await act('reserve');
await waitH1('Reserviert');
ok('confirmation shows period with days', (await txt('.hero p')).join('').includes('bis 24.02.2030 (45 Tage)'), (await txt('.hero p')).join(''));
await act('editForm');
await page.fill('[data-f="name"]', 'Zed Unsaved');
await page.goBack();
await page.waitForTimeout(200);
ok('back out of edit form shows the saved booking', (await txt('.hero p')).join('').includes('Anna Test'), (await txt('.hero p')).join(''));
await act('editBoxes');
await act('size', '[data-i="0"][data-id="S"]');
await page.goBack();
await page.waitForTimeout(200);
ok('back out of edit boxes shows the saved boxes', (await txt('tr')).join(' ').includes('Box 1 (XL)'), (await txt('tr')).join(' | '));
await act('cancelAsk');
ok('focus moves to the safe answer', await page.evaluate(() => document.activeElement && document.activeElement.dataset.act === 'cancelNo'));
await act('cancelYes');
await page.goto(BASE);
ok('undo survives a reload', (await page.locator('[data-act="undoCancel"]').count()) === 1);
await page.evaluate(() => { localStorage.setItem('lagerraum-box-check-reservierung-v1', '{"resNo":"LR-1"}'); localStorage.setItem('lagerraum-box-check-konto-v1', '{"name":null}'); });
await page.goto(BASE);
ok('malformed stored entries are ignored', errors.length === 0 && await h1() === 'Passt dein Hausrat in die Box?', errors.join(';'));
await page.evaluate(() => localStorage.clear());
await page.goto(BASE);
await act('own', '[data-i="0"]');
await page.fill('[data-i="0"][data-k="h"]', '250');
ok('cm typed as m: hint while typing', (await txt('#warn0')).join('').includes('in Metern'), (await txt('#warn0')).join(''));
await page.fill('[data-i="0"][data-k="l"]', '2.0');
await page.fill('[data-i="0"][data-k="b"]', '2.0');
await page.fill('[data-i="0"][data-k="h"]', '3.499');
await act('check');
ok('three decimals rejected', (await txt('#err0')).join('').includes('zwei Nachkommastellen'), (await txt('#err0')).join(''));
await page.fill('[data-i="0"][data-k="h"]', 'abc');
await page.fill('[data-i="0"][data-k="b"]', '');
ok('every bad field is named', /Breite.*Höhe/.test((await txt('#err0')).join('')), (await txt('#err0')).join(''));
await page.fill('#need', '1e2');
await act('check');
ok('1e2 is not a number here', (await txt('#needErr')).join('').includes('Bitte eine Zahl'), (await txt('#needErr')).join(''));
await page.evaluate(() => localStorage.clear());
await page.goto(BASE + '?n=14.0&b=2.0x2.0x2.5_2.0x1.1x2.0');
await waitH1('Passt, aber knapp');
ok('just above 14.4: knapp, more-reserve option, bulky hint', (await txt('tr.diff')).join('').includes('0.4') && (await page.locator('[data-act="fix"]').count()) >= 1 && (await txt('.note')).join('').includes('Sperrige'));
await page.setViewportSize({ width: 320, height: 700 });
ok('no horizontal scroll at 320', await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
await page.setViewportSize({ width: 390, height: 844 });

// overflow check at phone width, then the desktop layout with the simulation panel
ok('no horizontal scroll at 390', await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
await page.setViewportSize({ width: 1280, height: 800 });
await page.evaluate(() => localStorage.clear());
await page.goto(BASE + '?test');
await page.screenshot({ path: OUT + '/14-simulation-seitenleiste.png' });

ok('no page errors', errors.length === 0, errors.join(' ; '));
console.log(log.join('\n'));
await browser.close();
