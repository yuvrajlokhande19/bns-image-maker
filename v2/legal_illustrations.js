/**
 * Context-Aware Editorial Sketchbook Legal Illustrations for BNS 2023 Infographic Cards.
 * ViewBox: 0 0 286 122 across all motifs so every card stays balanced and zero text clips.
 */

const PALETTES = [
  // Card 1: Classic Navy & Gold
  {
    ink: '#0E2944',
    accent: '#E8A918',
    fillSoft: '#FBE8A6',
    fillMid: '#DDE8F6',
    tint: '#2D609B',
    alert: '#C94A38',
    pillBg: '#0E2944',
    pillText: '#F8D468',
  },
  // Card 2: Deep Teal & Sage Mint
  {
    ink: '#0F3633',
    accent: '#2B8E82',
    fillSoft: '#CBECE3',
    fillMid: '#FBECC2',
    tint: '#1C6E64',
    alert: '#D15B47',
    pillBg: '#175B53',
    pillText: '#E8FAF4',
  },
  // Card 3: Royal Indigo & Plum Gold
  {
    ink: '#291D48',
    accent: '#7D58B2',
    fillSoft: '#E6DAF8',
    fillMid: '#FCE8B8',
    tint: '#5D408D',
    alert: '#C74463',
    pillBg: '#46306E',
    pillText: '#F5EAFF',
  },
];

function banner(x, y, w, h, text, p, fillOverride, textOverride, fontSize = 9.5) {
  const bg = fillOverride || p.pillBg;
  const fg = textOverride || p.pillText;
  return `
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2}" fill="${bg}" stroke="${p.ink}" stroke-width="1.4"/>
    <text x="${x + w / 2}" y="${y + h / 2 + 3.4}" font-family="'Poppins', Arial, sans-serif" font-size="${fontSize}" font-weight="700" letter-spacing="0.4" fill="${fg}" text-anchor="middle">${text}</text>
  `;
}

function drawScales(cx, topY, armHalfW, panDrop, p) {
  return `
    <line x1="${cx}" y1="${topY - 8}" x2="${cx}" y2="${topY + panDrop + 12}" stroke="${p.ink}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M ${cx - armHalfW} ${topY} Q ${cx} ${topY - 5} ${cx + armHalfW} ${topY}" fill="none" stroke="${p.ink}" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="${cx}" cy="${topY - 3}" r="3.8" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.5"/>
    <line x1="${cx - armHalfW}" y1="${topY}" x2="${cx - armHalfW - 11}" y2="${topY + panDrop}" stroke="${p.ink}" stroke-width="1.4"/>
    <line x1="${cx - armHalfW}" y1="${topY}" x2="${cx - armHalfW + 11}" y2="${topY + panDrop}" stroke="${p.ink}" stroke-width="1.4"/>
    <path d="M ${cx - armHalfW - 14} ${topY + panDrop} Q ${cx - armHalfW} ${topY + panDrop + 10} ${cx - armHalfW + 14} ${topY + panDrop} Z" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="1.5"/>
    <line x1="${cx + armHalfW}" y1="${topY}" x2="${cx + armHalfW - 11}" y2="${topY + panDrop}" stroke="${p.ink}" stroke-width="1.4"/>
    <line x1="${cx + armHalfW}" y1="${topY}" x2="${cx + armHalfW + 11}" y2="${topY + panDrop}" stroke="${p.ink}" stroke-width="1.4"/>
    <path d="M ${cx + armHalfW - 14} ${topY + panDrop} Q ${cx + armHalfW} ${topY + panDrop + 10} ${cx + armHalfW + 14} ${topY + panDrop} Z" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="1.5"/>
  `;
}

function drawGavel(cx, cy, angleDeg, p) {
  return `
    <g transform="translate(${cx},${cy}) rotate(${angleDeg})">
      <rect x="6" y="-4" width="44" height="8" rx="4" fill="#B87A44" stroke="${p.ink}" stroke-width="1.7"/>
      <rect x="-15" y="-13" width="26" height="26" rx="4" fill="#9A5C2A" stroke="${p.ink}" stroke-width="1.9"/>
      <rect x="-18" y="-15" width="7" height="30" rx="2.5" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.6"/>
      <rect x="7" y="-15" width="7" height="30" rx="2.5" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.6"/>
    </g>
    <path d="M ${cx - 32} ${cy + 23} L ${cx + 22} ${cy + 23} L ${cx + 26} ${cy + 31} L ${cx - 36} ${cy + 31} Z" fill="#C98A4E" stroke="${p.ink}" stroke-width="1.7" stroke-linejoin="round"/>
  `;
}

