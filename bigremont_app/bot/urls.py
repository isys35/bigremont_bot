from bigremont_app.bot.views import welcome

urls = [
    (r'<wc:req>/start', welcome),
    ]