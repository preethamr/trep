import math
import re


# Build a hash table for all negative tokens
def parseNegative():

    nwords = {}
    nf = open('../data/negative-words.txt', 'r')

    for line in nf:
        line = line.strip()
        line = line.lower()
        if line and line[0] == ';':
            continue

        nwords[line] = True
    nf.close()
    return nwords

# Build a hash table for all positive tokens
def parsePositive():

    pwords = {}
    pf = open('../data/positive-words.txt', 'r')

    for line in pf:
        line = line.strip()
        line = line.lower()
        if line and line[0] == ';':
            continue

        pwords[line] = True

    pf.close()
    return pwords

nwords = parseNegative() 
pwords = parsePositive()

# Perform very basic sentiment analysis on the tweet
def parseTweet(tweet):
    
    # Tokonize on punctuations
    tokens = tokenize(tweet)

    positive = 0
    negative = 0 
    total = 0.0

    for word in tokens:
        word = word.strip()
        word = word.lower()
        if nwords.get(word):
            negative += 1
        if pwords.get(word):
            positive += 1
        total += 1

    return (positive, negative, total)

# Split into words
def tokenize(t):
    
    # User #hashtags and @snames as match words
    tweet = t.get('text')
    if tweet:
            # Replace #hashtag with hashtag 
            tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
            # Replace @username with username 
            tweet = re.sub(r'@([^\s]+)', r'\1', tweet)
            # Remove additional white spaces
            tweet = re.sub('[\s]+', ' ', tweet)

            return tweet.split()

    return None

# Combine reputation combonents at the root level of the user graph.
# Root level: Baseline score(50%), sentiment(25%), follower count score(12.5%), follower graph score(12.5%)
# Leaf level: Baseline score(50%), follower count score(50%)
def scoreUser((p, n, t), f_count, f_scores):
    
    # Score the profile
    full = 650

    baseline = full/2.0


    # Sentiment component
    s_factor = 0
    if (p + n) > 0:
        s_factor = float((p - n))/(p + n)

    sentiment = (full/4.0) * s_factor

    # Followers component with exponential decay with upper limit
    # Plateau around 50K followers
    decay = 0.00009
    follow = (full / 8.0) * (1 - math.exp(-1 * (decay * f_count)))

    # Followers reputation component
    f_score = 0
    if f_scores:
        f_score = (full / 8.0) * sum(f_scores)/( len(f_scores) * full)

    return int(baseline + sentiment + follow + f_score)

    
# Combine reputation combonents at the leaf level of the user graph.
# Leaf level: Baseline score(50%), follower count score(50%)
def scoreFollower(f_user):
    
    # Score the profile
    full = 650

    baseline = full/2.0

    # Followers component with exponential decay with upper limit
    # Plateau around 50K followers
    decay = 0.00009
    follow = (full/2.0) *(1 - math.exp(-1 * (decay * f_user.followers_count)))

    return int(baseline + follow)
