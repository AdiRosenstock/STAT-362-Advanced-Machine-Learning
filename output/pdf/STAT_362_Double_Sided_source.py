"""Print all practice parts with selected answers, plus remaining review details."""
from pathlib import Path
import hashlib
import re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, NumberObject, BooleanObject

ROOT = Path('/Users/adirosenstock/Downloads/Northwestern/Senior_Year/Q1/STAT_362')
FRONT = ROOT / 'output/pdf/STAT_362_Midterm_Cheat_Sheet.pdf'
OUT = ROOT / 'output/pdf/STAT_362_Midterm_Double_Sided.pdf'
TMP = ROOT / 'tmp/pdfs'
TMP.mkdir(parents=True, exist_ok=True)
BACK = TMP / 'STAT_362_Practice_Back.pdf'

# Reuse only font registration and layout helpers; do not regenerate the front.
ns = {}
exec((ROOT / 'output/pdf/STAT_362_Midterm_Cheat_Sheet_source.py').read_text().split('# Fixed readable typography')[0], ns)
fallback = ns['fallback']
W, H, MARGIN, GAP = 612, 792, 18, 10
CW = (W - 2*MARGIN - 2*GAP)/3
TOP, BOTTOM = 774, 18
INK = colors.HexColor('#151515')
ACCENT = colors.HexColor('#3f285d')
LIGHT = colors.HexColor('#efebf4')

# Retain the original choices as source data; print only officially selected answers.
MC = [
('1(a)', 'In each step of gradient descent, why is the step taken in the opposite direction of the gradient vector (i.e. −∇MSE)?', [
 'The gradient vector points in the direction of steepest increase, so moving opposite to it decreases the cost fastest.',
 'The gradient vector always points directly at the global minimum.',
 'Moving along −∇MSE reaches the exact Least Squares solution in one step.',
 'The magnitude of the gradient vector equals the distance to the global minimum.',
], 'A'),
('1(b)', 'Why is the MSE cost not used to train a Logistic Regression model?', [
 'The MSE cost has a closed-form solution that is computationally too expensive for classification data.',
 'With the sigmoid inside it, the MSE cost is no longer a convex function, so gradient descent becomes very inefficient.',
 'An MSE cost cannot be computed when the true response values are 0s and 1s.',
 'The MSE cost causes overfitting to classification data.',
], 'B'),
('1(c)', 'If a classification dataset has six classes and a binary classifier is trained on it with the One-vs-One extension, how many binary classifiers are trained?', [
 '6', '12', '15', '30',
], 'C'),
('1(d)', 'A regression dataset has two numeric features: one ranges from 0 to 1, the other from 0 to 100,000. Without scaling, what happens when gradient descent is run on a Linear Regression model trained on this data?', [
 'The cost function becomes non-convex.',
 'Gradient descent cannot be used, and the closed-form solution is required.',
 'Gradient descent gets stuck in a local minimum.',
 'The cost function turns into an “elongated bowl”, so the algorithm zig-zags and becomes sensitive to the initialization point and the learning rate.',
], 'D'),
('1(e)', 'For a Support Vector Machine (SVM) classifier, which of the following optimization problems does maximizing the margin lead to?', [
 'Maximize ‖w‖, the norm of the parameter vector, with no constraints.',
 'Minimize ‖w‖, the norm of the parameter vector, with no constraints.',
 'Minimize ‖w‖, the norm of the parameter vector, subject to no observations lying inside the margin.',
 'Minimize the number of support vectors.',
], 'C'),
('1(f)', 'For a Gaussian Mixture Model (GMM) and the Expectation-Maximization (EM) algorithm that trains it, what do the cluster weights (π<sub>c</sub>’s) represent for clusters c = 1, …, C?', [
 'The probability that a specific observation belongs to cluster c, given the values of the observation.',
 'The determinant of the covariance matrix of cluster c.',
 'The average probability, across all observations in the data, of belonging to cluster c.',
 'The number of observations hard-assigned (without any probabilities) to cluster c.',
], 'C'),
]

