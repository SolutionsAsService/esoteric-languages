# R4 Critic: Inclusion (Mace)

**Anchor used:** Mace et al., Principles of Universal Design: Principle 4 (Perceptible Information) and 7 (Size and Space for Approach and Use); named check, focus visibility.

**Observed in the work:** A global `:focus-visible` 4px outline with 3px offset covers masthead, skip link (shown on focus), pager and details summaries. Tiles and chips override it with a 4px outline in the field's own ink colour, inset inside the box, so overflow:hidden cannot clip it. Every scrolling `pre` and `.tablewrap`/`.piet-wrap` carries tabindex=0, a region role and a label, so overflow content is keyboard-reachable and shows the ring. Targets are at least 24px (measured 0 under). Reflow holds at 375 px with no page overflow. The current Piet cell and tape cell are marked by outline plus text, not colour alone. Hover motion sits behind prefers-reduced-motion. The Ook! fallback (one row) and the M13 container-unit titles introduce no focus or reflow barrier. I verified this by reading the CSS and HTML only; I ran no live keyboard pass.

**Verdict:** PASS

**Requested change:** none

**Statement of meaning:** The site can be reached, seen and used by keyboard alone, at phone width, without relying on colour or motion.

**Critic question:** Would the inset tile ring stay visible in forced-colors mode, where author colours are overridden?
