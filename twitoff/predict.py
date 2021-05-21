''' Handles DS prediction model '''
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    '''
    Determines which user is more likely to say a given hypothetical tweet.

    Example run: predict_user('elonmusk', 'jackblack', 'Doge to the moon!')
    Return a 0 for (user0_name) and a 1 for (user1_name)
    '''

    # Grabs users from our Database
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # Grabs tweets from our Database corresponding to their user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically Stack vectors together ([<user0_tweets>, <user1_tweets>])
    vects = np.vstack([user0_vects, user1_vects])

    # Creating labels of len(vects)
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # Create Logistic Regression model
    log_reg = LogisticRegression().fit(vects, labels)
    hypo_tweet_text = vectorize_tweet(hypo_tweet_text).reshape(1, -1)
    return log_reg.predict(hypo_tweet_text)