const MOTIFS = {
  // Section 1: Title, Commencement & Jurisdiction across India + Extra-territorial
  title_commencement: (p) => `
    <g>
      <!-- Gazetted Code Book (Left) -->
      <rect x="24" y="16" width="84" height="88" rx="7" fill="${p.pillBg}" stroke="${p.ink}" stroke-width="2" transform="rotate(-3 66 60)"/>
      <rect x="33" y="23" width="66" height="74" rx="4" fill="none" stroke="${p.accent}" stroke-width="1.4" transform="rotate(-3 66 60)"/>
      <text x="66" y="45" font-family="'Poppins',sans-serif" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle" transform="rotate(-3 66 60)">BNS</text>
      <text x="66" y="61" font-family="'Poppins',sans-serif" font-size="11.5" font-weight="700" fill="${p.accent}" text-anchor="middle" transform="rotate(-3 66 60)">2023</text>
      <text x="66" y="80" font-family="'Poppins',sans-serif" font-size="8" font-weight="600" fill="#DDE8F6" text-anchor="middle" transform="rotate(-3 66 60)">ACT NO. 45</text>

      <!-- Clean National Courthouse + Jurisdiction Globe (Right, zero overlapping text!) -->
      <polygon points="186,18 134,40 238,40" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="1.9" stroke-linejoin="round"/>
      <rect x="142" y="40" width="14" height="44" fill="#FFFDF7" stroke="${p.ink}" stroke-width="1.7"/>
      <rect x="179" y="40" width="14" height="44" fill="#FFFDF7" stroke="${p.ink}" stroke-width="1.7"/>
      <rect x="216" y="40" width="14" height="44" fill="#FFFDF7" stroke="${p.ink}" stroke-width="1.7"/>
      <rect x="132" y="84" width="108" height="9" rx="2" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="1.7"/>
      ${banner(126, 98, 128, 19, 'INDIA & JURISDICTION', p)}
    </g>
  `,

  // Section 2: Statutory Definitions Lexicon + Magnifying Lens
  definitions: (p) => `
    <g>
      <path d="M 30 22 L 104 16 L 104 94 L 30 100 Z" fill="#FFFDF7" stroke="${p.ink}" stroke-width="2" stroke-linejoin="round"/>
      <path d="M 104 16 L 178 22 L 178 100 L 104 94 Z" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2" stroke-linejoin="round"/>
      <text x="67" y="34" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="800" fill="${p.ink}" text-anchor="middle">DEFINITIONS</text>
      <line x1="42" y1="45" x2="92" y2="41" stroke="${p.tint}" stroke-width="2" stroke-linecap="round"/>
      <line x1="42" y1="57" x2="92" y2="53" stroke="${p.accent}" stroke-width="2.4" stroke-linecap="round"/>
      <line x1="42" y1="69" x2="88" y2="65" stroke="${p.tint}" stroke-width="2" stroke-linecap="round"/>
      <line x1="42" y1="81" x2="90" y2="77" stroke="${p.ink}" stroke-width="1.6" stroke-linecap="round"/>

      <text x="141" y="38" font-family="'Poppins',sans-serif" font-size="9" font-weight="700" fill="${p.ink}" text-anchor="middle">39 Clauses</text>
      <text x="141" y="54" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="600" fill="${p.ink}" text-anchor="middle">Act • Court</text>
      <text x="141" y="68" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="600" fill="${p.ink}" text-anchor="middle">Good Faith</text>
      <text x="141" y="82" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="600" fill="${p.ink}" text-anchor="middle">E-Records</text>

      <!-- Magnifying Glass -->
      <circle cx="222" cy="52" r="24" fill="#FFFFFF" fill-opacity="0.88" stroke="${p.ink}" stroke-width="2.6"/>
      <circle cx="222" cy="52" r="17" fill="${p.fillMid}" stroke="${p.accent}" stroke-width="1.4"/>
      <text x="222" y="56" font-family="'Poppins',sans-serif" font-size="11" font-weight="800" fill="${p.ink}" text-anchor="middle">2(1)</text>
      <line x1="239" y1="70" x2="258" y2="91" stroke="${p.ink}" stroke-width="5.5" stroke-linecap="round"/>
      ${banner(182, 98, 86, 19, 'STATUTORY KEY', p)}
    </g>
  `,

  // Section 3: General Explanations / Rules of Construction
  general_explanations: (p) => `
    <g>
      ${drawScales(143, 24, 62, 34, p)}
      ${banner(84, 70, 118, 22, 'CONSTRUCTION RULES', p)}
      ${banner(22, 97, 74, 19, 'INTENT', p, p.fillSoft, p.ink, 8.8)}
      ${banner(106, 97, 74, 19, 'EXPLAIN', p, p.fillMid, p.ink, 8.8)}
      ${banner(190, 97, 74, 19, 'LIABILITY', p, p.fillSoft, p.ink, 8.8)}
    </g>
  `,

  // Chapter V — Gang Rape / Severe Sexual Offence Against Women (Sec 70)
  woman_severe_justice: (p) => `
    <g>
      <!-- Protective Shield -->
      <path d="M 78 16 L 122 28 L 122 58 C 122 83 99 99 78 106 C 57 99 34 83 34 58 L 34 28 Z" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M 78 24 L 114 34 L 114 58 C 114 78 95 92 78 98 C 61 92 42 78 42 58 L 42 34 Z" fill="#FFFFFF" stroke="${p.accent}" stroke-width="1.4"/>
      <!-- Balance beam inside shield -->
      <line x1="78" y1="39" x2="78" y2="82" stroke="${p.ink}" stroke-width="2.2" stroke-linecap="round"/>
      <line x1="56" y1="48" x2="100" y2="48" stroke="${p.ink}" stroke-width="2.2" stroke-linecap="round"/>
      <circle cx="78" cy="48" r="2.6" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.2"/>
      <line x1="56" y1="48" x2="50" y2="65" stroke="${p.ink}" stroke-width="1.2"/>
      <line x1="56" y1="48" x2="62" y2="65" stroke="${p.ink}" stroke-width="1.2"/>
      <path d="M 48 65 Q 56 73 64 65 Z" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.3"/>
      <line x1="100" y1="48" x2="94" y2="65" stroke="${p.ink}" stroke-width="1.2"/>
      <line x1="100" y1="48" x2="106" y2="65" stroke="${p.ink}" stroke-width="1.2"/>
      <path d="M 92 65 Q 100 73 108 65 Z" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.3"/>
      <line x1="68" y1="82" x2="88" y2="82" stroke="${p.ink}" stroke-width="2.2" stroke-linecap="round"/>

      <!-- Sentence Severity Ledger Card (Right) -->
      <rect x="142" y="16" width="122" height="72" rx="8" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <rect x="142" y="16" width="122" height="21" rx="7" fill="${p.alert}" stroke="${p.ink}" stroke-width="1.8"/>
      <text x="203" y="30" font-family="'Poppins',sans-serif" font-size="9" font-weight="800" fill="#FFFFFF" text-anchor="middle">STRICT SENTENCE</text>
      <text x="203" y="54" font-family="'Poppins',sans-serif" font-size="11.5" font-weight="800" fill="${p.ink}" text-anchor="middle">20 YRS MIN</text>
      <text x="203" y="70" font-family="'Poppins',sans-serif" font-size="9.5" font-weight="700" fill="${p.alert}" text-anchor="middle">TO NATURAL LIFE</text>
      <text x="203" y="83" font-family="'Poppins',sans-serif" font-size="8.2" font-weight="600" fill="${p.tint}" text-anchor="middle">(or Death if &lt; 18)</text>

      ${banner(142, 95, 122, 20, 'ZERO TOLERANCE', p)}
    </g>
  `,

  // Repeat Offenders / Judicial Sentencing / Punishments (Sec 71, Sec 4-13)
  repeat_offender_punishment: (p) => `
    <g>
      <!-- Repeat Offence Dossier -->
      <rect x="26" y="18" width="96" height="82" rx="6" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <rect x="38" y="11" width="44" height="12" rx="3" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="1.5"/>
      <line x1="38" y1="35" x2="108" y2="35" stroke="${p.tint}" stroke-width="2"/>
      <line x1="38" y1="46" x2="102" y2="46" stroke="${p.tint}" stroke-width="2"/>
      <!-- Stamp Badge -->
      <rect x="36" y="57" width="76" height="25" rx="4" fill="#FDE4E1" stroke="${p.alert}" stroke-width="1.8" transform="rotate(-7 74 69)"/>
      <text x="74" y="73" font-family="'Poppins',sans-serif" font-size="9.5" font-weight="800" fill="${p.alert}" text-anchor="middle" transform="rotate(-7 74 69)">REPEAT ACT</text>

      <!-- Escalation Arrow -->
      <path d="M 130 62 L 154 62 L 154 53 L 169 66 L 154 79 L 154 70 L 130 70 Z" fill="${p.accent}" stroke="${p.ink}" stroke-width="1.5"/>

      <!-- Gavel + Prison/Sentence Box -->
      ${drawGavel(216, 48, -28, p)}
      ${banner(152, 95, 114, 20, 'ENHANCED PENALTY', p)}
    </g>
  `,

  // Identity Protection / Victim Privacy Shield (Sec 72)
  victim_identity_shield: (p) => `
    <g>
      <!-- Confidential Identity Card (Left-Center) -->
      <rect x="32" y="18" width="128" height="74" rx="8" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <circle cx="57" cy="46" r="13" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="1.6"/>
      <circle cx="57" cy="42" r="4.5" fill="${p.ink}"/>
      <path d="M 48 55 C 48 49 66 49 66 55" fill="${p.ink}"/>
      <!-- Redacted Name Bars -->
      <rect x="78" y="34" width="68" height="10" rx="2.5" fill="${p.ink}"/>
      <rect x="78" y="50" width="52" height="8" rx="2.5" fill="${p.tint}"/>
      <rect x="44" y="68" width="102" height="12" rx="3" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="1.2"/>
      <text x="95" y="77" font-family="'Poppins',sans-serif" font-size="8" font-weight="800" fill="${p.ink}" text-anchor="middle">IDENTITY SEALED</text>

      <!-- Padlock & Crossed Camera (Right) -->
      <rect x="184" y="42" width="44" height="36" rx="6" fill="${p.accent}" stroke="${p.ink}" stroke-width="2"/>
      <path d="M 193 42 L 193 30 C 193 19 219 19 219 30 L 219 42" fill="none" stroke="${p.ink}" stroke-width="3.2"/>
      <circle cx="206" cy="57" r="4.2" fill="${p.ink}"/>
      <line x1="206" y1="60" x2="206" y2="68" stroke="${p.ink}" stroke-width="2.5" stroke-linecap="round"/>

      <!-- Crossed Eye / Media Prohibited Sign -->
      <circle cx="248" cy="36" r="14" fill="#FFFFFF" stroke="${p.alert}" stroke-width="2.2"/>
      <ellipse cx="248" cy="36" rx="8" ry="5" fill="none" stroke="${p.ink}" stroke-width="1.6"/>
      <circle cx="248" cy="36" r="2.2" fill="${p.ink}"/>
      <line x1="238" y1="46" x2="258" y2="26" stroke="${p.alert}" stroke-width="2.4" stroke-linecap="round"/>

      ${banner(64, 98, 158, 20, 'PRIVACY & NO DISCLOSURE', p)}
    </g>
  `,

  // General Punishments / Sentencing / Imprisonment (Ch II)
  punishments_sentencing: (p) => `
    <g>
      ${drawGavel(82, 46, -26, p)}
      <!-- Sentencing Statute Scroll & Fine Seal -->
      <rect x="148" y="18" width="108" height="68" rx="7" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <text x="202" y="36" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="800" fill="${p.tint}" text-anchor="middle">STATUTORY ORDER</text>
      <line x1="164" y1="45" x2="240" y2="45" stroke="${p.accent}" stroke-width="2.2"/>
      <text x="202" y="61" font-family="'Poppins',sans-serif" font-size="9" font-weight="700" fill="${p.ink}" text-anchor="middle">Prison • Community</text>
      <text x="202" y="75" font-family="'Poppins',sans-serif" font-size="9" font-weight="700" fill="${p.ink}" text-anchor="middle">Service • Fine</text>
      ${banner(68, 95, 150, 20, 'SENTENCING & FINES', p)}
    </g>
  `,

  // General Exceptions & Legal Defences (Ch III)
  general_exceptions: (p) => `
    <g>
      <!-- Protective Legal Umbrella / Shield -->
      <path d="M 143 18 C 98 18 74 42 74 56 L 212 56 C 212 42 188 18 143 18 Z" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M 143 56 L 143 82 C 143 89 154 89 154 82" fill="none" stroke="${p.ink}" stroke-width="2.6" stroke-linecap="round"/>
      <circle cx="143" cy="40" r="11" fill="#FFFFFF" stroke="${p.ink}" stroke-width="1.8"/>
      <path d="M 138 40 L 142 44 L 150 35" fill="none" stroke="${p.tint}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      ${banner(64, 96, 158, 20, 'STATUTORY EXCEPTION', p)}
    </g>
  `,

  // Private Defence (Sec 34–44)
  private_defence: (p) => `
    <g>
      <path d="M 92 16 L 136 27 L 136 56 C 136 80 113 94 92 100 C 71 94 48 80 48 56 L 48 27 Z" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2.2"/>
      <path d="M 80 56 L 90 66 L 108 44" fill="none" stroke="${p.ink}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="156" y="24" width="96" height="58" rx="7" fill="#FFFDF8" stroke="${p.ink}" stroke-width="1.9"/>
      <text x="204" y="47" font-family="'Poppins',sans-serif" font-size="9.5" font-weight="800" fill="${p.ink}" text-anchor="middle">BODY &amp;</text>
      <text x="204" y="61" font-family="'Poppins',sans-serif" font-size="9.5" font-weight="800" fill="${p.tint}" text-anchor="middle">PROPERTY</text>
      <text x="204" y="74" font-family="'Poppins',sans-serif" font-size="8" font-weight="600" fill="${p.ink}" text-anchor="middle">Proportionate Force</text>
      ${banner(64, 98, 158, 19, 'RIGHT OF SELF-DEFENCE', p)}
    </g>
  `,

  // Abetment, Conspiracy & Attempt (Ch IV)
  abetment_conspiracy: (p) => `
    <g>
      <circle cx="62" cy="48" r="20" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2"/>
      <text x="62" y="52" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="800" fill="${p.ink}" text-anchor="middle">PLAN</text>
      <line x1="84" y1="48" x2="118" y2="48" stroke="${p.ink}" stroke-width="2.2" stroke-dasharray="4 3"/>
      <circle cx="143" cy="48" r="20" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="2"/>
      <text x="143" y="52" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="800" fill="${p.ink}" text-anchor="middle">AID</text>
      <line x1="165" y1="48" x2="199" y2="48" stroke="${p.ink}" stroke-width="2.2" stroke-dasharray="4 3"/>
      <circle cx="224" cy="48" r="20" fill="#FDE4E1" stroke="${p.alert}" stroke-width="2"/>
      <text x="224" y="52" font-family="'Poppins',sans-serif" font-size="8.5" font-weight="800" fill="${p.alert}" text-anchor="middle">ACT</text>
      ${banner(46, 94, 194, 20, 'ABETMENT & JOINT LIABILITY', p)}
    </g>
  `,

  // Woman & Child Offences General (Ch V)
  woman_child_general: (p) => `
    <g>
      <path d="M 84 18 L 124 28 L 124 55 C 124 78 104 91 84 96 C 64 91 44 78 44 55 L 44 28 Z" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2"/>
      <circle cx="84" cy="44" r="8" fill="${p.ink}"/>
      <path d="M 68 70 C 68 57 100 57 100 70" fill="${p.tint}" stroke="${p.ink}" stroke-width="1.5"/>
      ${drawScales(200, 32, 38, 28, p)}
      ${banner(54, 97, 178, 20, 'WOMAN & CHILD PROTECTION', p)}
    </g>
  `,

  // Human Body Offences (Ch VI — Murder, Homicide, Hurt)
  human_body: (p) => `
    <g>
      <rect x="36" y="18" width="96" height="70" rx="8" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <polyline points="48,54 66,54 76,34 86,70 96,46 104,54 120,54" fill="none" stroke="${p.alert}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      ${drawScales(202, 28, 38, 28, p)}
      ${banner(52, 96, 182, 20, 'HUMAN LIFE & BODILY SAFETY', p)}
    </g>
  `,

  // State Sovereignty, Organized Crime & Forces (Ch VII–VIII)
  state_security: (p) => `
    <g>
      <polygon points="143,16 90,34 196,34" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2" stroke-linejoin="round"/>
      <rect x="98" y="34" width="12" height="38" fill="#FFFDF7" stroke="${p.ink}" stroke-width="1.6"/>
      <rect x="137" y="34" width="12" height="38" fill="#FFFDF7" stroke="${p.ink}" stroke-width="1.6"/>
      <rect x="176" y="34" width="12" height="38" fill="#FFFDF7" stroke="${p.ink}" stroke-width="1.6"/>
      <rect x="88" y="72" width="110" height="8" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="1.6"/>
      ${banner(54, 94, 178, 20, 'SOVEREIGNTY & PUBLIC SAFETY', p)}
    </g>
  `,

  // Elections (Ch IX)
  elections: (p) => `
    <g>
      <rect x="88" y="42" width="110" height="44" rx="6" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="2"/>
      <line x1="118" y1="48" x2="168" y2="48" stroke="${p.ink}" stroke-width="3" stroke-linecap="round"/>
      <rect x="125" y="16" width="36" height="30" rx="3" fill="#FFFDF8" stroke="${p.ink}" stroke-width="1.8" transform="rotate(-6 143 31)"/>
      <path d="M 135 31 L 141 37 L 152 24" fill="none" stroke="${p.tint}" stroke-width="2.4" stroke-linecap="round"/>
      ${banner(58, 95, 170, 20, 'FREE & FAIR ELECTIONS', p)}
    </g>
  `,

  // Coin, Currency & Stamps (Ch X)
  currency_stamps: (p) => `
    <g>
      <rect x="44" y="24" width="118" height="58" rx="6" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="2"/>
      <rect x="52" y="32" width="102" height="42" rx="3" fill="#FFFDF8" stroke="${p.tint}" stroke-width="1.4"/>
      <text x="103" y="60" font-family="'Poppins',sans-serif" font-size="22" font-weight="800" fill="${p.ink}" text-anchor="middle">₹</text>
      <circle cx="206" cy="48" r="22" fill="#FFFFFF" stroke="${p.ink}" stroke-width="2.4"/>
      <line x1="222" y1="64" x2="240" y2="82" stroke="${p.ink}" stroke-width="5" stroke-linecap="round"/>
      <text x="206" y="52" font-family="'Poppins',sans-serif" font-size="9" font-weight="800" fill="${p.alert}" text-anchor="middle">CHECK</text>
      ${banner(60, 95, 166, 20, 'CURRENCY & STAMP INTEGRITY', p)}
    </g>
  `,

  // Public Servants & Judicial Evidence (Ch XI–XIV)
  public_justice_courts: (p) => `
    <g>
      ${drawGavel(92, 46, -24, p)}
      <rect x="150" y="18" width="96" height="68" rx="6" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <text x="198" y="38" font-family="'Poppins',sans-serif" font-size="9" font-weight="800" fill="${p.ink}" text-anchor="middle">TRUTH &amp; OATH</text>
      <line x1="165" y1="48" x2="230" y2="48" stroke="${p.accent}" stroke-width="2"/>
      <line x1="165" y1="60" x2="225" y2="60" stroke="${p.tint}" stroke-width="2"/>
      <line x1="165" y1="72" x2="215" y2="72" stroke="${p.tint}" stroke-width="2"/>
      ${banner(52, 95, 182, 20, 'PUBLIC JUSTICE & AUTHORITY', p)}
    </g>
  `,

  // Property, Theft, Robbery & Documents (Ch XVII–XVIII)
  property_documents: (p) => `
    <g>
      <rect x="44" y="20" width="90" height="68" rx="6" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <text x="89" y="42" font-family="'Poppins',sans-serif" font-size="9" font-weight="800" fill="${p.ink}" text-anchor="middle">PROPERTY</text>
      <line x1="56" y1="52" x2="122" y2="52" stroke="${p.accent}" stroke-width="2"/>
      <line x1="56" y1="64" x2="112" y2="64" stroke="${p.tint}" stroke-width="2"/>
      <circle cx="114" cy="72" r="10" fill="${p.fillSoft}" stroke="${p.ink}" stroke-width="1.5"/>
      <rect x="166" y="40" width="66" height="44" rx="6" fill="${p.fillMid}" stroke="${p.ink}" stroke-width="2"/>
      <path d="M 181 40 L 181 29 C 181 18 217 18 217 29 L 217 40" fill="none" stroke="${p.ink}" stroke-width="3"/>
      <circle cx="199" cy="61" r="4" fill="${p.ink}"/>
      ${banner(50, 95, 186, 20, 'PROPERTY & RECORD SECURITY', p)}
    </g>
  `,

  // Defamation, Intimidation, Public Peace, Religion, Repeal (Ch XV–XVI, XIX–XX)
  reputation_order_saving: (p) => `
    <g>
      ${drawScales(94, 28, 38, 30, p)}
      <rect x="156" y="22" width="96" height="62" rx="7" fill="#FFFDF8" stroke="${p.ink}" stroke-width="2"/>
      <text x="204" y="44" font-family="'Poppins',sans-serif" font-size="9" font-weight="800" fill="${p.ink}" text-anchor="middle">LAWFUL</text>
      <text x="204" y="59" font-family="'Poppins',sans-serif" font-size="9" font-weight="800" fill="${p.tint}" text-anchor="middle">BALANCE</text>
      <text x="204" y="74" font-family="'Poppins',sans-serif" font-size="8" font-weight="600" fill="${p.ink}" text-anchor="middle">Rights &amp; Duties</text>
      ${banner(52, 95, 182, 20, 'LEGAL RIGHTS & SAVINGS', p)}
    </g>
  `,
};