MA = [
('2(a)', 'Which of the following statements are <b>TRUE</b> about Lasso Regression?', [
 'It can be optimized algebraically, but that approach is not useful for big data.',
 'It cannot use plain gradient descent, so extensions such as subgradient or coordinate descent are needed.',
 'It adds the L1-Norm of the parameter vector, which consists of the squared parameter values, to the cost function.',
 'It can drive some trained parameter values to exactly zero, and performs feature selection that way.',
], 'BD'),
('2(b)', 'Which of the following statements are <b>FALSE</b> about precision and recall for a multi-class classification task?', [
 'Macro precision/recall treats every class as equally important.',
 'Micro precision/recall treats every class as equally important.',
 'Micro precision/recall is defined to reflect a sharp decrease in performance due to a poorly predicted minority class.',
 'Macro precision/recall takes a weighted average of all (One-vs-Rest/binary) precision/recall values calculated for each class present in the data.',
], 'BCD'),
('2(c)', 'Which of the following statements are <b>TRUE</b> about shortcomings of a K-Means clustering model that are addressed by other clustering models?', [
 'DB-SCAN addresses finding possible outliers in the data.',
 'GMM addresses finding possible outliers in the data.',
 'DB-SCAN addresses non-Gaussian underlying sources.',
 'DB-SCAN addresses cluster probabilities for each observation.',
], 'AC'),
('2(d)', 'Which of the following statements are <b>FALSE</b> about the E-Step of the EM algorithm?', [
 'Assuming C clusters in the data, the E-Step always calculates C cluster probabilities for each observation.',
 'The E-Step uses Bayes’ rule to calculate the cluster probabilities from the data and the current model parameters.',
 'The current E-Step receives the current model parameters from the previous E-Step.',
 'Given the necessary assumptions, the E-Step of the EM algorithm becomes equivalent to the Update step of Lloyd’s algorithm.',
], 'CD'),
]

TF = [
('3(a)', 'For gradient descent, a smaller tolerance gives parameters closer to the closed-form (Least Squares) solution but takes more steps to converge.', True),
('3(b)', 'If two classes in a binary classification task are perfectly separable, a Logistic Regression model trained with gradient descent converges to the decision boundary with the largest margin between both classes.', False),
('3(c)', 'The classifier chain approach is applicable to a multi-class classification task with only one response/target variable.', False),
('3(d)', 'In the Hinge cost of an SVM model, increasing λ, the hyperparameter, shrinks the margin and reduces regularization.', False),
('3(e)', 'For a K-Means clustering model, inertia decreases monotonically as K (number of clusters) increases, and it equals 0 when K equals the number of observations.', True),
('3(f)', 'Assuming the variables with higher orders of magnitude are not necessarily more important than those with lower orders of magnitude in your unsupervised dataset, scaling is typically necessary before clustering the data with a K-Means model.', True),
('3(g)', 'The DB-SCAN model requires the number of clusters as an input.', False),
('3(h)', 'If all cluster probabilities become 0 or 1 and all covariance matrices become diagonal, the EM algorithm (for a GMM) becomes equivalent to Lloyd’s algorithm.', True),
]

