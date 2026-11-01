from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from pypdf import PdfReader

ROOT = Path('/Users/adirosenstock/Downloads/Northwestern/Senior_Year/Q1/STAT_362')
OUT = ROOT / 'output/pdf/STAT_362_Midterm_Cheat_Sheet.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('/System/Library/Fonts/Supplemental')
for key, fn in [('N', 'Arial Narrow.ttf'), ('NB', 'Arial Narrow Bold.ttf'),
                ('NI', 'Arial Narrow Italic.ttf'), ('NBI', 'Arial Narrow Bold Italic.ttf'),
                ('U', 'Arial Unicode.ttf')]:
    pdfmetrics.registerFont(TTFont(key, str(FONT_DIR / fn)))
pdfmetrics.registerFontFamily('N', normal='N', bold='NB', italic='NI', boldItalic='NBI')

COLS = [
[
('h', '1  GRADIENT DESCENT + LINEAR REGRESSION'),
('p', 'M observations, N features; xᵢ₀ = 1. <b>Model:</b> zᵢ = wᵀxᵢ = w₀ + ∑<sub>j=1</sub><super>N</super>wⱼxᵢⱼ. Training minimizes J over w; x, y are fixed.'),
('e', 'J = MSE = (1/M) ∑ᵢ (yᵢ − zᵢ)<super>2</super>'),
('e', '∂J/∂wⱼ = −(2/M) ∑ᵢ (yᵢ − zᵢ)xᵢⱼ'),
('e', '∇J = (2/M) Xᵀ(Xw − y)'),
('p', '<b>Why −2 and xᵢⱼ?</b> Chain rule: derivative of the square gives 2(yᵢ − zᵢ); the inside derivative is −xᵢⱼ. For w₀, xᵢ₀ = 1.'),
('e', '<b>GD:</b> w<sub>k+1</sub> = w<sub>k</sub> − η∇J(w<sub>k</sub>)'),
('p', 'Initialize w → gradient → update <b>all coordinates using old w</b> → repeat until ‖w<sub>k+1</sub> − w<sub>k</sub>‖₂ &lt; tol (or iteration limit).'),
('p', '<b>−∇J</b> = steepest local decrease; ∇J points uphill. Its norm is <b>not</b> distance to the optimum; it need not point straight at it.'),
('p', '<b>η too big:</b> overshoot/diverge; <b>too small:</b> slow. Adaptive example: η<sub>k</sub> = 1/k. <b>tol↓:</b> more accurate/more steps; <b>tol↑:</b> faster/less accurate. Course: η, tol are <b>algorithm settings, not model hyperparameters</b>; no CV.'),
('p', '<b>Scale:</b> unequal feature magnitudes → elongated bowl → zig-zag/slow GD. Scaling improves conditioning, not convexity.'),
('p', '<b>Convex:</b> ∇²J = (2/M)XᵀX ≥ 0. Full column rank → strictly convex bowl, unique global minimum.'),
('e', 'Least squares: ŵ = (XᵀX)<super>−1</super>Xᵀy'),
('p', 'Closed form if invertible; costly at scale. GD is numerical.'),
('h', '2  REGULARIZATION: FIT + PENALTY'),
('e', 'Ridge: J = MSE + λ‖w‖₂<super>2</super>'),
('e', 'Lasso: J = MSE + λ‖w‖₁'),
('e', 'ElasticNet: J = MSE + λ₁‖w‖₁ + λ₂‖w‖₂<super>2</super>'),
('p', '‖w‖₁ = ∑ⱼ|wⱼ|; ‖w‖₂<super>2</super> = ∑ⱼwⱼ<super>2</super>. <b>λ↑:</b> more shrinkage/regularization, less overfit; too large → underfit. λ is a <b>model hyperparameter</b>.'),
('p', '<b>Ridge:</b> smooth; closed form or plain GD. ∇J = ∇MSE + 2λw.'),
('p', '<b>Lasso:</b> sets some weights <b>exactly to 0</b> (feature selection). |w| is nondifferentiable at 0 → no plain GD/general closed form; use subgradient/coordinate descent. ElasticNet has the same issue.'),
('p', '<b>ElasticNet:</b> λ₁ = 0 gives Ridge; λ₂ = 0 gives Lasso. Ideal tuning including endpoints can match either’s best selection score; tuning two parameters costs more. Neither Ridge nor Lasso always wins.'),
('s', 'Slides penalize w₀. If the intercept is excluded, omit its penalty and penalty-gradient term.'),
('h', '3  LOGISTIC REGRESSION + DERIVATIONS'),
('e', 'pᵢ = P(yᵢ = 1 | xᵢ) = σ(zᵢ) = 1/(1 + e<super>−zᵢ</super>)'),
('e', 'σ′(z) = e<super>−z</super>/(1 + e<super>−z</super>)<super>2</super> = σ(z)[1 − σ(z)]'),
('p', '<b>Split:</b> [1/(1 + e<super>−z</super>)]·[e<super>−z</super>/(1 + e<super>−z</super>)]. Factor 1 = σ(z); factor 2 = [(1 + e<super>−z</super>) − 1]/(1 + e<super>−z</super>) = 1 − σ(z).'),
('e', 'J = BCE = −(1/M) ∑ᵢ [yᵢ ln pᵢ'),
('e', '                         + (1 − yᵢ) ln(1 − pᵢ)]'),
('p', '<b>y = 1:</b> loss −ln p. <b>y = 0:</b> loss −ln(1 − p). Confident correct → 0; confident wrong → ∞. Independent Bernoulli likelihood: L = ∏ᵢ pᵢ<super>yᵢ</super>(1 − pᵢ)<super>1−yᵢ</super>; BCE = −ln L/M.'),
('e', '∂ℓᵢ/∂pᵢ = (pᵢ − yᵢ)/[pᵢ(1 − pᵢ)]'),
('e', '∂pᵢ/∂wⱼ = pᵢ(1 − pᵢ)xᵢⱼ'),
('e', '⇒ ∂J/∂wⱼ = (1/M) ∑ᵢ (pᵢ − yᵢ)xᵢⱼ'),
('e', '⇒ ∇J = Xᵀ(p − y)/M'),
('p', '<b>Why BCE?</b> Convex in w; sigmoid-MSE is nonconvex. No closed form → GD in class. Regularized classification = BCE + the same penalties.'),
('p', 'Predict 1 if p ≥ threshold (0.5 ⇔ z ≥ 0). Multi-class: categorical cross-entropy. Perfect separation: unregularized weights can diverge; <b>no finite max-margin convergence</b>.'),
],
[
('h', '4  SUPPORT VECTOR MACHINES'),
('p', '<b>Large margin</b> aids generalization. f = b + vᵀx; v = slopes (<b>norm excludes b</b>). Labels: <b>−1, +1</b>.'),
('e', 'Boundary: f = 0; parallel support planes: f = ±a'),
('e', 'Point-to-boundary distance = |f(x)|/‖v‖₂'),
('e', 'Full margin = 2a/‖v‖₂; normalize a = 1'),
('p', '<b>Derive:</b> subtract support-plane equations → projected separation × ‖v‖ = 2a. Max margin ⇔ min ‖v‖ <b>subject to no margin violations</b>. Without constraints: v = 0.'),
('e', '<b>Hard margin:</b> min ‖v‖; yᵢf(xᵢ) ≥ 1 for all i'),
('p', 'Requires separability. Support vectors touch the margin; soft-margin violations can also be support vectors.'),
('e', '<b>Soft margin:</b> H = ∑ᵢ max(0, 1 − yᵢzᵢ) + λ‖w‖₂<super>2</super>'),
('p', 'Score zᵢ = wᵀxᵢ; signed margin mᵢ = yᵢzᵢ. <b>Hinge:</b> hᵢ = max(0, 1 − mᵢ).'),
('p', '<b>m ≥ 1:</b> correct, outside/on margin → loss 0.<br/><b>0 &lt; m &lt; 1:</b> correct but inside margin → 1 − m.<br/><b>m = 0:</b> on boundary → 1.<br/><b>m &lt; 0:</b> misclassified → loss &gt; 1.'),
('p', '<b>λ↑:</b> wider margin, more regularization/tolerance of violations; too high → underfit. <b>λ↓:</b> narrower margin, less regularization; too low → overfit. <b>C ∝ 1/λ</b> acts oppositely.'),
('p', '<b>Convex, nonsmooth at m = 1</b> → GD extensions (or quadratic programming). Kernel SVM handles nonlinear boundaries; costly for big data. Scale features.'),
('p', 'SVC needs extensions for probabilities. Soft margins tolerate outliers; logistic optimizes BCE.'),
('p', '<b>SVR:</b> regression; course: “outermost” support vectors. Zero loss inside ε-tube; penalize observations outside.'),
('h', '5  MULTI-CLASS: ONE TARGET, C CLASSES'),
('p', '<b>KNN/trees:</b> multiple classes by votes; odd K can still tie (2–2–1). Binary logistic/SVM need extensions.'),
('p', '<b>OvR = OvA:</b> <b>C</b> models, c vs rest; pick largest positive-class score. Several say 1 → most confident positive; all 0 → least confident negative.'),
('p', '<b>OvO:</b> train <b>C(C − 1)/2</b> models, one per pair using only that pair’s data. Majority vote; confidence breaks ties. C = 6 → 15 models.'),
('p', '<b>OvR:</b> linear count, more imbalance (under/oversampling can help). <b>OvO:</b> quadratic count, smaller datasets; can be faster for few classes/large data. Neither always wins.'),
('h', '6  METRICS: READ THE MATRIX AXES FIRST'),
('p', 'With <b>rows = actual, columns = predicted</b>, for class c:<br/><b>TP:</b> diagonal cell; <b>FP:</b> other entries in its column;<br/><b>FN:</b> other entries in its row; TN = M − TP − FP − FN.'),
('e', 'P<sub>c</sub> = TP/(TP + FP) = diagonal / column sum'),
('e', 'R<sub>c</sub> = TP/(TP + FN) = diagonal / row sum'),
('e', 'Macro P = (1/C)∑<sub>c</sub>P<sub>c</sub>; macro R = (1/C)∑<sub>c</sub>R<sub>c</sub>'),
('p', '<b>Macro = equal class weights.</b> Bad minority performance hurts; not a support-weighted average.'),
('e', 'Micro P = ∑TP/(∑TP + ∑FP)'),
('e', 'Micro R = ∑TP/(∑TP + ∑FN)'),
('p', '<b>Micro = pool counts first.</b> Majority dominates, can hide minority failure. Single-label multi-class, all classes: <b>micro P = micro R = accuracy</b>.'),
('p', '<b>Accuracy:</b> sum diagonal / M; uniform-guess baseline 1/C. <b>ROC-AUC:</b> one OvR curve/AUC per class.'),
('h', '7  MULTI-LABEL: L TARGETS PER OBSERVATION'),
('p', '<b>Binary relevance:</b> L independent models; ignores target correlations. <b>Label powerset:</b> one class per label combination; classification only, up to 2<super>L</super> classes → impractical.'),
('p', '<b>Classifier/regressor chain:</b> L models, adding previous target predictions to x; uses target correlations. Order matters; errors can propagate.'),
('e', 'Hamming loss = (1/(ML))∑ᵢ∑<sub>l</sub>I(yᵢ<sub>l</sub> ≠ ŷᵢ<sub>l</sub>)'),
('p', '<b>Wrong labels / all entries.</b> Lower is better; 0 = perfect. For continuous responses, pool entries for RMSE/MAE.'),
('s', '1 − Hamming loss = labelwise accuracy (slides call it “Jaccard”). Standard Jaccard = TP/(TP + FP + FN), comparing positive-label sets.'),
],
[
('h', '8  K-MEANS + LLOYD’S ALGORITHM'),
('p', '<b>No target y.</b> Input <b>K</b>; hard labels, no probabilities/noise. Course: Gaussian, diagonal Σ (uncorrelated). Favors round clusters. Scale.'),
('e', '<b>Assignment:</b> cᵢ = arg min<sub>c</sub> ‖xᵢ − μ<sub>c</sub>‖₂'),
('e', '<b>Update:</b> μ<sub>c</sub> = (1/n<sub>c</sub>) ∑<sub>i:cᵢ=c</sub>xᵢ'),
('p', 'Initialize labels → update first; centroids → assign first. Alternate until stable. Different starts → different <b>local optima</b>; restarts/spread-out seeds (K-Means++) help.'),
('e', '<b>Inertia:</b> I = ∑ᵢ ‖xᵢ − μ<sub>cᵢ</sub>‖₂<super>2</super>'),
('p', 'I ≥ 0; optimum nonincreasing as K↑; K = M → 0. <b>Elbow:</b> K where decrease slows sharply. Lowest inertia alone overselects K; elbow can be unclear.'),
('h', '9  K-MEANS EXTENSIONS'),
('p', '<b>K-Modes:</b> categorical features; centroid = featurewise <b>mode</b>, assignment by <b>matching dissimilarity</b> d<sub>cat</sub>(x, u) = ∑ⱼ I(xⱼ ≠ uⱼ), the number of mismatches.'),
('p', '<b>K-Prototypes:</b> mixed numeric + categorical; mean for numeric coordinates, mode for categorical.'),
('e', 'd<sub>total</sub> = d<sub>Euclidean,numeric</sub> + γd<sub>cat</sub>  [course formula]'),
('p', 'γ balances continuous distances vs integer mismatch counts so neither dominates. E.g. [red, large, metal] vs [red, small, wood] → 0 + 1 + 1 = <b>2</b> mismatches.'),
('p', '<b>K-Medoids:</b> <b>actual observation</b> minimizing total distance to its cluster’s points. Assign to nearest medoid. More robust to outliers than means; more computation.'),
('h', '10  GMM: SOFT CLUSTERS + EM'),
('p', 'Input C; μ<sub>c</sub>: N-vector mean, Σ<sub>c</sub>: N×N covariance, π<sub>c</sub>: weight. Full Σ allows tilted/correlated clusters. Still Gaussian; no noise label. Scale features (course).'),
('e', 'p(x) = ∑<sub>c</sub> π<sub>c</sub>φ<sub>c</sub>(x); π<sub>c</sub> ≥ 0, ∑<sub>c</sub>π<sub>c</sub> = 1'),
('p', 'φ<sub>c</sub>(x) = Gaussian density N(x | μ<sub>c</sub>, Σ<sub>c</sub>).'),
('p', '<b>E-step:</b> parameters → probabilities (Bayes). C responsibilities per point, summing to 1.'),
('e', 'τᵢ<sub>c</sub> = P(c | xᵢ) = π<sub>c</sub>φ<sub>c</sub>(xᵢ) / ∑<sub>r</sub>π<sub>r</sub>φ<sub>r</sub>(xᵢ)'),
('p', '<b>M-step:</b> probabilities → parameters (maximize expected complete-data log-likelihood). Soft count n<sub>c</sub> = ∑ᵢτᵢ<sub>c</sub>.'),
('e', 'μ<sub>c</sub> = ∑ᵢτᵢ<sub>c</sub>xᵢ/n<sub>c</sub>;    π<sub>c</sub> = n<sub>c</sub>/M'),
('e', 'Σ<sub>c</sub> = ∑ᵢτᵢ<sub>c</sub>(xᵢ − μ<sub>c</sub>)(xᵢ − μ<sub>c</sub>)ᵀ/n<sub>c</sub>'),
('p', 'Use <b>new μ</b> in Σ; denominator n<sub>c</sub>, not n<sub>c</sub> − 1. Larger τ → more influence. <b>π<sub>c</sub> = average membership over points</b>; τᵢ<sub>c</sub> = one point’s membership.'),
('p', 'Initialize → E → M → E … until stable. E gets parameters from <b>previous M</b>; M uses latest E probabilities. Hard label = largest τ.'),
('p', '<b>E ↔ Assignment; M ↔ Update.</b> Practice: hard 0/1 probabilities + diagonal Σ ⇒ Lloyd is <b>true in course</b>. Exact Euclidean form: shared σ²I, equal weights (or small-variance limit).'),
('e', '<b>BIC</b> = −2 ln L + q ln M;    L = ∏ᵢ p(xᵢ)'),
('p', '<b>Lower BIC wins.</b> More clusters: likelihood↑ (term 1↓), parameter count q↑ (term 2↑). Balances fit vs complexity.'),
('p', '<b>Generative:</b> estimates source density; generate by choosing c via π, then sampling x from its Gaussian.'),
('h', '11  DB-SCAN + SILHOUETTE + HIERARCHY'),
('p', '<b>DB-SCAN:</b> nonparametric, arbitrary shapes, outliers; <b>no K input</b>. Radius ε (= tol); min_samples sets density (course: min cluster size). Grow via nearby points; isolated/sparse groups → noise. Scale.'),
('p', '<b>tol too large:</b> joins distinct clusters. <b>Too small:</b> fragments clusters/more noise. min_samples↑ rejects more sparse groups. Sensitive to radius; varying densities are hard → OPTICS/HDBSCAN (more computation).'),
('e', '<b>Silhouette:</b> s = (b − a)/max(a, b), in [−1, 1]'),
('p', '<b>Slides:</b> a = avg point-to-own-centroid distance; b = avg centroid-pair distance. 1 = separated; 0 = overlap; negative = poor assignment. Applicable across clustering models; inertia/elbow poor for DB-SCAN.'),
('s', 'Standard: a = mean distance to own-cluster peers; b = nearest other cluster’s mean distance; average sᵢ. Follow the question’s convention.'),
('p', '<b>Agglomerative:</b> singletons → merge. <b>Divisive:</b> one cluster → split. Dendrogram height = distance; a horizontal cut sets clusters. Good for small data; costly/messy at scale. Mini-batch K-Means/BIRCH help large data.'),
]
]

