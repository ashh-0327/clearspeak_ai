from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

DOMAIN_KEYWORDS = {
    'bank_loan': ['loan', 'emi', 'interest', 'repayment', 'borrower', 'lender', 'principal', 'collateral', 'mortgage', 'credit', 'bank', 'sip', 'mutual fund', 'nav', 'nach', 'investment', 'installment'],
    'property': ['sale deed', 'property', 'land', 'plot', 'flat', 'apartment', 'ownership', 'registration', 'stamp duty', 'encumbrance', 'title', 'carpet area', 'possession', 'builder'],
    'contract': ['agreement', 'contract', 'parties', 'obligations', 'indemnity', 'arbitration', 'termination', 'penalty', 'breach', 'force majeure', 'confidential', 'jurisdiction', 'whereas', 'hereinafter']
}

DOMAIN_DESCRIPTIONS = {
    'bank_loan': 'loan EMI interest repayment borrower lender principal collateral mortgage credit bank SIP mutual fund NAV NACH investment installment',
    'property': 'sale deed property land plot flat apartment ownership registration stamp duty encumbrance title deed carpet area builder possession',
    'contract': 'agreement contract parties obligations indemnity arbitration termination penalty breach force majeure NDA confidential liquidated damages jurisdiction'
}

def detect_domain(text):
    text_lower = text.lower()
    keyword_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        keyword_scores[domain] = count
    text_embedding = model.encode([text[:1000]])
    embedding_scores = {}
    for domain, description in DOMAIN_DESCRIPTIONS.items():
        domain_embedding = model.encode([description])
        similarity = cosine_similarity(text_embedding, domain_embedding)[0][0]
        embedding_scores[domain] = float(similarity)
    combined_scores = {}
    total_keywords = max(sum(keyword_scores.values()), 1)
    for domain in DOMAIN_DESCRIPTIONS.keys():
        keyword_normalized = keyword_scores[domain] / total_keywords
        combined_scores[domain] = (keyword_normalized * 0.4) + (embedding_scores[domain] * 0.6)
    detected_domain = max(combined_scores, key=combined_scores.get)
    confidence = combined_scores[detected_domain]
    return {
        'domain': detected_domain,
        'confidence': round(confidence, 3),
        'all_scores': {k: round(v, 3) for k, v in combined_scores.items()}
    }