SA = [
('h', 'Q4 SHORT ANSWER - QUESTIONS + SOLUTIONS'),
('q', '<b>4(a) [8 points]</b> In the gradient vector for the Mean Squared Error (MSE) cost, the partial derivative with respect to wⱼ (j = 1, …, N) is:'),
('e', '∂MSE/∂wⱼ = −(2/M)∑ᵢ(yᵢ − wᵀxᵢ)xᵢⱼ.'),
('q', 'Explain where the factor −2 and the term xᵢⱼ come from.'),
('a', '<b>Answer:</b> Start from MSE = (1/M)∑ᵢ(yᵢ − wᵀxᵢ)<super>2</super>. The outer derivative of the square gives 2(yᵢ − wᵀxᵢ). The chain rule supplies the inner derivative −xᵢⱼ, since wⱼxᵢⱼ is the only term of wᵀxᵢ that depends on wⱼ.'),
('e', '∂(yᵢ − wᵀxᵢ)<super>2</super>/∂wⱼ = 2(yᵢ − wᵀxᵢ)(−xᵢⱼ).'),
('gap', ''),
('q', '<b>4(b) [10 points]</b> The derivative of the sigmoid function (with respect to its only variable) can be written as:'),
('e', 'σ′(x) = e<super>−x</super>/(1 + e<super>−x</super>)<super>2</super>.'),
('q', 'Explain/Formulate how the right side of the equation above can be split into two factors and express the factors in terms of σ(x).'),
('a', '<b>Answer:</b> Split the squared denominator:'),
('e', 'σ′(x) = [1/(1 + e<super>−x</super>)]·[e<super>−x</super>/(1 + e<super>−x</super>)].'),
('a', 'The first factor is σ(x). In the second, add and subtract 1 in the numerator:'),
('e', 'e<super>−x</super>/(1 + e<super>−x</super>) = [(1 + e<super>−x</super>) − 1]/(1 + e<super>−x</super>)'),
('e', '= 1 − 1/(1 + e<super>−x</super>) = 1 − σ(x).'),
('e', '<b>Therefore σ′(x) = σ(x)[1 − σ(x)].</b>'),
('gap', ''),
('q', '<b>4(c) [9 points]</b> Explain what kind of dataset a K-Prototypes clustering model is useful for. For a K-Prototypes clustering model, find the matching dissimilarity between the categorical parts of the following two observations: <b>[red, large, metal]</b> and <b>[red, small, wood]</b>. Lastly, explain why the total distance equation for K-Prototypes multiplies the matching dissimilarity by a factor γ.'),
('a', '<b>Answer:</b> K-Prototypes is useful for a <b>mix of numeric and categorical variables</b>. Matching dissimilarity counts categorical mismatches:'),
('e', 'd = 0 (red = red) + 1 (large ≠ small)'),
('e', '      + 1 (metal ≠ wood) = <b>2</b>.'),
('e', 'Total distance = Euclidean distance + γ·d.'),
('a', 'The categorical distance is a nonnegative integer; the numeric Euclidean distance can be at any order of magnitude. <b>γ rescales one component so neither dominates</b> the total distance.'),
('gap', ''),
('q', '<b>4(d) [8 points]</b> The test confusion matrix for a three-class classification task is as follows:'),
('matrix', ''),
('q', 'Express the (One-vs-Rest/binary) precision and recall for the class <b>Bird</b> as fractions. You are not required to perform any calculations. (It is fine if you do.)'),
('a', '<b>Answer:</b> TP = 12 (Bird diagonal). FP = 2 + 1 = 3 (other entries in the Bird <b>column</b>). FN = 6 + 2 = 8 (other entries in the Bird <b>row</b>).'),
('e', '<b>Precision<sub>Bird</sub></b> = TP/(TP + FP) = 12/(12 + 3)'),
('e', '= <b>12/15</b> (= 4/5).'),
('e', '<b>Recall<sub>Bird</sub></b> = TP/(TP + FN) = 12/(12 + 8)'),
('e', '= <b>12/20</b> (= 3/5).'),
]

def choice_blocks(items):
    blocks=[]
    for label,question,options,answer in items:
        blocks.append(('q', f'<b>{label}</b> {question}'))
        selected=[opt for letter,opt in zip('ABCD',options) if letter in answer]
        if label.startswith('1('):
            assert len(selected)==1
            blocks.append(('a','<b>Answer:</b> '+selected[0]))
        else:
            lead='Select these FALSE statements' if 'FALSE' in question else 'Correct statements'
            blocks.append(('a','<b>'+lead+':</b><br/>'+'<br/>'.join('• '+opt for opt in selected)))
        blocks.append(('gap',''))
    return blocks

