from app import app, db
from models import Forum
# run pip install python-slugify
from slugify import slugify

# running this file is essential to getting everything to work correctly!
# make sure to run python add_forum_data.py in the terminal

# create the Forum table
with app.app_context():
    db.create_all()

# add data
with app.app_context():
    forums_data = [
        {
            'title': 'Random Corner',
            'description': 'This forum is a digital retreat for spontaneous and diverse conversations. Embrace the unexpected as we navigate through a kaleidoscope of topics, from lighthearted banter to profound musings.',
            'image_filename': 'random.jpg'
        },
        {
            'title': 'Developer Corner',
            'description': 'This forum is the hub for passionate developers, programmers, and tech enthusiasts to discuss and explore all things related to software development, coding, and technology. Get programming tips, debugging solutions, and share your latest project.',
            'image_filename': 'developer.jpg'
        },
        {
            'title': 'Indie Games Corner',
            'description': 'This forum is a haven for exploring the world of indie games and the innovative creations of game developers on our platform. Discuss indie game gems, share your favorite discoveries, and connect with the talented developers behind these unique experiences.',
            'image_filename': 'indie.jpg'
        },
        {
            'title': 'PC Corner',
            'description': 'This forum is your go-to destination for all things related to PC gaming, hardware, and software. Join in on discussions about the latest PC games, hardware upgrades, troubleshooting, optimization tips and more.',
            'image_filename': 'pc.jpg'
        },
        {
            'title': 'Nintendo Corner',
            'description': 'This forum is where you can engage in lively discussions about your favorite Nintendo games, consoles, and the iconic characters that make them special. Get nostalgic, exchange gaming tips, and explore the latest Nintendo news.',
            'image_filename': 'nintendo.jpg'
        },
        {
            'title': 'Xbox Corner',
            'description': 'This forum is dedicated to all things Xbox, where gamers come together to discuss the latest Xbox games, consoles, and everything in between. You can share your achievements, seek multiplayer partners, and stay up-to-date on Xbox news and releases.',
            'image_filename': 'xbox.jpg'
        },
        {
            'title': 'PlayStation Corner',
            'description': 'This forum is the gathering place for PlayStation enthusiasts to discuss the latest games, consoles, and experiences. Share gaming tips, seek co-op partners, and stay informed about PlayStation news and updates.',
            'image_filename': 'playstation.jpg'
        }
    ]

    for forum_data in forums_data:
        # generate a slug for each forum entry
        forum_data['slug'] = slugify(forum_data['title'])

        # create a Forum object and add it to the database
        new_forum = Forum(**forum_data)
        db.session.add(new_forum)

    db.session.commit()