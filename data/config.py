from environs import Env

# this is how we use environs library
env = Env()
env.read_env()

# reading data from .env file
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
admins = env.list("ADMINS")  # admin list
support_agents = env.list('SUPPORT_AGENTS')  # users that allowed to answer as spec. agent
