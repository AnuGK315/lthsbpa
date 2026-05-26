---
name: Executive Green & Gold
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#404945'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#707974'
  outline-variant: '#c0c9c3'
  surface-tint: '#376757'
  primary: '#003629'
  on-primary: '#ffffff'
  primary-container: '#1b4d3e'
  on-primary-container: '#8abda9'
  inverse-primary: '#9ed1bd'
  secondary: '#775a19'
  on-secondary: '#ffffff'
  secondary-container: '#fed488'
  on-secondary-container: '#785a1a'
  tertiary: '#252f3f'
  on-tertiary: '#ffffff'
  tertiary-container: '#3b4557'
  on-tertiary-container: '#a8b2c8'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#baeed9'
  primary-fixed-dim: '#9ed1bd'
  on-primary-fixed: '#002117'
  on-primary-fixed-variant: '#1d4f40'
  secondary-fixed: '#ffdea5'
  secondary-fixed-dim: '#e9c176'
  on-secondary-fixed: '#261900'
  on-secondary-fixed-variant: '#5d4201'
  tertiary-fixed: '#d9e3f9'
  tertiary-fixed-dim: '#bdc7dc'
  on-tertiary-fixed: '#121c2c'
  on-tertiary-fixed-variant: '#3d4759'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
  forest-deep: '#1B4D3E'
  champagne-gold: '#C5A059'
  slate-navy: '#2D3748'
  paper-white: '#FFFFFF'
  graphite: '#4A5568'
typography:
  headline-xl:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style

The design system is engineered for the Lebanon Trail High School BPA Chapter, bridging the gap between high school identity and professional business standards. The brand personality is **ambitious, structured, and prestigious**, moving away from "athletic" vibrance toward a "corporate-collegiate" aesthetic.

The design style is **Corporate / Modern** with a focus on **Precision Minimalism**. It utilizes generous whitespace, sharp layouts, and a sophisticated color palette to evoke the feeling of a high-end consulting firm or financial institution, while subtly honoring the school's heritage through refined material metaphors.

## Colors

The palette transforms the traditional school colors into a professional executive theme. 

- **Primary (Forest Deep):** A muted, dark green used for primary actions, navigation backgrounds, and authoritative elements.
- **Secondary (Champagne Gold):** A sophisticated metallic hue used for accents, highlights, and secondary call-to-actions. This should be used sparingly to maintain its prestige.
- **Tertiary (Slate Navy):** Used for deep text, iconography, and subtle structural borders to ground the design.
- **Neutral:** A range of soft greys and whites to ensure the interface remains "airy" and easy to navigate.

Avoid using the high-vibrance athletic green or yellow found in traditional school sports gear. High-contrast pairings should favor Forest Deep against Paper White.

## Typography

This design system utilizes a dual-font strategy to balance character with readability.

- **Headlines (Montserrat):** Chosen for its geometric precision and modern professional feel. Use Bold or Semi-Bold weights for hierarchy. Negative letter-spacing is applied to larger sizes to maintain a tight, editorial look.
- **Body & UI (Inter):** A systematic sans-serif that ensures maximum legibility for dense information, such as event schedules and competition results.
- **Labels:** Always use Inter with increased letter-spacing and medium to bold weights for clear categorization.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for desktop to provide a structured, "document-like" feel that aligns with business professional aesthetics.

- **Desktop:** 12-column grid with a 1200px max-width. Gutters are fixed at 24px to ensure breathing room between content modules.
- **Mobile:** Fluid 4-column grid with 16px side margins. 
- **Rhythm:** All spacing (padding, margins) should be multiples of 8px. Use 48px or 64px vertical spacing between major sections to emphasize a clean, uncluttered experience.
- **Alignment:** Consistent left-alignment for text blocks to mimic formal reports and business correspondence.

## Elevation & Depth

To maintain a "Professional" and "Clean" look, this design system avoids heavy, muddy shadows. 

- **Tonal Layers:** Depth is primarily communicated through subtle background color shifts (e.g., a slightly darker neutral for the footer or a pure white surface over a light grey background).
- **Low-Contrast Outlines:** Use 1px borders in Slate Navy (at 10-15% opacity) for cards and input fields. This creates structure without visual noise.
- **Focus States:** When an element requires elevation (like a hovered card), use a very soft, diffused "ambient" shadow with a hint of the Forest Deep tint to maintain brand cohesion.

## Shapes

The shape language is **Soft/Professional**. By using a 0.25rem (4px) base radius, we avoid the aggressive nature of sharp corners while remaining more formal than the "bubbly" feel of highly rounded UI. 

- **Buttons:** 4px radius for a crisp, tailored appearance.
- **Cards:** 8px (rounded-lg) for container elements to provide a gentle distinction from the background.
- **Inputs:** 4px radius, ensuring they feel like official forms.

## Components

- **Buttons:** The primary button is Forest Deep with white text. The secondary button uses a Slate Navy outline. Use the Champagne Gold exclusively for high-priority "Join" or "Register" actions to make them stand out.
- **Chips:** Used for competition categories or status tags. Use low-saturation background tints of the brand colors with dark text (e.g., a light champagne background with dark brown-gold text).
- **Cards:** White background, 1px subtle border, 8px corner radius. No shadow in default state; soft shadow on hover.
- **Input Fields:** Clean, minimal styling with a Slate Navy bottom-border or light 4-sided border. Labels should use the `label-md` typography style.
- **Lists:** Use Forest Deep for bullet points or iconography in lists to reinforce the brand.
- **Navigation:** Top-bar should be clean with text-only links. Use a subtle Champagne Gold underline for the active state.