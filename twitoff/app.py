''' Main app/routing file for Twitoff '''
from operator import add
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():
    '''Creates and configures an instance of the flask application'''
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.dqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/compare', methods=['POST'])
    def compare():
        # getting users and hypothetical tweet from client
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])
        hypo_tweet_text = request.values['tweet_text']

        # stops clients from comparing same user
        if user0 == user1:
            message = 'Cannot compare users to themselves!'

        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)
            message = '"{}" is more likely to be said by {} than {}'.format(
                hypo_tweet_text,
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} successfully added!'

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    # TODO: Update all users when button is clicked

    @app.route('/update')
    def update():
        pass

    @app.route('/populate')
    def populate():
        # insert_users(['elonmusk', 'jack'])
        # insert_tweets(['DOGE to the mooooon', 'all my movies suck',
        #                'born 69 days after 420', 'Starlink launch tonight',
        #                'I should have never been an actor', 'meme gawd'])
        add_or_update_user('elonmusk')
        add_or_update_user('jackblack')
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home', users=User.query.all())

    return app


# def insert_users(usernames):
#     for id_index, username in enumerate(usernames):
#         user = User(id=id_index, username=username)
#         DB.session.add(user)
#         DB.session.commit()


# def insert_tweets(tweets):
#     mylist = []
#     n = 0
#     while n <= 6:
#         id = n
#         text = random.choice(tweets)
#         user_id = random.randint(1, 2)
#         tweet = Tweet(id=id, text=text, user_id=user_id)
#         mylist.append(tweet)
#         n += 1
#     DB.session.add_all(mylist)
#     DB.session.commit()

    # for id, text, user_id in enumerate(tweets):
    #     tweet = Tweet(id=id, text=text, user_id=user_id)
    #     DB.session.add(tweet.user_id, tweet.text)
    #     DB.session.commit()
