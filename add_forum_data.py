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
            'title': 'Developer Corner',
            'description': 'Welcome to the Developer Corner! This forum is the hub for passionate developers, programmers, and tech enthusiasts to discuss and explore all things related to software development, coding, and technology. Whether youre looking for programming tips, debugging solutions, or want to share your latest project, this is the place to connect with fellow developers. Join us in discussions on coding languages, frameworks, best practices, and stay updated with the latest trends in the tech world. Lets learn, share, and code together in the Developer Corner!'
        },
        {
            'title': 'PC Corner',
            'description': 'Dive into the world of PC gaming and computer technology! This forum is your go-to destination for all things related to PC gaming, hardware, and software. Join fellow gamers and tech enthusiasts in discussions about the latest PC games, hardware upgrades, troubleshooting, and optimization tips. Whether youre a seasoned gamer or new to the world of PC gaming, this is the place to share your experiences, seek recommendations, and stay updated on the exciting developments in the PC gaming and technology realm. Explore the PC Corner and level up your gaming and computer knowledge!'
        },
        {
            'title': 'Nintendo Corner',
            'description': 'Where the world of Nintendo gaming comes to life! Join the Nintendo gaming forum in lively discussions about your favorite Nintendo games, consoles, and the iconic characters that make them special. Whether youre a fan of Mario, Zelda, Pokémon, or any of Nintendos beloved franchises, this is the place to share your passion, exchange gaming tips, and explore the latest Nintendo news. Dive into nostalgia or discover new adventures with fellow Nintendo enthusiasts. The Nintendo Corner is your portal to the colorful and exciting world of Nintendo gaming!'
        },
        {
            'title': 'Xbox Corner',
            'description': 'Your gateway to the Xbox gaming universe! This forum is dedicated to all things Xbox, where gamers come together to discuss the latest Xbox games, consoles, and everything in between. Join the community to share your achievements, seek multiplayer partners, and stay up-to-date on Xbox news and releases. Whether youre a fan of Halo, Forza, or any Xbox-exclusive titles, this is the hub for Xbox enthusiasts. Dive into the Xbox Corner, where gaming adventures and camaraderie await!'
        },
        {
            'title': 'PlayStation Corner',
            'description': 'Immerse yourself in the world of PlayStation gaming! This forum is the gathering place for PlayStation enthusiasts to discuss the latest games, consoles, and experiences. Join fellow gamers to explore titles like God of War, Uncharted, and many more. Share gaming tips, seek co-op partners, and stay informed about PlayStation news and updates. Whether youre a long-time PlayStation fan or just discovering the magic of Sonys gaming world, the PlayStation Corner is where you belong. Get ready to embark on epic gaming journeys and connect with fellow PlayStation players!'
        },
        {
            'title': 'Indie Games Corner',
            'description': 'Celebrating creativity in gaming! Welcome to the Indie Games Corner, your haven for exploring the world of indie games and the innovative creations of game developers on our platform. Join the community to discuss indie game gems, share your favorite discoveries, and connect with the talented developers behind these unique experiences. Whether youre a fan of pixel art, story-driven adventures, or experimental gameplay, this is where you can celebrate and support indie game development. Dive into a world of originality, playtest upcoming titles, and be a part of the indie gaming revolution right here in the Indie Games Corner!'
        }
    ]

    for forum_data in forums_data:
        # generate a slug for each forum entry
        forum_data['slug'] = slugify(forum_data['title'])

        # create a Forum object and add it to the database
        new_forum = Forum(**forum_data)
        db.session.add(new_forum)

    db.session.commit()