function selectMotifKey(card, post) {
  const secNum = parseInt(String(card.n || card.s || '0').replace(/\D/g, ''), 10) || 0;
  const text = `${card.title || ''} ${card.easy || ''} ${post.chapter_name || ''}`.toLowerCase();

  // Exact early sections
  if (secNum === 1) return 'title_commencement';
  if (secNum === 2) return 'definitions';
  if (secNum === 3) return 'general_explanations';

  // Specific high-impact sections (e.g. Post 24: Sec 70-72 & nearby)
  if (text.includes('identity') || text.includes('disclosure') || text.includes('privacy')) {
    return 'victim_identity_shield';
  }
  if (text.includes('repeat offender') || text.includes('previous conviction')) {
    return 'repeat_offender_punishment';
  }
  if (text.includes('gang rape') || text.includes('rape')) {
    return 'woman_severe_justice';
  }
  if (text.includes('private defence') || text.includes('self-defence')) {
    return 'private_defence';
  }
  if (text.includes('abet') || text.includes('conspiracy') || text.includes('attempt')) {
    return 'abetment_conspiracy';
  }
  if (text.includes('election') || text.includes('ballot') || text.includes('voting')) {
    return 'elections';
  }
  if (text.includes('coin') || text.includes('currency') || text.includes('bank-note') || text.includes('stamp')) {
    return 'currency_stamps';
  }
  if (text.includes('punishment') || text.includes('imprisonment') || text.includes('commut') || text.includes('fine') || text.includes('solitary')) {
    return 'punishments_sentencing';
  }
  if (text.includes('exception') || text.includes('unsound mind') || text.includes('intoxication') || text.includes('mistake of fact') || text.includes('good faith')) {
    return 'general_exceptions';
  }
  if (text.includes('woman') || text.includes('child') || text.includes('dowry') || text.includes('marriage') || text.includes('miscarriage')) {
    return 'woman_child_general';
  }
  if (text.includes('murder') || text.includes('homicide') || text.includes('hurt') || text.includes('assault') || text.includes('kidnap') || text.includes('human body')) {
    return 'human_body';
  }
  if (text.includes('state') || text.includes('sovereignty') || text.includes('terror') || text.includes('army') || text.includes('navy') || text.includes('air force')) {
    return 'state_security';
  }
  if (text.includes('public servant') || text.includes('evidence') || text.includes('perjury') || text.includes('contempt') || text.includes('court')) {
    return 'public_justice_courts';
  }
  if (text.includes('theft') || text.includes('robbery') || text.includes('extortion') || text.includes('dacoity') || text.includes('property') || text.includes('forgery') || text.includes('document') || text.includes('cheat')) {
    return 'property_documents';
  }
  return 'reputation_order_saving';
}

function renderCardIllustration(card, cardIndex, post) {
  const palette = PALETTES[cardIndex % PALETTES.length];
  const motifKey = selectMotifKey(card, post);
  const svgInner = (MOTIFS[motifKey] || MOTIFS.reputation_order_saving)(palette);
  return `<svg viewBox="0 0 286 128" width="96%" height="100%" style="max-height:224px;" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-label="${motifKey}">${svgInner}</svg>`;
}

module.exports = { renderCardIllustration, selectMotifKey };
