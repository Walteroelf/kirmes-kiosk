/*
 * Bilder für die Kinder auf einem Gerät (statt Namen): schlichte, flache Zeichnungen im Stil der App.
 * Jedes Kind tippt beim Start auf sein Bild. farbe = Hintergrund der Kachel.
 */
'use strict';
const KinderSymbole = (() => {
  const D = '#1d3a5c';   // dunkle Linien (statt Schwarz)
  const s = inhalt => `<svg viewBox="0 0 64 64" aria-hidden="true">${inhalt}</svg>`;
  const liste = {
    igel: { name: 'Igel', farbe: '#fde7c8', svg: s(
      `<polygon points="8,46 10,34 15,38 17,25 23,33 27,20 32,31 37,20 41,32 46,26 48,40 50,46" fill="#7a4b2a"/>` +
      `<path d="M8 46Q10 34 26 32Q44 30 50 40L58 46Q56 52 48 52L14 52Q8 52 8 46Z" fill="#a0673a"/>` +
      `<path d="M42 36Q52 36 58 46Q52 50 44 48Z" fill="#e8c39a"/>` +
      `<circle cx="48" cy="41" r="2.2" fill="${D}"/><circle cx="58" cy="46" r="2.6" fill="${D}"/>` +
      `<rect x="16" y="50" width="6" height="6" rx="2" fill="#7a4b2a"/><rect x="36" y="50" width="6" height="6" rx="2" fill="#7a4b2a"/>`) },
    rakete: { name: 'Rakete', farbe: '#dbeefa', svg: s(
      `<path d="M25 46Q32 64 39 46Z" fill="#ffd200"/>` +
      `<path d="M22 32L12 47L23 45Z" fill="#f39325"/><path d="M42 32L52 47L41 45Z" fill="#f39325"/>` +
      `<path d="M32 5C43 14 45 29 42 46L22 46C19 29 21 14 32 5Z" fill="#fff" stroke="${D}" stroke-width="2.5" stroke-linejoin="round"/>` +
      `<path d="M32 5C36 8 38.6 11.5 40.2 16L23.8 16C25.4 11.5 28 8 32 5Z" fill="#f39325"/>` +
      `<circle cx="32" cy="26" r="5.5" fill="#9fd3f0" stroke="${D}" stroke-width="2.5"/>`) },
    blume: { name: 'Blume', farbe: '#e6f4e0', svg: s(
      `<path d="M32 34V58" stroke="#2e7d32" stroke-width="4" stroke-linecap="round"/>` +
      `<path d="M32 49Q22 41 16 47Q23 55 32 51Z" fill="#4caf50"/><path d="M32 45Q41 37 48 42Q41 50 32 47Z" fill="#4caf50"/>` +
      [[42, 24], [37, 32.7], [27, 32.7], [22, 24], [27, 15.3], [37, 15.3]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="8" fill="#f48fb1"/>`).join('') +
      `<circle cx="32" cy="24" r="6.5" fill="#ffd200"/>`) },
    sonne: { name: 'Sonne', farbe: '#fff6cc', svg: s(
      Array.from({ length: 8 }, (_, i) => { const w = i * Math.PI / 4, c = Math.cos(w), n = Math.sin(w);
        return `<path d="M${(32 + 18 * c).toFixed(1)} ${(32 + 18 * n).toFixed(1)}L${(32 + 27 * c).toFixed(1)} ${(32 + 27 * n).toFixed(1)}" stroke="#f39325" stroke-width="4.5" stroke-linecap="round"/>`; }).join('') +
      `<circle cx="32" cy="32" r="13.5" fill="#ffd200"/>` +
      `<circle cx="27" cy="30" r="1.8" fill="${D}"/><circle cx="37" cy="30" r="1.8" fill="${D}"/><path d="M26.5 35.5Q32 40 37.5 35.5" fill="none" stroke="${D}" stroke-width="2" stroke-linecap="round"/>`) },
    fisch: { name: 'Fisch', farbe: '#dbeefa', svg: s(
      `<path d="M44 32L59 19L59 45Z" fill="#3d9ad6"/>` +
      `<ellipse cx="29" cy="32" rx="20" ry="13" fill="#9fd3f0" stroke="#3d9ad6" stroke-width="2.5"/>` +
      `<path d="M31 20Q37 32 31 44" fill="none" stroke="#3d9ad6" stroke-width="2.5"/>` +
      `<circle cx="18" cy="29" r="2.8" fill="${D}"/>` +
      `<circle cx="7" cy="17" r="2.6" fill="none" stroke="#3d9ad6" stroke-width="1.8"/><circle cx="11" cy="9" r="1.9" fill="none" stroke="#3d9ad6" stroke-width="1.6"/>`) },
    auto: { name: 'Auto', farbe: '#e6f4e0', svg: s(
      `<path d="M7 41V33Q7 30 10 30H18L24 21Q25 19.5 27 19.5H42Q44 19.5 45 21L51 30H54Q57 30 57 33V41Q57 43 55 43H9Q7 43 7 41Z" fill="#4caf50"/>` +
      `<path d="M21 30L26 23H33V30Z" fill="#dbeefa"/><path d="M36 23H43L48 30H36Z" fill="#dbeefa"/>` +
      `<rect x="52.5" y="33" width="4.5" height="3.5" rx="1" fill="#ffd200"/>` +
      `<circle cx="19" cy="43" r="6.5" fill="${D}"/><circle cx="19" cy="43" r="2.6" fill="#d8dee6"/>` +
      `<circle cx="45" cy="43" r="6.5" fill="${D}"/><circle cx="45" cy="43" r="2.6" fill="#d8dee6"/>`) },
    katze: { name: 'Katze', farbe: '#fde7c8', svg: s(
      `<path d="M13 28L15 7L29 18Z" fill="#f39325"/><path d="M51 28L49 7L35 18Z" fill="#f39325"/>` +
      `<path d="M17 21L18 13L24 18Z" fill="#fbc8a4"/><path d="M47 21L46 13L40 18Z" fill="#fbc8a4"/>` +
      `<ellipse cx="32" cy="35" rx="20" ry="18" fill="#f39325"/>` +
      `<ellipse cx="32" cy="42" rx="8.5" ry="6.5" fill="#fde7c8"/>` +
      `<ellipse cx="24" cy="31" rx="2.6" ry="3.6" fill="${D}"/><ellipse cx="40" cy="31" rx="2.6" ry="3.6" fill="${D}"/>` +
      `<path d="M29.5 38H34.5L32 41Z" fill="#c76f0a"/>` +
      `<path d="M8 38L21 40M8 44L21 43M56 38L43 40M56 44L43 43" stroke="${D}" stroke-width="1.6" stroke-linecap="round"/>`) },
    baum: { name: 'Baum', farbe: '#e6f4e0', svg: s(
      `<rect x="28" y="36" width="8" height="21" rx="2" fill="#a0673a"/>` +
      `<circle cx="20" cy="31" r="11" fill="#4caf50"/><circle cx="44" cy="31" r="11" fill="#4caf50"/><circle cx="32" cy="21" r="14" fill="#5cbf60"/>` +
      `<circle cx="24" cy="25" r="2.6" fill="#f39325"/><circle cx="40" cy="20" r="2.6" fill="#f39325"/><circle cx="37" cy="33" r="2.6" fill="#f39325"/>`) },
    stern: { name: 'Stern', farbe: '#fff6cc', svg: s(
      `<polygon points="32,9 37.9,24.9 54.8,25.6 41.5,36.1 46.1,52.4 32,43 17.9,52.4 22.5,36.1 9.2,25.6 26.1,24.9" fill="#ffd200" stroke="#f39325" stroke-width="2.5" stroke-linejoin="round"/>`) },
    schiff: { name: 'Schiff', farbe: '#dbeefa', svg: s(
      `<rect x="31" y="9" width="3" height="31" fill="#7a4b2a"/>` +
      `<path d="M35 11L51 36H35Z" fill="#fff" stroke="${D}" stroke-width="2" stroke-linejoin="round"/><path d="M30 15L15 36H30Z" fill="#f39325"/>` +
      `<path d="M9 40H55L48 51H16Z" fill="#a0673a"/>` +
      `<path d="M3 52Q9 48 15 52T27 52T39 52T51 52T63 52V61H3Z" fill="#3d9ad6"/>`) },
    apfel: { name: 'Apfel', farbe: '#e6f4e0', svg: s(
      `<path d="M32 22C22 14 8 20 10 36C12 50 22 58 32 54C42 58 52 50 54 36C56 20 42 14 32 22Z" fill="#7cc242"/>` +
      `<path d="M32 22Q32 14 36 9" stroke="#7a4b2a" stroke-width="3" fill="none" stroke-linecap="round"/>` +
      `<path d="M35 14Q44 6 51 12Q43 19 35 14Z" fill="#2e7d32"/>` +
      `<ellipse cx="21" cy="33" rx="3" ry="6.5" fill="#fff" opacity=".5"/>`) },
    eule: { name: 'Eule', farbe: '#ece6f6', svg: s(
      `<path d="M15 22L17 7L27 16Z" fill="#9575cd"/><path d="M49 22L47 7L37 16Z" fill="#9575cd"/>` +
      `<ellipse cx="32" cy="36" rx="18" ry="22" fill="#9575cd"/>` +
      `<ellipse cx="32" cy="45" rx="11" ry="11.5" fill="#d1c4e9"/>` +
      `<circle cx="24" cy="28" r="7.5" fill="#fff"/><circle cx="40" cy="28" r="7.5" fill="#fff"/>` +
      `<circle cx="24" cy="28" r="3.4" fill="${D}"/><circle cx="40" cy="28" r="3.4" fill="${D}"/>` +
      `<path d="M29 34H35L32 39.5Z" fill="#f39325"/>` +
      `<ellipse cx="26" cy="58" rx="3.5" ry="2.2" fill="#f39325"/><ellipse cx="38" cy="58" rx="3.5" ry="2.2" fill="#f39325"/>`) },
  };
  return { liste, folge: Object.keys(liste) };
})();
