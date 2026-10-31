# Critic: Inclusion (Holmes), R4

Anchor used: Kat Holmes, Mismatch: exclusion arises when a design fits one body or context (persona spectrum: permanent, temporary, situational); solve for one, extend to many.

Observed in the work: Every page has a viewport meta, a skip link, labelled navs, aria-current, focus-visible outlines of 4 px, and keyboard-focusable scroll regions (tablewrap, pre with aria-label). Glyph art is aria-hidden with its content as text on the page. Contrast minimum 5.25 in light and dark; targets 24 px or larger; no page overflow at 375 px; 12 px smallest text. M12 degrades to one row without round(); at 320 px only the caption shows, no information is lost. Motion is gated by prefers-reduced-motion. Titles fit in fallback font.

Verdict: PASS

Requested change: none

Statement of meaning: A phone reader, a screen-reader user and a keyboard user each get the same programs, outputs and step counts as text.

Critic question: At 320 px the glyph area is 0 px; is that decorative loss, or does any poster figure exist only there?