# These notes close the gap between the compact front and every subject in the
# attached Midterm_Review (1).html, while keeping the six MC answers unambiguous.
REVIEW_MODEL = [
 ('h','REVIEW: MODEL SETUP + GRADIENT DESCENT'),
 ('a','<b>Parametric model:</b> equation + cost + training algorithm. <b>GD:</b> approximate (“close enough”), applies to differentiable costs, efficient for big data. <b>Least squares:</b> exact/algebraic for linear and Ridge; costly at scale.'),
 ('e','GD step length = η‖∇J‖.'),
 ('a','Gradient shrinks near the minimum → smaller steps. Choose η, tol by rules of thumb/trial and error.'),
 ('a','<b>Scaling:</b> problems worsen with more features/larger magnitude gaps; initialization and η affect convergence.'),
 ('a','<b>Penalty:</b> balances fit against large weights.'),
 ('h','REVIEW: SVM DETAILS'),
 ('a','Linear SVM is <b>parametric, interpretable</b>; classification/regression, nonlinear with kernels. Support vectors: classifier = <b>innermost/closest to boundary</b>; regressor = outermost (course).'),
 ('a','<b>Extreme λ:</b> very low → vanishing margin/overfit; very high → weights toward 0, enormous (course: infinite) margin/underfit.'),
 ('a','SVC needs extensions for <b>probability thresholds</b>.'),
]
REVIEW_OTHER = [
 ('a','<b>OvR:</b> class c → 1, rest → 0; confidence = logistic probability or SVM signed boundary distance.'),
 ('a','Large feature values dominate Euclidean distances. K-Means/GMM assign all points to K clusters; DBSCAN automatically labels noise.'),
 ('a','<b>Elbow axes:</b> x = K, y = inertia; K = 1 gives maximum inertia, K = M gives 0. Medoid: minimize sum/average distance (equivalent).'),
 ('a','<b>EM stop:</b> μ, Σ, π, τ stable. GMM fits a PDF/generates data; other models in the review focus on values/classes/clusters (course: “discriminative”).'),
]
REVIEW_CHAIN = [
 ('a','<b>Chain:</b> f₁(X) → ŷ₁; f₂(X, ŷ₁) → ŷ₂; …, for L targets. <b>Hamming loss</b> = mean of (1 − accuracyᵢ), where accuracyᵢ is the fraction of labels correct within point i. Weighted metrics are not on the exam.'),
]
REVIEW_DBSCAN = [
 ('h','REVIEW: DBSCAN COURSE ALGORITHM'),
 ('a','Start at a random point. Add the nearest point if its distance to the cluster is &lt; tol; otherwise finalize and start a new cluster. Groups below min_samples become noise. Small tol changes can abruptly change the cluster count. Nonparametric: no Gaussian/source PDF is specified.'),
]

COLS=[
 [('h','Q1 QUESTIONS + CORRECT ANSWERS')] + choice_blocks(MC) + REVIEW_MODEL + REVIEW_OTHER,
 [('h','Q2 SELECTED ANSWERS')] + choice_blocks(MA)
 + [('h','Q3 TRUE / FALSE - OFFICIAL ANSWERS')]
 + [('t',f'<b>{label} {"TRUE" if answer else "FALSE"}.</b> {question}') for label,question,answer in TF]
 + REVIEW_CHAIN,
 SA + REVIEW_DBSCAN,
]

def styles(scale):
    return {
      'h':ParagraphStyle('h',fontName='NB',fontSize=9.5*scale,leading=10.6*scale,textColor=ACCENT,spaceBefore=3*scale,spaceAfter=2*scale),
      'q':ParagraphStyle('q',fontName='N',fontSize=9.0*scale,leading=9.8*scale,textColor=INK,spaceAfter=2*scale),
      'o':ParagraphStyle('o',fontName='N',fontSize=8.8*scale,leading=9.5*scale,textColor=INK,spaceAfter=0),
      't':ParagraphStyle('t',fontName='N',fontSize=9.0*scale,leading=9.8*scale,textColor=INK,spaceAfter=5*scale),
      'a':ParagraphStyle('a',fontName='N',fontSize=9.0*scale,leading=9.8*scale,textColor=INK,spaceAfter=2*scale),
      'e':ParagraphStyle('e',fontName='N',fontSize=9.2*scale,leading=10.3*scale,textColor=INK,spaceAfter=1.3*scale),
    }