# Balance the columns while retaining a distinct heading for each topic.
hierarchy = COLS[2].pop()
COLS[0].extend([('h', 'HIERARCHY + LARGE DATA'), hierarchy])
for col in COLS:
    for i, (kind, txt) in enumerate(col):
        if kind == 'h':
            col[i] = (kind, re.sub(r'^\d+  ', '', txt).replace(' + HIERARCHY', ''))

W, H = 612, 792  # US Letter, portrait, exactly one side
MARGIN, GAP = 18, 10
CW = (W - 2*MARGIN - 2*GAP)/3
TOP, BOTTOM = 774, 18
INK = colors.HexColor('#151515')
ACCENT = colors.HexColor('#3f285d')
LIGHT = colors.HexColor('#efebf4')

missing = set()
def fallback(text):
    # Arial Narrow needs fallback glyphs for math. Preserve XML markup.
    text = text.replace('ᵢ', '<sub>i</sub>').replace('ⱼ', '<sub>j</sub>').replace('ᵀ', '<super>T</super>').replace('ᴺ', '<super>N</super>')
    # Keep mathematical indices within the line instead of touching the next row.
    text = text.replace('<sub>', '<sub size="6.2" rise="1.2">')
    text = text.replace('<super>', '<super size="6.2" rise="2.4">')
    parts = re.split(r'(<[^>]+>)', text)
    chars = pdfmetrics.getFont('N').face.charWidths
    for i in range(0, len(parts), 2):
        out = []
        for ch in parts[i]:
            if ord(ch) not in chars:
                if ord(ch) not in pdfmetrics.getFont('U').face.charWidths:
                    missing.add(ch)
                out.append(f'<font name="U">{ch}</font>')
            else:
                out.append(ch)
        parts[i] = ''.join(out)
    return ''.join(parts)

