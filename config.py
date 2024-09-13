import os
from dotenv import load_dotenv, find_dotenv
valid_commands = [
    "/start",
    "Начать викторину 🦁",
    "Попробовать еще раз 🐘",
    "Поделиться результатом в соцсети 🦒",
    "Связаться со службой поддержки 📨",
    "Вернуться в главное меню 🐘"
]

creatures = [
    "aardvark", "albatross", "alligator", "alpaca", "ant", "anteater", "antelope", "ape", "armadillo", "donkey",
    "baboon", "badger", "barracuda", "bat", "bear", "beaver", "bee", "bison", "boar", "buffalo",
    "butterfly", "camel", "capybara", "caribou", "cassowary", "cat", "caterpillar", "cattle", "chamois", "cheetah",
    "chicken", "chimpanzee", "chinchilla", "chough", "clam", "cobra", "cockroach", "cod", "cormorant", "coyote",
    "crab", "crane", "crocodile", "crow", "curlew", "deer", "dinosaur", "dog", "dogfish", "dolphin",
    "dotterel", "dove", "dragonfly", "duck", "dugong", "dunlin", "eagle", "echidna", "eel", "eland",
    "elephant", "elk", "emu", "falcon", "ferret", "finch", "fish", "flamingo", "fly", "fox",
    "frog", "gaur", "gazelle", "gerbil", "giraffe", "gnat", "gnu", "goat", "goldfinch", "goosander",
    "goose", "gorilla", "goshawk", "grasshopper", "grouse", "guanaco", "guinea fowl", "guinea pig", "gull", "hamster",
    "hare", "hawk", "hedgehog", "heron", "herring", "hippopotamus", "hornet", "horse", "human", "hummingbird",
    "hyena", "ibex", "ibis", "jackal", "jaguar", "jay", "jellyfish", "kangaroo", "kingfisher", "koala",
    "kookaburra", "kouprey", "kudu", "lapwing", "lark", "lemur", "leopard", "lion", "llama", "lobster",
    "locust", "loris", "louse", "lyrebird", "magpie", "mallard", "manatee", "mandrill", "mantis", "marten",
    "meerkat", "mink", "mole", "mongoose", "monkey", "moose", "mosquito", "mouse", "mule", "narwhal",
    "newt", "nightingale", "octopus", "okapi", "opossum", "oryx", "ostrich", "otter", "owl", "ox",
    "oyster", "panther", "parrot", "partridge", "peafowl", "pelican", "penguin", "pheasant", "pig", "pigeon",
    "pike", "piranha", "platypus", "polar bear", "porcupine", "porpoise", "quail", "quelea", "quetzal", "rabbit",
    "raccoon", "rail", "ram", "rat", "raven", "red deer", "red panda", "reindeer", "rhinoceros", "rook",
    "salamander", "salmon", "sand dollar", "sandpiper", "sardine", "scorpion", "seahorse", "seal", "shark", "sheep",
    "shrew", "shrimp", "skunk", "snail", "snake", "sparrow", "spider", "spoonbill", "squid", "squirrel",
    "starfish", "stingray", "stoat", "stork", "swallow", "swan", "swift", "swordfish", "tahr", "takin",
    "tapir", "tarsier", "termite", "tiger", "toad", "trout", "turkey", "turtle", "viper", "vulture",
    "wallaby", "walrus", "wasp", "weasel", "whale", "wolf", "wolverine", "wombat", "woodcock", "woodpecker",
    "worm", "wren", "yak", "zebra", "zebu", "zokor", "arowana", "barramundi", "betta", "bluegill",
    "carp", "catfish", "clownfish", "coelacanth", "crappie", "cutthroat trout", "discus", "drum", "goby", "gourami",
    "guppy", "haddock", "halibut", "herring", "koi", "lionfish", "loach", "mackerel", "manta ray", "minnow",
    "neon tetra", "perch", "pike", "pompano", "rainbow trout", "rasbora", "sailfish", "sardine", "sockeye salmon", "sturgeon",
    "sunfish", "tarpon", "tuna", "walleye", "yellowfin tuna", "yellow perch", "anchovy", "bream", "bronze whaler", "butterflyfish",
    "chub", "cod", "coral trout", "damselfish", "darter", "dorado", "eel", "flounder", "garfish", "grunion",
    "hake", "lamprey", "ling", "mohar", "mullet", "paddlefish", "pufferfish", "rockfish", "sculpin", "seatrout",
    "snapper", "sole", "sucker", "tarwhine", "toadfish", "trumpeter", "whiting", "bald eagle", "barn owl", "blackbird",
    "blue jay", "budgerigar", "canary", "cardinal", "chickadee", "crane", "crow", "cuckoo", "dove", "duck",
    "eagle", "falcon", "flamingo", "goldfinch", "goose", "heron", "hummingbird", "ibis", "kingfisher", "kite",
    "macaw", "magpie", "nightingale", "osprey", "owl", "parrot", "peacock", "pelican", "penguin", "pheasant",
    "pigeon", "quail", "raven", "robin", "seagull", "sparrow", "stork", "swallow", "swift", "vulture",
    "warbler", "woodpecker"
]


user_scores = {}

result_dict = {}

if not find_dotenv():
    exit('Отсутсвует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
API_KEY = os.getenv("API_KEY")