def matrix(scale):
    cells=[['Actual ↓ / Predicted →','Cat','Dog','Bird'],['Cat','20','3','2'],['Dog','4','15','1'],['Bird','6','2','12']]
    sty=ParagraphStyle('m',fontName='N',fontSize=8.7*scale,leading=9.5*scale)
    cells=[[Paragraph(fallback(str(v)),sty) for v in row] for row in cells]
    tbl=Table(cells,colWidths=[CW*.49,CW*.17,CW*.17,CW*.17])
    tbl.setStyle(TableStyle([
       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BACKGROUND',(0,0),(-1,0),LIGHT),
       ('GRID',(0,0),(-1,-1),.35,colors.HexColor('#8b8492')),
       ('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
       ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
    ]))
    return tbl

def measure(col,scale):
    st=styles(scale);total=0;items=[]
    for kind,txt in col:
        if kind=='gap':items.append((kind,None,2*scale,0,0));total+=2*scale;continue
        if kind=='matrix':
            p=matrix(scale);_,height=p.wrap(CW,3000);before=2*scale;after=4*scale
        else:
            p=Paragraph(fallback(txt),st[kind]);_,height=p.wrap(CW-6 if kind=='h' else CW,3000)
            before=st[kind].spaceBefore if items else 0;after=st[kind].spaceAfter
            if kind=='h':height+=4
        items.append((kind,p,height,before,after));total+=height+before+after
    return total,items

SCALE=1.0
for ci,col in enumerate(COLS):
    height,_=measure(col,SCALE)
    print(f'Back column {ci+1}: {height:.1f} pt; available {TOP-BOTTOM}')
    if height>TOP-BOTTOM:raise ValueError(f'Column {ci+1} overflow: {height-(TOP-BOTTOM):.1f}')
assert not ns['missing'],ns['missing']

front_before=hashlib.sha256(FRONT.read_bytes()).hexdigest()
c=canvas.Canvas(str(BACK),pagesize=(W,H),pageCompression=1)
for ci,col in enumerate(COLS):
    x=MARGIN+ci*(CW+GAP);y=TOP
    _,items=measure(col,SCALE)
    for kind,p,height,before,after in items:
        y-=before
        if kind=='h':
            c.setFillColor(LIGHT);c.rect(x-2,y-height,CW+4,height,fill=1,stroke=0)
            p.drawOn(c,x+3,y-height+2)
        elif p:p.drawOn(c,x,y-height)
        y-=height+after
    if ci<2:
        c.setStrokeColor(colors.HexColor('#d5d0db'));c.setLineWidth(.35)
        c.line(x+CW+GAP/2,BOTTOM,x+CW+GAP/2,TOP)
c.showPage();c.save()

w=PdfWriter();w.append(str(FRONT));w.append(str(BACK))
w.add_metadata({'/Title':'STAT 362 Midterm - Front Cheat Sheet + Back Practice Questions and Answers',
                '/Author':'Prepared for Adi Rosenstock from STAT 362 course materials',
                '/Subject':'One US Letter sheet, double-sided, flip on long edge'})
w._root_object[NameObject('/ViewerPreferences')]=DictionaryObject({
    NameObject('/Duplex'):NameObject('/DuplexFlipLongEdge'),
    NameObject('/PrintScaling'):NameObject('/None'),
    NameObject('/NumCopies'):NumberObject(1),
    NameObject('/PickTrayByPDFSize'):BooleanObject(True),
})
with OUT.open('wb') as f:w.write(f)
assert front_before==hashlib.sha256(FRONT.read_bytes()).hexdigest()
r=PdfReader(OUT)
assert len(r.pages)==2
assert all(list(p.mediabox)==[0,0,612,792] and p.rotation==0 for p in r.pages)
assert r.pages[0].extract_text()==PdfReader(FRONT).pages[0].extract_text()
back_text=r.pages[1].extract_text()
for label in [f'1({a})' for a in 'abcdef']+[f'2({a})' for a in 'abcd']+[f'3({a})' for a in 'abcdefgh']+[f'4({a})' for a in 'abcd']:
    assert label in back_text,label
print('Created:',OUT)
print('Front preserved; two portrait Letter pages; long-edge duplex preference set.')
print('All 22 practice parts retained; only the 15 officially selected MC/MA choices printed.')
print('Review topics covered across the front and the additional back-page review notes.')
print('Back words:',len(back_text.split()))