def styles(scale):
    return {
        'p': ParagraphStyle('body', fontName='N', fontSize=9.0*scale,
                            leading=9.8*scale, textColor=INK,
                            spaceAfter=1.0*scale),
        'e': ParagraphStyle('equation', fontName='N', fontSize=9.2*scale,
                            leading=10.3*scale, textColor=INK,
                            spaceAfter=.7*scale),
        's': ParagraphStyle('small', fontName='N', fontSize=8.2*scale,
                            leading=9.0*scale, textColor=colors.HexColor('#333333'),
                            spaceAfter=1.2*scale),
        'h': ParagraphStyle('heading', fontName='NB', fontSize=9.5*scale,
                            leading=10.8*scale, textColor=ACCENT,
                            spaceAfter=2.0*scale, spaceBefore=3*scale),
    }

def measure(col, scale):
    st=styles(scale)
    total=0
    items=[]
    for kind, txt in col:
        p=Paragraph(fallback(txt), st[kind])
        width=CW-6 if kind=='h' else CW
        _,height=p.wrap(width, 3000)
        before=st[kind].spaceBefore if items else 0
        after=st[kind].spaceAfter
        if kind=='h':height+=4
        total+=before+height+after
        items.append((kind,p,height,before,after))
    return total,items

# Fixed readable typography: fail and edit content instead of silently shrinking.
SCALE=.98
for i,col in enumerate(COLS):
    height,_=measure(col,SCALE)
    print(f'Column {i+1}: {height:.1f} pt; available {TOP-BOTTOM:.1f} pt')
    if height>TOP-BOTTOM:
        raise ValueError(f'Column {i+1} overflows by {height-(TOP-BOTTOM):.1f} pt')
