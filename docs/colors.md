# Colors

All colors are importable as module-level constants and collected in the `CHARITE_COLORS` dict.

```python
from charite_plot.colors import PRIME_BLUE, TEXT_GREY
from charite_plot import CHARITE_COLORS  # full dict

print(PRIME_BLUE)  # "#004d9b"
print(CHARITE_COLORS["korall"])  # "#ea5451"
```

## How the colors look with color-vision deficiencies

Switch the simulation to see every swatch on this page as people with a color-vision deficiency see it
(Machado et al. 2009, full severity). About 8 % of men and 0.5 % of women have a red–green deficiency;
greyscale shows how a palette survives black-and-white printing. Simulations are approximations, least
accurate for the rare tritanopia.

<div class="cvd-toggle"></div>

---

## Primary

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#004d9b"></div>
    <span class="name">PRIME_BLUE</span>
    <code class="hex">#004d9b</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#7e898f"></div>
    <span class="name">PRIME_DGREY</span>
    <code class="hex">#7e898f</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#cbcfd2"></div>
    <span class="name">PRIME_LGREY</span>
    <code class="hex">#cbcfd2</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#5e676c"></div>
    <span class="name">TEXT_GREY</span>
    <code class="hex">#5e676c</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#000000"></div>
    <span class="name">BLACK</span>
    <code class="hex">#000000</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#ffffff;border:1px solid #cbcfd2"></div>
    <span class="name">WHITE</span>
    <code class="hex">#ffffff</code>
  </div>
</div>

## Secondary

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#002552"></div>
    <span class="name">SECOND_DBLUE</span>
    <code class="hex">#002552</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#007bc3"></div>
    <span class="name">SECOND_LBLUE</span>
    <code class="hex">#007bc3</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#ea5451"></div>
    <span class="name">KORALL</span>
    <code class="hex">#ea5451</code>
  </div>
</div>

## Accents

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#564091"></div>
    <span class="name">LILA</span>
    <code class="hex">#564091</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#7876b6"></div>
    <span class="name">LAVENDEL</span>
    <code class="hex">#7876b6</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#6f186d"></div>
    <span class="name">BROMBEERE</span>
    <code class="hex">#6f186d</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#944292"></div>
    <span class="name">PFLAUME</span>
    <code class="hex">#944292</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#89014c"></div>
    <span class="name">WEINROT</span>
    <code class="hex">#89014c</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#d74b7f"></div>
    <span class="name">HIMBEER</span>
    <code class="hex">#d74b7f</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#e31f2c"></div>
    <span class="name">ROT</span>
    <code class="hex">#e31f2c</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#fab600"></div>
    <span class="name">MANGO</span>
    <code class="hex">#fab600</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#ffdf43"></div>
    <span class="name">RAPSGELB</span>
    <code class="hex">#ffdf43</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#d1d811"></div>
    <span class="name">LIMETTE</span>
    <code class="hex">#d1d811</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#a1ba0c"></div>
    <span class="name">GRASGRUEN</span>
    <code class="hex">#a1ba0c</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#008939"></div>
    <span class="name">GRUEN</span>
    <code class="hex">#008939</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#88c69a"></div>
    <span class="name">MINT</span>
    <code class="hex">#88c69a</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#009aa9"></div>
    <span class="name">MINERAL</span>
    <code class="hex">#009aa9</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#61c3d7"></div>
    <span class="name">AQUA</span>
    <code class="hex">#61c3d7</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#89725b"></div>
    <span class="name">BRAUN</span>
    <code class="hex">#89725b</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#c8b8ad"></div>
    <span class="name">MOCCA</span>
    <code class="hex">#c8b8ad</code>
  </div>
</div>

## Employer branding

Employer-Branding-Grün is reserved for Charité's employer-branding communication.
It is available as `EMPLOYER_BRANDING_GREEN`, but it is not used in any palette.

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#ccefcb"></div>
    <span class="name">EMPLOYER_BRANDING_GREEN</span>
    <code class="hex">#ccefcb</code>
  </div>
</div>

---

# BIH colors

The Berlin Institute of Health at Charité colors live in `charite_plot.brands.bih` and are collected in the `BIH_COLORS` dict
(they are not re-exported at the top level, because `KORALL`, `MINERAL` and `LAVENDEL` share names with Charité colors).

```python
from charite_plot.brands.bih import BLAU, BIH_COLORS
from charite_plot import tint

tint(BLAU, 20)  # "#ccd7dd" — BIH allows tints of the diagram colors in 10 % steps
```

## Diagram colors

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#003754"></div>
    <span class="name">BLAU</span>
    <code class="hex">#003754</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#ea5451"></div>
    <span class="name">KORALL</span>
    <code class="hex">#ea5451</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#9d7220"></div>
    <span class="name">GOLD</span>
    <code class="hex">#9d7220</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#009aa9"></div>
    <span class="name">MINERAL</span>
    <code class="hex">#009aa9</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#7876b6"></div>
    <span class="name">LAVENDEL</span>
    <code class="hex">#7876b6</code>
  </div>
</div>

## Text-only colors

The BIH handbook reserves these for text and highlights; they are not used in any palette.

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#af1821"></div>
    <span class="name">DUNKELROT</span>
    <code class="hex">#af1821</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#ffb0ac"></div>
    <span class="name">HELLROSA</span>
    <code class="hex">#ffb0ac</code>
  </div>
</div>

## Text and axes

The handbook forbids black, but the BIH theme deliberately uses black text and axes because scientific journals expect it.

<div class="color-grid">
  <div class="color-swatch">
    <div class="chip" style="background:#000000"></div>
    <span class="name">BLACK</span>
    <code class="hex">#000000</code>
  </div>
  <div class="color-swatch">
    <div class="chip" style="background:#ffffff"></div>
    <span class="name">WHITE</span>
    <code class="hex">#ffffff</code>
  </div>
</div>
