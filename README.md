# pointypoints

My first python project!

Not yet hosted.

[Userscript repo](https://github.com/xorus/twitch-channel-points-logger)

## run

Copy .env.dist to .env, set it up and load it into your env.

`poetry install`
`./start.sh`

Install database `poetry run alembic upgrade head`.

There is also a docker image with a docker-compose provided. It will automatically run the database migration command.
Since this is a work in progress, the image is not yet hosted (but will be once I set up some CI).

## privacy

In the following paragraphs, "app" refers to the current instance of this server code.

- [Database structure code](https://github.com/xorus/pointypoints/blob/main/app/db/models.py)

### Twitch Login process

Collected data from Twitch:

- user id
- display name
- profile picture

Your display name and profile picture will be displayed on the webapp pages, so you can see with which account you are
logged in as. This information is only saved in your session and is **not** stored in the database.

Only info about your twitch account stored will be your hashed (using sha256) Twitch user id, so we can map your user id
to your point logs. This operation is not reversible, meaning a database administrator cannot personally identify your
Twitch account id. Hence, your Twitch account id is not stored in the database.

It might be unnecessary, but I really hate handling personal information of any kind, so I'm minimizing it to a maximum.
If I ever want to make a feature to compare user points or display names, it will be on an opt-in basis.

[Login code](https://github.com/xorus/pointypoints/blob/main/app/security.py)

### Point Counts

Point count logs include the following data:

- unique id for the record
- your app user id
- date time
- the point value
- channel name in plaintext

### Cookies

A session cookie will be used. The session cookie will contain your login information:

- App user id
- Twitch display name
- Twitch profile picture link

Don't worry, the cookie will be baked at the right temperature and duration to ensure perfect cookieness.