if missing:raise ValueError(f'Unsupported glyphs: {missing}')

c=canvas.Canvas(str(OUT), pagesize=(W,H), pageCompression=1)
c.setTitle('STAT 362 Midterm - One-sided Letter Cheat Sheet')
c.setAuthor('Prepared for Adi Rosenstock from STAT 362 course materials')
c.setSubject('Midterm reference through Clustering 3; no Python or dimensionality reduction')

for ci,col in enumerate(COLS):
    x=MARGIN+ci*(CW+GAP)
    y=TOP
    _,items=measure(col,SCALE)
    for kind,p,height,before,after in items:
        y-=before
        if kind=='h':
            c.setFillColor(LIGHT)
            c.rect(x-2,y-height,CW+4,height,fill=1,stroke=0)
            p.drawOn(c,x+3,y-height+2)
        else:
            p.drawOn(c,x,y-height)
        y-=height+after
    print(f'Column {ci+1} bottom: {y:.1f}')
    if ci<2:
        c.setStrokeColor(colors.HexColor('#d5d0db'));c.setLineWidth(.35)
        c.line(x+CW+GAP/2,BOTTOM,x+CW+GAP/2,TOP)

c.showPage();c.save()
r=PdfReader(OUT)
assert len(r.pages)==1
assert tuple(float(x) for x in r.pages[0].mediabox)==(0,0,612,792)
print('Created:',OUT)
print('Words:',len(r.pages[0].extract_text().split()))
